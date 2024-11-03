import ast
import os
import threading
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout, QPushButton, QCheckBox, \
    QComboBox, QProgressBar, QFileDialog, QVBoxLayout, QGroupBox
from PyQt5.QtGui import QDesktopServices, QIntValidator
from PyQt5.QtCore import QUrl, QEasingCurve, QPropertyAnimation
from PyQt5.QtCore import QObject, pyqtSignal

import resources.BaseFunc as BG
import resources.CORE as COR


class Communicate(QObject):
    signal = pyqtSignal(str, int)


class Communicate2(QObject):
    signal = pyqtSignal(int)


class SmoothProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setRange(0, 100)
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setDuration(200)  # Длительность анимации

    def set_new_range(self, min, max):
        self.setRange(min, max)

    def setValue(self, value):
        self.animation.setEndValue(value)
        self.animation.start()


class SlasherBKB(QWidget):
    def __init__(self):
        super().__init__()
        self.v_input_path = ""  # Путь к входной папке
        self.v_output_path = ""  # Путь к выходной папке
        self.v_count_slice = True  # Если True, то режем по кол-ву, иначе по желаемой высоте
        self.v_count_scans = 10  # Кол-во желаемых сканов на выходе
        self.v_custom_height = 30000  # Желаемая высота сканов на выходе
        self.v_consider_psd = True  # Принимаем ли ПСД
        self.v_cruel_slash = False  # Жесткая ли разрезка или нет
        self.v_ignorable_edges_pixels = 10  # Отступы между сканами
        self.v_custom_width = 0  # Кастомная ширина сканов
        self.v_type_images_output = ".png"  # Выходной тип сканов
        self.progress_value = 0
        self.all_progess_val = 0
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
        self.batch_mode = QCheckBox("Пакетная обработка?")

        self.first_layout.addWidget(self.input_path, 0, 0)
        self.first_layout.addWidget(self.select_folder_btn, 0, 1)
        self.first_layout.addWidget(self.output_path, 1, 0, 1, 1)
        self.first_layout.addWidget(self.batch_mode, 1, 1)

        self.first_group.setLayout(self.first_layout)
        self.first_group.setFixedHeight(100)

        # Второй раздел
        self.second_group = QGroupBox("Базовые настройки:")
        self.second_layout = QGridLayout()
        self.second_layout.setColumnStretch(0, 1)
        self.second_layout.setColumnStretch(1, 1)

        self.scan_height_cb = QCheckBox("Высота скана(в пикселях):")
        self.scan_count_cb = QCheckBox("Кол-во сканов на выходе:")

        self.scan_height_cb.stateChanged.connect(
            lambda state: self.pixel_state(state, self.scan_count_cb))
        self.scan_count_cb.stateChanged.connect(
            lambda state: self.pixel_state(state, self.scan_height_cb))

        self.height_edit = QLineEdit()
        self.height_edit.setValidator(QIntValidator())
        self.count_edit = QLineEdit()
        self.count_edit.setValidator(QIntValidator())
        self.type_output = QComboBox()
        self.type_output.addItems([".png", ".jpeg", ".jpg"])
        self.action_btn = QPushButton("VK BIKINI BOTTOM")
        self.action_btn.clicked.connect(self.open_link)

        self.second_layout.addWidget(self.scan_height_cb, 0, 0)
        self.second_layout.addWidget(self.scan_count_cb, 0, 1)
        self.second_layout.addWidget(self.height_edit, 1, 0)
        self.second_layout.addWidget(self.count_edit, 1, 1)
        self.second_layout.addWidget(self.type_output, 2, 0)
        self.second_layout.addWidget(self.action_btn, 2, 1)

        self.second_group.setLayout(self.second_layout)
        self.second_group.setFixedHeight(130)

        # Третий раздел
        self.third_group = QGroupBox("Дополнительные настройки:")
        self.third_layout = QGridLayout()
        self.third_layout.setColumnStretch(0, 1)
        self.third_layout.setColumnStretch(1, 1)

        self.psd_cb = QCheckBox("Принимать PSD?")
        self.hard_cut_cb = QCheckBox("Жесткая резка?")
        self.border_label = QLabel("Игнорируемые пиксели границ:")
        self.width_label = QLabel("Настройка ширины(0 - для игнорирования)")
        self.border_edit = QLineEdit()
        self.border_edit.setValidator(QIntValidator())
        self.width_combo = QLineEdit()
        self.width_combo.setValidator(QIntValidator())

        self.third_layout.addWidget(self.psd_cb, 0, 0)
        self.third_layout.addWidget(self.hard_cut_cb, 0, 1)
        self.third_layout.addWidget(self.border_label, 1, 0)
        self.third_layout.addWidget(self.width_label, 1, 1)
        self.third_layout.addWidget(self.border_edit, 2, 0)
        self.third_layout.addWidget(self.width_combo, 2, 1)

        self.third_group.setLayout(self.third_layout)
        self.third_group.setFixedHeight(120)

        # Четвертый раздел
        self.fourth_group = QGroupBox("Процесс:")
        self.fourth_layout = QGridLayout()

        self.status = QLabel("Простой")
        self.start_btn = QPushButton("ПОПЛЫЛИ")
        self.start_btn.clicked.connect(self.running_proc)

        self.communicate = Communicate()
        self.communicate.signal.connect(self.update_gui_progress)

        self.communicate2 = Communicate2()
        self.communicate2.signal.connect(self.update_max_progress_bar)

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
        self.main_layout.addWidget(self.third_group)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.fourth_group)

        self.setLayout(self.main_layout)
        # self.setFixedSize(532, 450)

    def setup_setting(self):
        self.scan_count_cb.setChecked(self.v_count_slice)
        self.scan_height_cb.setChecked(not self.v_count_slice)
        self.count_edit.setText(str(self.v_count_scans))
        self.height_edit.setText(str(self.v_custom_height))

        self.psd_cb.setChecked(self.v_consider_psd)
        self.hard_cut_cb.setChecked(self.v_cruel_slash)
        self.border_edit.setText(str(self.v_ignorable_edges_pixels))
        self.width_combo.setText(str(self.v_custom_width))
        self.type_output.setCurrentText(str(self.v_type_images_output))

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
            if "[SLASH]" in folder_name:
                self.output_path.setText(folder_path + f"/{folder_name}")
            else:
                self.output_path.setText(folder_path + f"/{folder_name}[SLASH]")

    def pixel_state(self, state, other_checkbox):
        if state == 0:
            other_checkbox.setChecked(True)
        else:
            other_checkbox.setChecked(False)

    def open_link(self):
        QDesktopServices.openUrl(QUrl("https://vk.com/bkbmanga"))

    def unload_setting(self):
        (self.v_consider_psd, self.v_custom_width, self.v_custom_height,
         self.v_count_scans, self.v_cruel_slash, self.v_ignorable_edges_pixels, self.v_type_images_output,
         self.v_count_slice, _, _, _, _) = BG.get_settings()
        self.v_count_slice = ast.literal_eval(self.v_count_slice)
        self.v_consider_psd = ast.literal_eval(self.v_consider_psd)
        self.v_cruel_slash = ast.literal_eval(self.v_cruel_slash)
        self.setup_setting()

    def save_setting(self):
        self.v_count_slice = str(self.scan_count_cb.isChecked())
        self.v_consider_psd = str(self.psd_cb.isChecked())
        self.v_cruel_slash = str(self.hard_cut_cb.isChecked())
        self.v_count_slice = ast.literal_eval(self.v_count_slice)
        self.v_consider_psd = ast.literal_eval(self.v_consider_psd)
        self.v_cruel_slash = ast.literal_eval(self.v_cruel_slash)

        self.v_custom_width = str(self.width_combo.text())
        self.v_custom_height = str(self.height_edit.text())
        self.v_count_scans = str(self.count_edit.text())
        self.v_ignorable_edges_pixels = str(self.border_edit.text())
        self.v_type_images_output = str(self.type_output.currentText())
        BG.save_slasher(str(self.v_consider_psd), self.v_custom_width, self.v_custom_height, self.v_count_scans,
                        self.v_cruel_slash, self.v_ignorable_edges_pixels, self.v_type_images_output,
                        self.v_count_slice)

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
        if self.v_custom_width == "":
            self.status.setText("Не указана желаемая ширина")
            return False
        if self.v_ignorable_edges_pixels == "":
            self.status.setText("Не указаны игнорируемые пиксели границ")
            return False
        if self.v_custom_height == "" and self.v_count_slice == False:
            self.status.setText("Не указана желаемая высота сканов")
            return False
        if self.v_count_scans == "" and self.v_count_slice == True:
            self.status.setText("Не указано желаемое кол-во сканов")
            return False
        return True

    def start_long_operation(self):
        # Запуск функции резалки в потоке
        thread = threading.Thread(target=self.launch_slash, daemon=True)
        thread.start()

    def running_proc(self):
        self.save_setting()
        self.v_input_path = self.input_path.text()
        self.v_output_path = self.output_path.text()
        if self.preprocess_check() == False:
            pass
        else:
            self.progress_value = 0
            self.start_long_operation()

    def launch_slash(self):
        self.all_progess_val = 0
        self.progress_value = 0
        if self.batch_mode.isChecked() == False:
            self.communicate2.signal.emit(100)
            self.running_one_dir(self.v_input_path, self.v_output_path, "0/1")
            self.communicate.signal.emit(f"Готово - 1/1!", 100 - self.progress_value)
        else:
            path = self.v_input_path
            subdirs = [os.path.join(path, d) for d in os.listdir(path)
                       if os.path.isdir(os.path.join(path, d))]
            len_dirs = len(subdirs)
            self.communicate2.signal.emit(int(len_dirs * 100))
            ind = 0
            for dir in subdirs:
                self.progress_value = 0
                folder_name = os.path.basename(dir)
                output_path = f"{self.v_output_path}/{folder_name}"
                self.running_one_dir(dir, output_path, f"{ind}/{len_dirs}")
                ind += 1
            self.communicate.signal.emit(f"Готово - {ind}/{len_dirs}!", 100 - self.progress_value)

    def running_one_dir(self, input_path, output_path, num_chap):
        self.communicate.signal.emit(f"Работа {num_chap} - грузим изображения", 2)  # summ = 2
        conv_in_memo = COR.Converter(self.v_consider_psd)
        abs_path_image = conv_in_memo.get_images_paths(input_path)
        converted_images = conv_in_memo.convert_image_onec_type(abs_path_image)
        self.communicate.signal.emit(f"Работа {num_chap} - Изображения загружены в память", 2)  # summ = 4
        if self.v_count_slice:
            slash = COR.Slasher(custom_width=int(self.v_custom_width), custom_height=0,
                                custom_count_images=int(self.v_count_scans), cruel_slash=self.v_cruel_slash,
                                ignorable_edges_pixels=int(self.v_ignorable_edges_pixels),
                                type_images_output=str(self.v_type_images_output))
        else:
            slash = COR.Slasher(custom_width=int(self.v_custom_width), custom_height=int(self.v_custom_height),
                                custom_count_images=0, cruel_slash=self.v_cruel_slash,
                                ignorable_edges_pixels=int(self.v_ignorable_edges_pixels),
                                type_images_output=str(self.v_type_images_output))
        self.communicate.signal.emit(f"Работа {num_chap} - Ищем где резать", 1)  # summ = 5
        slices_images = slash.running_slash(converted_images, num_chap,
                                            self.update_saving_progress)  # Тут с 5 до 45, то есть надо 40
        self.communicate.signal.emit(f"Работа {num_chap} - Сохраняем", 5)  # summ = 50
        slash.saves_images(output_path, slices_images, num_chap, self.update_saving_progress)
        self.communicate.signal.emit("Готово", 100 - self.progress_value)  # summ = 100

    def update_max_progress_bar(self, val):
        self.progress_bar.set_new_range(0, int(val))

    def update_gui_progress(self, status_message, progress_increase):
        self.progress_value += progress_increase
        self.all_progess_val += progress_increase
        self.status.setText(status_message)
        self.progress_bar.setValue(int(self.all_progess_val))

    def update_saving_progress(self, message, plus):
        self.communicate.signal.emit(message, plus)
