from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea

import resources.BaseFunc as BG


class ScrollableButtonList(QWidget):
    def __init__(self, item):
        super().__init__()
        self.initial_items = item
        self.initUI()

    def initUI(self):
        # Создаем основной layout
        self.main_layout = QVBoxLayout(self)

        # Создаем scroll area
        self.scroll = QScrollArea()
        self.main_layout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)

        # Создаем widget для содержимого scroll area
        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)

        # Layout для кнопок
        self.buttons_layout = QVBoxLayout(self.content_widget)
        self.buttons_layout.setAlignment(Qt.AlignTop)
        self.buttons_layout.setSpacing(0)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Добавляем начальные кнопки
        for item in self.initial_items:
            self.add_new_button(item)

    def delete_button(self, container, button_text):
        BG.delete_by_name(str(button_text))
        container.deleteLater()

    def push_button(self, container, button_text):
        BG.set_template_to_preset(str(button_text))

    def add_new_button(self, text=None):
        # Создаем контейнер для пары кнопок
        container = QWidget()

        layout = QHBoxLayout(container)

        # Основная кнопка
        main_btn = QPushButton(text)

        # Кнопка удаления
        delete_btn = QPushButton("Удалить")
        delete_btn.setFixedWidth(70)

        layout.addWidget(main_btn)
        layout.addWidget(delete_btn)

        # Добавляем контейнер в основной layout
        self.buttons_layout.addWidget(container)

        # Подключаем функцию удаления
        delete_btn.clicked.connect(lambda: self.delete_button(container, text))
        main_btn.clicked.connect(lambda: self.push_button(container, text))


class Templates(QWidget):
    def __init__(self):
        super().__init__()

        lst = BG.get_all_templates()
        self.names_all_temp = [x[0] for x in lst]

        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)
        self.first_group = QGroupBox("Добавить шаблон")
        self.first_layout = QGridLayout()
        self.name_templ = QLineEdit()
        self.add_templ_btn = QPushButton("Добавить шаблон")
        self.add_templ_btn.clicked.connect(self.create_templates)

        self.first_layout.addWidget(self.name_templ, 0, 0)
        self.first_layout.addWidget(self.add_templ_btn, 0, 1)
        self.first_group.setLayout(self.first_layout)
        self.first_group.setFixedHeight(70)


        # Второй раздел
        self.second_group = QGroupBox("Выбрать шаблон:")
        self.second_layout = QGridLayout()
        self.second_layout.setColumnStretch(0, 1)
        self.second_layout.setColumnStretch(1, 1)

        self.templates_buttons_class = ScrollableButtonList(self.names_all_temp)

        self.second_layout.addWidget(self.templates_buttons_class, 1, 0, 1, 2)

        self.second_group.setLayout(self.second_layout)
        self.second_group.setFixedHeight(432)

        self.main_layout.addWidget(self.first_group)
        self.main_layout.addWidget(self.second_group)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def create_templates(self):
        name_new_templ = self.name_templ.text()
        if name_new_templ in self.names_all_temp:
            pass
        else:
            if name_new_templ != "" or name_new_templ != " ":
                BG.create_template(name_new_templ)
                self.templates_buttons_class.add_new_button(name_new_templ)
