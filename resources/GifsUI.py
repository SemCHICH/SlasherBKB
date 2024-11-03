import ast
import os
import threading

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIntValidator, QDesktopServices
from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QLabel, \
    QCheckBox

from resources.SlasherUI import Communicate, SmoothProgressBar
import resources.BaseFunc as BG
import resources.CORE as COR


class GifsConvert(QWidget):
    def __init__(self):
        super().__init__()
        self.v_input_path = ""  # Путь к входной папке
        self.v_output_path = ""  # Путь к выходной папке
        self.v_consider_psd = True  # Принимаем ли ПСД
        self.v_save_temp_png = True  # Cохранять ли временные ПНГшки?
        self.v_quality_jpg = 60  # Качество конвертации
        self.v_do_gif = True  # Качество конвертации
        self.progress_value = 0
        self.initUI()
        self.unload_setting()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)

        # Первый раздел
        self.first_group = QGroupBox("Выбор папок:")
        self.first_layout = QGridLayout()

        self.input_path = QLineEdit()
        self.select_folder_btn = QPushButton("Выбрать папку")
        self.select_folder_btn.clicked.connect(self.show_folder_dialog)
        self.output_path = QLineEdit()

        self.first_layout.addWidget(self.input_path, 0, 0)
        self.first_layout.addWidget(self.select_folder_btn, 0, 1)
        self.first_layout.addWidget(self.output_path, 1, 0, 1, 2)

        self.first_group.setLayout(self.first_layout)
        self.first_group.setFixedHeight(100)

        # Второй раздел
        self.second_group = QGroupBox("Настройки:")
        self.second_layout = QGridLayout()
        self.second_layout.setColumnStretch(0, 1)
        self.second_layout.setColumnStretch(1, 1)
        self.psd_cb = QCheckBox("Принимать PSD?")
        self.do_gifs = QCheckBox("Делать Гиф?")
        self.save_templ_png = QCheckBox("Сохранять пнгшки?")
        self.quality_label = QLabel("Качество конвертации (%)")
        self.quality_jpg = QLineEdit()
        self.quality_jpg.setValidator(QIntValidator())
        self.action_btn = QPushButton("Читать Гайд")
        self.action_btn.clicked.connect(self.open_link)

        self.second_layout.addWidget(self.psd_cb, 0, 0)
        self.second_layout.addWidget(self.do_gifs, 0, 1)
        self.second_layout.addWidget(self.quality_label, 1, 0)
        self.second_layout.addWidget(self.save_templ_png, 1, 1)
        self.second_layout.addWidget(self.quality_jpg, 2, 0)
        self.second_layout.addWidget(self.action_btn, 2, 1)
        self.second_group.setLayout(self.second_layout)
        self.second_group.setFixedHeight(130)

        # Третий раздел
        self.fourth_group = QGroupBox("Процесс:")
        self.fourth_layout = QGridLayout()

        self.status = QLabel("Простой")
        self.start_btn = QPushButton("ПОПЛЫЛИ")
        self.start_btn.clicked.connect(self.running_proc)

        self.communicate = Communicate()
        self.communicate.signal.connect(self.update_gui_progress)

        self.progress_bar = SmoothProgressBar()

        self.fourth_layout.addWidget(self.status, 0, 0)
        self.fourth_layout.addWidget(self.start_btn, 0, 1)
        self.fourth_layout.addWidget(self.progress_bar, 1, 0, 1, 2)

        self.fourth_group.setLayout(self.fourth_layout)
        self.fourth_group.setFixedHeight(100)

        # Добавляем все разделы в главный layout
        self.main_layout.addWidget(self.first_group)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.second_group)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.fourth_group)

        self.setLayout(self.main_layout)

    def setup_setting(self):
        self.psd_cb.setChecked(self.v_consider_psd)
        self.do_gifs.setChecked(self.v_do_gif)
        self.save_templ_png.setChecked(self.v_save_temp_png)
        self.quality_jpg.setText(self.v_quality_jpg)

    def unload_setting(self):
        (_, _, _,
         _, _, _, _,
         _, self.v_consider_psd, self.v_save_temp_png, self.v_quality_jpg, self.v_do_gif) = BG.get_settings()
        self.v_consider_psd = ast.literal_eval(self.v_consider_psd)
        self.v_save_temp_png = ast.literal_eval(self.v_save_temp_png)
        self.v_quality_jpg = self.v_quality_jpg
        self.v_do_gif = ast.literal_eval(self.v_do_gif)
        self.setup_setting()

    def save_setting(self):
        self.v_consider_psd = self.psd_cb.isChecked()
        self.v_save_temp_png = self.save_templ_png.isChecked()
        self.v_quality_jpg = self.quality_jpg.text()
        self.v_do_gif = self.do_gifs.isChecked()
        BG.save_gifs(str(self.v_consider_psd), str(self.v_save_temp_png), str(self.v_quality_jpg), str(self.v_do_gif))

    def show_folder_dialog(self):
        # Открываем диалоговое окно выбора папки
        last_path = BG.get_other_settings()[0]
        if last_path != "":
            if os.path.exists(last_path):
                folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", last_path)
            else:
                last_path = os.path.dirname(last_path)
                folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", last_path)
        else:
            folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        # Обновляем строку ввода пути и метку с выбранной папкой
        if folder_path:
            BG.save_other_settings(str(folder_path))
            self.input_path.setText(folder_path)
            folder_name = os.path.basename(folder_path)
            folder_name = folder_name.replace("[SLASH]", "")
            self.output_path.setText(folder_path + f"/{folder_name}[GIF]")

    def open_link(self):
        QDesktopServices.openUrl(QUrl("https://github.com/SemCHICH/SlasherBKB"))

    def start_long_operation(self):
        thread = threading.Thread(target=self.launch_converting, daemon=True)
        thread.start()

    def update_gui_progress(self, status_message, progress_increase):
        self.progress_value += progress_increase
        self.status.setText(status_message)
        self.progress_bar.setValue(int(self.progress_value))

    def preprocess_check(self):
        if str(self.v_input_path) == "":
            self.status.setText("Не указан путь к входной папке!")
            return False
        if str(self.v_output_path) == "":
            self.status.setText("Не задан путь к выходной папке!")
            return False
        if not os.path.exists(str(self.v_input_path)):
            self.status.setText("Путь к входной папке не существует.")
            return False
        if self.v_quality_jpg == "":
            self.status.setText("Не указано качество")
            return False
        if int(self.v_quality_jpg) > 100 or int(self.v_quality_jpg) < 1:
            self.status.setText("Качество должно быть больше 0 и меньше 100")
            return False
        return True

    def running_proc(self):
        self.save_setting()
        self.v_input_path = self.input_path.text()
        self.v_output_path = self.output_path.text()
        if self.preprocess_check() == False:
            pass
        else:
            self.progress_value = 0
            self.start_long_operation()

    def launch_converting(self):
        self.communicate.signal.emit("Работа - грузим изображения", 2)
        gifc = COR.ConverterGif(self.v_output_path, consider_psd=self.v_consider_psd, save_temp_png=self.v_save_temp_png, quality_jpg=int(self.v_quality_jpg), do_gif=self.v_do_gif)
        self.communicate.signal.emit("Работа - изображения загружены", 3)
        gifc.running(self.v_input_path, self.update_saving_progress)
        self.communicate.signal.emit("Готово!", int(100-self.progress_value))

    def update_saving_progress(self, message, plus):
        self.communicate.signal.emit(message, plus)

