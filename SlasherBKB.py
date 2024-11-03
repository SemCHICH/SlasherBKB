from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QSizePolicy, QLabel, QTabWidget)
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt
import sys

import resources.SlasherUI as SlasherUI
import resources.GifsUI as GifsUI
import resources.TemplatesUI as TemplatesUI
import res.stylesheet as styu


class TitleBarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(46, 30)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888888;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #404040;
                color: white;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)


class DarkFrameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.dragPos = None
        self.previous_tab = 0
        self.setWindowTitle('SlasherBKB')
        self.setWindowIcon(QIcon('res/SlasherBKBLogo.ico'))
        self.setFixedSize(600, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background: transparent;
            }
            QWidget#mainContainer {
                background-color: #2d2d2d;
                border: 1px solid #1a1a1a;
                border-radius: 8px;
            }
            QWidget#titleBar {
                background-color: #1a1a1a;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QWidget#contentWidget {
                background-color: #2d2d2d;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QLabel#titleLabel {
                color: #ffffff;
                font-size: 14px;
            }
        """)

        self.main_container = QWidget()
        self.main_container.setObjectName("mainContainer")
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_container)

        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.title_bar = QWidget()
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(30)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 0, 0)
        title_layout.setSpacing(5)

        self.icon_label = QLabel()
        icon_pixmap = QPixmap('res/SlasherBKBLogo.ico')
        if not icon_pixmap.isNull():
            self.icon_label.setPixmap(icon_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            print("Не удалось загрузить иконку")
        self.icon_label.setFixedSize(16, 16)
        title_layout.addWidget(self.icon_label)

        self.title_label = QLabel("SlasherBKB [3.0]")
        self.title_label.setObjectName("titleLabel")
        title_layout.addWidget(self.title_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        title_layout.addWidget(spacer)

        self.minimize_button = TitleBarButton("🗕")
        self.minimize_button.clicked.connect(self.showMinimized)

        self.close_button = TitleBarButton("✕")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888888;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
            QPushButton:pressed {
                background-color: #bf0f1d;
            }
            QPushButton:hover {
                border-top-right-radius: 8px;
            }
        """)
        self.close_button.clicked.connect(self.close)

        title_layout.addWidget(self.minimize_button)
        title_layout.addWidget(self.close_button)

        container_layout.addWidget(self.title_bar)

        self.content = QWidget()
        self.content.setStyleSheet(styu.load_styling())

        self.content.setObjectName("contentWidget")
        container_layout.addWidget(self.content)

        # Создаем layout для контента
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # Создаем и настраиваем tab widget
        self.tab_widget = QTabWidget(self)
        self.slash_window = SlasherUI.SlasherBKB()
        self.tab_widget.addTab(self.slash_window, "Слэшер")
        self.tab_widget.tabBar().setTabTextColor(self.tab_widget.indexOf(self.slash_window), QColor("black"))

        self.gifs_window = GifsUI.GifsConvert()
        self.tab_widget.addTab(self.gifs_window, "Гифки")
        self.tab_widget.tabBar().setTabTextColor(self.tab_widget.indexOf(self.gifs_window), QColor("black"))

        self.templates_window = TemplatesUI.Templates()
        self.tab_widget.addTab(self.templates_window, "Шаблоны")
        self.tab_widget.tabBar().setTabTextColor(self.tab_widget.indexOf(self.templates_window), QColor("black"))

        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Добавляем tab widget в layout контента
        content_layout.addWidget(self.tab_widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Получаем позицию клика относительно title_bar
            title_bar_pos = self.title_bar.mapFromGlobal(event.globalPos())

            # Проверяем, находится ли клик в пределах title_bar
            if self.title_bar.rect().contains(title_bar_pos):
                self.dragging = True
                self.dragPos = event.globalPos()
                event.accept()
            else:
                self.dragging = False
                event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragging and self.dragPos is not None:
            # Перемещаем окно только если мы в режиме перетаскивания
            delta = event.globalPos() - self.dragPos
            self.move(self.pos() + delta)
            self.dragPos = event.globalPos()
            event.accept()
        else:
            event.ignore()

    def closeEvent(self, event):
        self.slash_window.save_setting()
        self.gifs_window.save_setting()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.dragPos = None
            event.accept()

    def on_tab_changed(self, current_index):
        if self.previous_tab == 0:
            self.slash_window.save_setting()
        elif self.previous_tab == 1:
            self.gifs_window.save_setting()
        elif self.previous_tab == 2:
            self.slash_window.unload_setting()
            self.gifs_window.unload_setting()
        self.previous_tab = current_index


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создаем и показываем окно
    window = DarkFrameWindow()
    window.show()

    sys.exit(app.exec_())
