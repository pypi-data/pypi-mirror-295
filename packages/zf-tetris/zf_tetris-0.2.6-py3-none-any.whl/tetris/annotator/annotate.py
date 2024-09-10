from base64 import b64encode
from collections import OrderedDict
from glob import glob
from json import dump as json_dump
from json import load as json_load
from os import path as os_path
from random import choice as random_choice
from re import search as re_search
from sys import argv

from loguru import logger
from openai import OpenAI
from PIL import Image
from PyQt5.QtWidgets import QApplication

from ..config import settings
from ..models import models
from .icons import Icons
from .image import ImageAnnotationTool

TETRIS_PATH = settings.TETRIS_PATH


class Annotator:
    def __init__(self):
        self.app = None
        self.tool = None
        self.client = OpenAI(api_key=settings.TETRIS_OPENAI_API_KEY)
        self.templates = OrderedDict()

    def run(self, meme, randomize):
        if not self.app:
            self.app = QApplication(argv)
            Icons.load_icons()

        meme_path = self.__select_meme__(meme, randomize)
        if not meme_path:
            logger.error(f"Meme {meme} not found")
            return

        logger.info(f"Picked meme {meme_path} for annotation")
        self.annotate(meme_path)

        self.app.exec_()

    def annotate(self, image_path: str):
        image_source = models.FileSource.from_filepath(image_path)
        description = self.__describe_meme__(image_source=image_source)
        self.preview(image_source, description)

    def preview(self, image_source: str | models.FileSource, image_description: str):
        if isinstance(image_source, str):
            image_source = models.FileSource.from_filepath(image_source)

        if self.tool:
            self.tool.close()

        self.tool = ImageAnnotationTool(image_source, image_description)
        self.tool.annotationSaved.connect(self.on_saved)
        self.tool.refreshed.connect(self.on_refreshed)
        self.tool.show()

    def process_events(self):
        self.app.processEvents()
        if not self.tool.isVisible():
            self.app.quit()

    def on_saved(self, result: tuple[models.FileSource, list[models.TextZone], bool]):
        image_source, text_zones, description, should_close = result
        self.templates[image_source.name]["text_zones"] = [tz.model_dump() for tz in text_zones]
        self.templates[image_source.name]["description"] = description

        with open(f"{image_source.dir}/templates.json", "w") as f:
            json_dump(self.templates, f, indent=2)

        if should_close:
            self.tool.close()

        logger.info("Saved annotations")

    def on_refreshed(self, result):
        meme_path = self.__select_meme__(None, True)
        if meme_path:
            self.annotate(meme_path)
        else:
            logger.error("No memes found for refresh")

    def __select_meme__(self, meme: str, randomize: bool) -> str:
        meme_path, meme_name = None, None

        meme_paths = glob(f"{TETRIS_PATH}/templates/**/*.png")
        meme_schemas_paths = glob(f"{TETRIS_PATH}/templates/**/*.json")

        logger.info(f"Meme paths: {meme_paths}")
        logger.info(f"Meme schemas paths: {meme_schemas_paths}")

        # del all path from meem_paths that end with -1.png or -2.png or -3.png basically -\d.png
        meme_paths = [path for path in meme_paths if not re_search(r"_\d+\.png", path)]

        logger.info(f"Found {len(meme_paths)} meme paths at {TETRIS_PATH}/templates")

        all_meme_schemas = {}
        for meme_schemas_path in meme_schemas_paths:
            meme_schemas_dict = json_load(open(meme_schemas_path, "r"))  # directory level

            for k, v in meme_schemas_dict.items():
                p = meme_schemas_path.replace("templates.json", f"{k}.png")
                all_meme_schemas[(p, k)] = v

        logger.info(f"Loaded schemas for {len(all_meme_schemas)} memes")

        if randomize:
            meme_path = random_choice(meme_paths)
            meme_name = os_path.basename(meme_path).replace(".png", "")

            while (meme_path, meme_name) in all_meme_schemas.keys():
                meme_path = random_choice(meme_paths)
                meme_name = os_path.basename(meme_path).replace(".png", "")
        else:
            meme = meme.strip().replace(" ", "_")

            for meme_path in meme_paths:
                if meme in meme_path:
                    meme_path = meme_path
                    break

        return meme_path

    def __describe_meme__(self, image_source: models.FileSource):
        templates_path = f"{image_source.dir}/templates.json"

        if os_path.exists(templates_path):
            with open(templates_path, "r") as f:
                self.templates = OrderedDict(sorted(json_load(f).items()))
        else:
            self.templates = OrderedDict()

        description = ""
        if image_source.name in self.templates and "description" in self.templates[image_source.name]:
            description = self.templates[image_source.name]["description"]
        else:
            image_base64 = None
            with open(image_source.path, "rb") as image_file:
                image_base64 = b64encode(image_file.read()).decode("utf-8")
                logger.debug(f"Loaded image {image_source.name} from {image_source.path}")

            result = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in understanding memes and explaining when to use them",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Explain the meme named {image_source.name} in two sentences. First sentence should describe the meme, second sentence should describe when to use it.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}",
                                },
                            },
                        ],
                    },
                ],
                max_tokens=200,
            )

            name_formats = models.name_formats(image_source.name)
            description = result.choices[0].message.content

            logger.info(f"Annotated meme {image_source.name}: {description}")

            self.templates[image_source.name] = {
                "name": name_formats[models.NameFormat.SPACE_CASE],
                "filename": f"{image_source.name}.{image_source.type}",
                "description": description,
            }

            self.templates = OrderedDict(sorted(self.templates.items()))

        if "width" not in self.templates[image_source.name] or "height" not in self.templates[image_source.name]:
            with Image.open(image_source.path) as img:
                width, height = img.size

            self.templates[image_source.name]["width"] = width
            self.templates[image_source.name]["height"] = height

        return description
