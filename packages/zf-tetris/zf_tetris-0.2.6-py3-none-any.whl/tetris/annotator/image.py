import os
from json import load as json_load
from os import path as os_path

from loguru import logger
from PyQt5.QtCore import QPoint, QRect, QRectF, QSizeF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QKeySequence, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QShortcut,
    QSplitter,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..models import models
from .dialog import AnnotationInputDialog
from .icons import Icons


class ImageAnnotationTool(QMainWindow):
    annotationSaved = pyqtSignal(object)
    refreshed = pyqtSignal(object)

    def __init__(self, image_source: models.FileSource | None = None, image_description: str = ""):
        super().__init__()
        self.initUI(image_source, image_description)  # Loads the image and annotations
        self.setup_shortcuts()

        self.resize_handle = None
        self.resizing_index = -1
        self.scale_factor = 1.0

    def initUI(self, image_source: models.FileSource | None = None, image_description: str = ""):
        self.image_source = image_source
        self.image_description = image_description

        self.original_image = None
        self.image = None  # scaled

        self.cached_description: str = ""
        self.description: str = ""

        self.original_text_zones: list[models.TextZone] = []
        self.cached_text_zones: list[models.TextZone] = []
        self.text_zones: list[models.TextZone] = []  # scaled

        self.unsaved_changes = False

        self.start_point = None
        self.current_rect = None

        self.setWindowTitle("Image Annotation Tool")
        self.setGeometry(100, 100, 1000, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.description_text_area = QTextEdit()
        self.description_text_area.setPlaceholderText("Enter meme description here...")
        self.description_text_area.setMaximumHeight(100)
        self.description_text_area.setText(self.image_description)
        main_layout.addWidget(self.description_text_area)

        image_and_annotations_layout = QHBoxLayout()
        main_layout.addLayout(image_and_annotations_layout)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(768)
        left_layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Image")
        load_button.clicked.connect(self.load_image)
        button_layout.addWidget(load_button)

        self.save_button = QPushButton("Save Annotations")
        self.save_button.clicked.connect(self.save_annotations)
        button_layout.addWidget(self.save_button)

        left_layout.addLayout(button_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        self.annotation_list = QListWidget()
        self.annotation_list.setMinimumWidth(350)
        right_layout.addWidget(QLabel("Annotations:"))
        right_layout.addWidget(self.annotation_list)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([700, 300])

        image_and_annotations_layout.addWidget(splitter)

        if image_source:
            self.load_image_from_file_source(image_source.path)

        if self.image:
            self.display_image()

    def setup_shortcuts(self):
        refresh_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        refresh_shortcut.activated.connect(self.refresh)

        close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_shortcut.activated.connect(self.close)

        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save)

    def load_image_from_file_source(self, image_path: str):
        if not os.path.exists(image_path):
            logger.error(f"File not found: {image_path}")
            return

        self.original_image = QPixmap(image_path)
        if self.original_image.isNull():
            logger.error(f"Failed to load image from {image_path}")
            return

        self.image_source = models.FileSource.from_filepath(image_path)
        logger.info(f"Successfully loaded image from {image_path}")

        self.load_and_scale_image()
        self.load_and_scale_annotations()
        self.display_image()

        self.annotation_list.clear()
        for text_zone in self.text_zones:
            self.add_annotation_to_list(text_zone)

    def load_and_scale_image(self):
        if self.original_image.height() > 768:
            self.scale_factor = 768 / self.original_image.height()

            new_width = int(self.original_image.width() * self.scale_factor)
            self.image = self.original_image.scaled(new_width, 768, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            self.scale_factor = 1.0
            self.image = QPixmap(self.original_image)

        self.image_label.setFixedSize(self.image.width(), self.image.height())

        logger.debug(f"Original image size: {self.original_image.width()}x{self.original_image.height()}")
        logger.debug(f"Scaled image size: {self.image.width()}x{self.image.height()}")
        logger.debug(f"Image label size: {self.image_label.width()}x{self.image_label.height()}")
        logger.debug(f"Scale factor: {self.scale_factor}")

        self.display_image()

    def load_and_scale_annotations(self):
        templates_path = f"{self.image_source.dir}/templates.json"

        self.original_text_zones = []
        if os_path.exists(templates_path):
            with open(templates_path, "r") as f:
                templates = json_load(f)

                if self.image_source.name in templates:
                    meme_data = templates[self.image_source.name]

                    if "text_zones" in meme_data:
                        self.original_text_zones = [models.TextZone(**tz) for tz in meme_data["text_zones"]]

        self.text_zones = [tz * self.scale_factor for tz in self.original_text_zones]

    def add_annotation_to_list(self, text_zone):
        item = QListWidgetItem()
        self.annotation_list.addItem(item)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text_zone.title)
        layout.addWidget(label)

        edit_button = QToolButton()
        edit_button.setIcon(Icons["pencil"])
        edit_button.clicked.connect(lambda: self.edit_annotation(item, text_zone))
        layout.addWidget(edit_button)

        delete_button = QToolButton()
        delete_button.setIcon(Icons["X"])
        delete_button.clicked.connect(lambda: self.delete_annotation(item, text_zone))
        layout.addWidget(delete_button)

        widget.setLayout(layout)

        item.setSizeHint(widget.sizeHint())
        self.annotation_list.setItemWidget(item, widget)

    def save_annotations(self, autosave=False):
        if not self.text_zones:
            logger.error("No annotations to save")
            return

        scale_factor = self.image.height() / self.original_image.height()
        original_text_zones = [tz / scale_factor for tz in self.text_zones]

        description = self.description_text_area.toPlainText()

        self.annotationSaved.emit((self.image_source, original_text_zones, description, not autosave))

        self.unsaved_changes = False
        self.update_save_button()

        if not autosave:
            logger.info("Annotations saved successfully")

    def add_new_annotation(self, rect):
        dialog = AnnotationInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, description, examples, font_family, font_size, font_color = dialog.get_inputs()
            text_zone = models.TextZone(
                bbox=(
                    rect.x(),
                    rect.y(),
                    rect.width(),
                    rect.height(),
                ),
                font_family=font_family,
                font_size=font_size,
                font_color=font_color,
                title=title,
                description=description,
                examples=examples,
            )
            self.text_zones.append(text_zone)
            self.add_annotation_to_list(text_zone)
            self.save_annotations(autosave=True)

    def edit_annotation(self, item, text_zone):
        dialog = AnnotationInputDialog(self, text_zone)
        if dialog.exec_() == QDialog.Accepted:
            title, description, examples, font_family, font_size, font_color = dialog.get_inputs()
            text_zone.title = title
            text_zone.description = description
            text_zone.examples = examples
            text_zone.font_family = font_family
            text_zone.font_size = font_size
            text_zone.font_color = font_color
            widget = self.annotation_list.itemWidget(item)
            label = widget.layout().itemAt(0).widget()
            label.setText(title)
            self.draw_image_with_annotations()
            self.save_annotations(autosave=True)

    def delete_annotation(self, item, text_zone):
        self.text_zones.remove(text_zone)
        self.annotation_list.takeItem(self.annotation_list.row(item))
        self.draw_image_with_annotations()
        self.save_annotations(autosave=True)

    def display_image(self):
        if self.image and not self.image.isNull():
            self.draw_image_with_annotations()
        else:
            logger.warning("Attempted to display null or non-existent image")

    def draw_image_with_annotations(self):
        if self.image:
            pixmap = QPixmap(self.image)
            painter = QPainter(pixmap)

            for text_zone in self.text_zones:
                rect = QRect(*text_zone.bbox)

                # Set pen to black for existing annotations
                painter.setPen(QColor(text_zone.font_color))
                painter.drawRect(rect)

                self.draw_resize_handles(painter, rect)

                # Draw the text
                font = QFont(text_zone.font_family, int(text_zone.font_size * self.scale_factor))
                painter.setFont(font)
                painter.setPen(QColor(text_zone.font_color))
                painter.drawText(rect, Qt.AlignCenter, text_zone.title)

            # Draw the current rectangle in red if it exists
            if self.current_rect:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
                painter.drawRect(self.current_rect)

            painter.end()
            self.image_label.setPixmap(pixmap)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png )")

        if file_name:
            self.load_image_from_file_source(file_name)
            self.display_image()

    def update_save_button(self):
        if self.unsaved_changes:
            self.save_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
            self.save_button.setText("Save Annotations*")
        else:
            self.save_button.setStyleSheet("")
            self.save_button.setText("Save Annotations")

    def mousePressEvent(self, event):
        if self.image and event.button() == Qt.LeftButton:
            pos = event.pos()
            label_pos = self.image_label.mapFrom(self, pos)
            image_rect = self.image_label.contentsRect()

            if image_rect.contains(label_pos):
                pos = QPoint(label_pos.x() - image_rect.x(), label_pos.y() - image_rect.y())

            self.resize_handle, self.resizing_index = self.get_resize_handle(pos)

            if self.resize_handle is None:
                self.start_point = pos
                self.current_rect = None
            else:
                self.start_point = pos

            self.draw_image_with_annotations()

    def mouseMoveEvent(self, event):
        """mouseMoveEvent either resizes annotation bboxes or draws a new annotation bbox"""
        if not self.start_point:
            return

        pos = self.image_label.mapFrom(self, event.pos())

        image_rect = self.image_label.contentsRect()
        if image_rect.contains(pos):
            pos = QPoint(pos.x() - image_rect.x(), pos.y() - image_rect.y())

        if self.resize_handle is not None:
            self.resize_annotation(pos)
        else:
            self.current_rect = QRect(self.start_point, pos).normalized()

        self.draw_image_with_annotations()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_point:
            end_point = self.image_label.mapFrom(self, event.pos())

            image_rect = self.image_label.contentsRect()
            if image_rect.contains(end_point):
                end_point = QPoint(end_point.x() - image_rect.x(), end_point.y() - image_rect.y())

            if self.resize_handle is not None:
                self.resize_handle = None
                self.resizing_index = -1

                self.unsaved_changes = True
            else:
                rect = QRect(self.start_point, end_point).normalized()

                if rect.width() > 10 and rect.height() > 10:
                    self.add_new_annotation(rect)

            self.start_point = None
            self.current_rect = None
            self.draw_image_with_annotations()
            self.update_save_button()

    def get_resize_handle(self, pos):
        for i, text_zone in enumerate(self.text_zones):
            rect = QRectF(*text_zone.bbox)
            handle_size = 10
            handles = [
                QRectF(rect.topLeft(), QSizeF(handle_size, handle_size)),
                QRectF(
                    rect.topRight().x() - handle_size,
                    rect.topRight().y(),
                    handle_size,
                    handle_size,
                ),
                QRectF(
                    rect.bottomLeft().x(),
                    rect.bottomLeft().y() - handle_size,
                    handle_size,
                    handle_size,
                ),
                QRectF(
                    rect.bottomRight().x() - handle_size,
                    rect.bottomRight().y() - handle_size,
                    handle_size,
                    handle_size,
                ),
            ]
            for j, handle in enumerate(handles):
                if handle.contains(pos):
                    return j, i
        return None, -1

    def resize_annotation(self, pos):
        if 0 <= self.resizing_index < len(self.text_zones):
            text_zone = self.text_zones[self.resizing_index]

            rect = QRectF(*text_zone.bbox)

            if self.resize_handle == 0:
                rect.setTopLeft(pos)
            elif self.resize_handle == 1:
                rect.setTopRight(pos)
            elif self.resize_handle == 2:
                rect.setBottomLeft(pos)
            elif self.resize_handle == 3:
                rect.setBottomRight(pos)

            self.text_zones[self.resizing_index].bbox = (
                int(rect.x()),
                int(rect.y()),
                int(rect.width()),
                int(rect.height()),
            )

            self.draw_image_with_annotations()

    def draw_resize_handles(self, painter, rect):
        handle_size = 10

        original_brush = painter.brush()  # Save the original brush
        original_pen = painter.pen()  # Save the original pen

        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)  # No outline for the handles

        painter.drawRect(rect.topLeft().x(), rect.topLeft().y(), handle_size, handle_size)
        painter.drawRect(
            rect.topRight().x() - handle_size,
            rect.topRight().y(),
            handle_size,
            handle_size,
        )
        painter.drawRect(
            rect.bottomLeft().x(),
            rect.bottomLeft().y() - handle_size,
            handle_size,
            handle_size,
        )
        painter.drawRect(
            rect.bottomRight().x() - handle_size,
            rect.bottomRight().y() - handle_size,
            handle_size,
            handle_size,
        )

        painter.setBrush(original_brush)
        painter.setPen(original_pen)

    def refresh(self):
        self.refreshed.emit(None)

    def save(self):
        self.save_annotations(autosave=True)

    def closeEvent(self, event):
        self.save_annotations(autosave=True)
        super().closeEvent(event)
