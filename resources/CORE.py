import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image as pil
from natsort import natsorted


class Converter:
    def __init__(self, consider_psd):
        self.consider_psd = consider_psd

    def get_images_paths(self, folder_path):
        # Допустимые расширения файлов
        if not self.consider_psd:
            valid_extensions = {'.png', '.jpeg', '.jpg', '.webp', '.jfif', '.bmp', '.tiff', '.tga'}
        elif self.consider_psd:
            valid_extensions = {'.png', '.jpeg', '.jpg', '.webp', '.jfif', '.bmp', '.tiff', '.tga', '.psd', '.psb'}
        else:
            valid_extensions = {'.png', '.jpeg', '.jpg', '.webp', '.jfif', '.bmp', '.tiff', '.tga'}
        # Список для хранения путей
        image_paths = []
        try:
            # Преобразуем путь в объект Path
            folder = Path(folder_path)
            # Проверяем существование папки
            if not folder.exists():
                raise FileNotFoundError(f"Папка {folder_path} не найдена")
            # Проходим только по файлам в указанной папке (без подпапок)
            for file_path in folder.iterdir():
                # Проверяем, что это файл (не папка) и проверяем расширение
                if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
                    # Добавляем путь в список
                    image_paths.append(str(file_path))
            image_paths = natsorted(image_paths)
            return image_paths
        except Exception as e:
            print(f"Ошибка при сканировании папки: {e}")
        return []

    def convert_image_onec_type(self, image_paths):
        converted_images = []
        for path in image_paths:
            with pil.open(path) as img:
                img_copy = img.copy()
                converted_images.append(img_copy)
        return converted_images


class Slasher:
    def __init__(self, custom_width, custom_height, custom_count_images, cruel_slash, ignorable_edges_pixels,
                 type_images_output):
        self.custom_width = custom_width  # Кастомная ширина
        self.custom_height = custom_height  # Длинна 1 скана
        self.custom_count_images = custom_count_images  # Кол-во сканов на выходе
        self.cruel_slash = cruel_slash  # Надо ли искать контуры или хуярим как есть
        self.ignorable_edges_pixels = ignorable_edges_pixels  # Игнорирование пикселей границ
        self.type_images_output = type_images_output

    def true_grayscale(self, image_in):
        # Загрузить изображение
        image = image_in.copy()
        # Defining all the parameters
        t_lower = 100  # Lower Threshold
        t_upper = 200  # Upper threshold
        aperture_size = 5  # Aperture size
        L2Gradient = True  # Boolean

        # Applying the Canny Edge filter
        # with Aperture Size and L2Gradient
        gray_image = cv2.Canny(image, t_lower, t_upper,
                               apertureSize=aperture_size,
                               L2gradient=L2Gradient)
        return gray_image

    def resize(self, images_pillow):
        if self.custom_width != 0:
            converted_images = []
            for image in images_pillow:
                new_width = self.custom_width
                ratio = new_width / image.size[0]
                new_height = int(image.size[1] * ratio)
                resized_img = image.resize((new_width, new_height), pil.Resampling.LANCZOS)
                converted_images.append(resized_img)
            return converted_images
        else:
            return images_pillow

    def new_count_heights(self, images, count):
        """Определяем новую высоту выходных изображение при кол-во моде"""
        widths, heights = zip(*(image.size for image in images))
        new_image_height = sum(heights)
        return new_image_height // int(count) + new_image_height // 120

    def combine_images(self, images):
        """Обьединение в одно изображение в памяти"""
        widths, heights = zip(*(image.size for image in images))
        new_image_width = max(widths)
        new_image_height = sum(heights)
        new_image = pil.new('RGB', (new_image_width, new_image_height))
        combine_offset = 0
        for image in images:
            new_image.paste(image, (0, combine_offset))
            combine_offset += image.size[1]
        return new_image, new_image_height

    def find_clean_stripe(self, canny_image, target_y, stripe_height=10):
        height, width = canny_image.shape
        min_distance = float('inf')
        best_y = None

        # Определяем границы поиска
        search_start = max(0, target_y - height)
        search_end = min(height - stripe_height, target_y + height)

        # Проходим по всем возможным позициям полосы
        for y in range(search_start, search_end):
            # Выделяем полосу
            stripe = canny_image[y:y + stripe_height, :]

            # Если в полосе нет белых пикселей (контуров)
            if not np.any(stripe):
                # Вычисляем расстояние до целевой позиции
                distance = abs(y - target_y)

                # Если это расстояние меньше предыдущего минимального
                if distance < min_distance:
                    min_distance = distance
                    best_y = y

        return best_y

    def split_image_to_heights(self, original_image_cv, all_height, num_ima, progress_func):
        gray_scale_image = self.true_grayscale(original_image_cv)
        search_h = self.custom_height
        ideal_slah = self.custom_height
        ideal_nums = int(all_height/ideal_slah)
        list_slash = []
        while search_h < all_height:
            find_slash = self.find_clean_stripe(gray_scale_image, search_h, self.ignorable_edges_pixels)
            if find_slash - ideal_slah > self.custom_height / 2:
                search_h = find_slash + self.custom_height - self.custom_height / 2
            else:
                ideal_slah += self.custom_height
                search_h = ideal_slah
            if (progress_func != None):
                progress_func(f"Работа {num_ima} - Ищем где резать!", int(40/ideal_nums))
            list_slash.append(find_slash)
        return list_slash

    def running_slash(self, list_images, num_ima=1, progress_func=None):
        resized_img = self.resize(list_images)
        if self.custom_count_images != 0:
            self.custom_height = self.new_count_heights(resized_img, self.custom_count_images)
        one_big_img, all_images_height = self.combine_images(resized_img)
        original_image_cv = cv2.cvtColor(np.array(one_big_img), cv2.COLOR_RGB2BGR)
        if self.cruel_slash == False:
            y_coordinates = self.split_image_to_heights(original_image_cv, all_images_height, num_ima, progress_func)
        else:
            y_coordinates = []
            start_h = self.custom_height
            while start_h < all_images_height:
                y_coordinates.append(start_h)
                start_h += self.custom_height
        y_coordinates = [0] + y_coordinates + [original_image_cv.shape[0]]
        sliced_images = []
        # Нарезаем изображение
        for i in range(len(y_coordinates) - 1):
            y1 = y_coordinates[i]
            y2 = y_coordinates[i + 1]
            # Вырезаем часть изображения
            slice_img = original_image_cv[y1:y2, :]
            sliced_images.append(slice_img)
        return sliced_images

    def saves_images(self, foldername, images_to_save, num_ima=1, progress_func=None):
        new_folder = str(foldername)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        imageIndex = 1
        count_images = len(images_to_save)
        for slice_img in images_to_save:
            if (progress_func != None):
                progress_func(f"Работа {num_ima} - Сохранение изображений!", int(50/count_images))
            is_success, im_buf_arr = cv2.imencode(f"{self.type_images_output}", slice_img)
            im_buf_arr.tofile(f'{new_folder}/{imageIndex:02}{self.type_images_output}')
            imageIndex += 1


class ConverterGif:
    def __init__(self, save_folder_name, consider_psd=False, save_temp_png=True, quality_jpg=60, do_gif=True):
        self.consider_psd = consider_psd
        self.save_temp_png = save_temp_png
        self.quality_jpg = quality_jpg
        self.do_gif = do_gif
        self.save_folder_name = save_folder_name

    def get_images_paths(self, folder_path):
        # Допустимые расширения файлов
        if not self.consider_psd:
            valid_extensions = {'.png', '.jpeg', '.jpg', '.webp', '.jfif', '.bmp', '.tiff', '.tga'}
        elif self.consider_psd:
            valid_extensions = {'.png', '.jpeg', '.jpg', '.webp', '.jfif', '.bmp', '.tiff', '.tga', '.psd', '.psb'}
        else:
            valid_extensions = {'.png', '.jpeg', '.jpg', '.webp', '.jfif', '.bmp', '.tiff', '.tga'}
        # Список для хранения путей
        image_paths = []
        try:
            # Преобразуем путь в объект Path
            folder = Path(folder_path)
            # Проверяем существование папки
            if not folder.exists():
                raise FileNotFoundError(f"Папка {folder_path} не найдена")
            # Проходим только по файлам в указанной папке (без подпапок)
            for file_path in folder.iterdir():
                # Проверяем, что это файл (не папка) и проверяем расширение
                if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
                    # Добавляем путь в список
                    image_paths.append(str(file_path))
            image_paths = natsorted(image_paths)
            return image_paths
        except Exception as e:
            print(f"Ошибка при сканировании папки: {e}")
        return []

    def convert_image_onec_type(self, image_paths):
        converted_images = []
        for path in image_paths:
            with pil.open(path) as img:
                img_copy = img.copy()
                if img_copy.mode in ('RGBA', 'LA') or (img_copy.mode == 'P' and 'transparency' in img_copy.info):
                    img_copy = img_copy.convert('RGB')
                converted_images.append(img_copy)
        return converted_images

    def save_images(self, conv_images, progress_func):
        new_folder = str(self.save_folder_name)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        if self.do_gif == True:
            type_images_output = ".gif"
        else:
            type_images_output = ".jpeg"
        imageIndex = 1
        for image in conv_images:
            name_save = f'{new_folder}/{imageIndex:02}{type_images_output}'
            image.save(name_save, "JPEG", optimize=True, quality=self.quality_jpg)
            imageIndex += 1
        if self.save_temp_png == True:
            folder_name = os.path.basename(new_folder)
            folder_name = folder_name.replace("[GIF]", "")
            new_folder = os.path.dirname(new_folder)
            new_folder = new_folder + f"/{folder_name}[PNG]"
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            count_images = len(conv_images)
            imageIndex = 1
            for image in conv_images:
                if (progress_func != None):
                    progress_func("Работа - Сохранение Итоговых Изображений!", int(95/count_images))
                name_save = f'{new_folder}/{imageIndex:02}.png'
                image.save(name_save)
                imageIndex += 1

    def running(self, folder_path, progress_func=None):
        image_paths = self.get_images_paths(folder_path)
        conv_images = self.convert_image_onec_type(image_paths)
        self.save_images(conv_images, progress_func)
