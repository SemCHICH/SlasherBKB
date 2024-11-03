import sqlite3


# Первичная проверка о том что базы данных вообще существуют
def first_connection():
    con = sqlite3.connect('res/data.db')
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS thispres(consider_psd_slasher TEXT, custom_width TEXT, custom_height TEXT, 
        custom_count_images TEXT, cruel_slash TEXT, ignorable_edges_pixels TEXT, type_images_output TEXT, switch_count TEXT, consider_psd_gif TEXT, 
        save_originals TEXT, quality_jpg TEXT, do_gif TEXT);"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS presets(name TEXT, consider_psd_slasher TEXT, custom_width TEXT, custom_height TEXT, 
        custom_count_images TEXT, cruel_slash TEXT, ignorable_edges_pixels TEXT, type_images_output TEXT, switch_count TEXT,
        consider_psd_gif TEXT, save_originals TEXT, quality_jpg TEXT, do_gif TEXT);"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS other(last_input TEXT);"""
    )
    con.commit()
    con.close()


CONN_DATA = sqlite3.connect('res/data.db')
TABLE_DATA = ["thispres", "presets"]


def create_first():
    cursor = CONN_DATA.cursor()

    # Проверяем количество записей
    cursor.execute("SELECT COUNT(*) FROM thispres")
    count = cursor.fetchone()[0]

    if count == 0:
        # Таблица пуста, добавляем запись
        cursor.execute("INSERT INTO thispres (consider_psd_slasher, custom_width, custom_height, custom_count_images, cruel_slash, "
                       "ignorable_edges_pixels, type_images_output, switch_count, consider_psd_gif, save_originals, quality_jpg, do_gif) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                       ("False", "0", "30000", "10", "False", "10", ".png", "True", "False", "True", "60", "True"))
        CONN_DATA.commit()

    # Проверяем количество записей
    cursor.execute("SELECT COUNT(*) FROM other")
    count = cursor.fetchone()[0]

    if count == 0:
        # Таблица пуста, добавляем запись
        cursor.execute("INSERT INTO other (last_input) VALUES (?)",
                       ("",))
        CONN_DATA.commit()


def get_settings():
    cursor = CONN_DATA.cursor()
    cursor.execute('SELECT * FROM thispres')
    record = cursor.fetchone()
    return record


def save_slasher(consider_psd_slasher, custom_width, custom_height, custom_count_images, cruel_slash, ignorable_edges_pixels, type_images_output, switch_count):
    cursor = CONN_DATA.cursor()
    cursor.execute('''
    UPDATE thispres 
    SET consider_psd_slasher = ?, custom_width = ?, custom_height = ?, custom_count_images = ?, 
    cruel_slash = ?, ignorable_edges_pixels = ?, type_images_output = ?, switch_count = ?
    ''',
    (consider_psd_slasher, custom_width, custom_height, custom_count_images, cruel_slash, ignorable_edges_pixels, type_images_output, switch_count))
    CONN_DATA.commit()


def save_gifs(consider_psd_gif, save_originals, quality_jpg, do_gif):
    cursor = CONN_DATA.cursor()
    cursor.execute('''
    UPDATE thispres 
    SET consider_psd_gif = ?, save_originals = ?, quality_jpg = ?, do_gif = ?
    ''',
                   (consider_psd_gif, save_originals, quality_jpg, do_gif))
    CONN_DATA.commit()


def save_other_settings(last_input):
    cursor = CONN_DATA.cursor()
    cursor.execute('''
        UPDATE other 
        SET last_input = ?
        ''',
                   (last_input,))
    CONN_DATA.commit()


def get_other_settings():
    cursor = CONN_DATA.cursor()
    cursor.execute('SELECT * FROM other')
    record = cursor.fetchone()
    return record



def create_template(name):
    cursor = CONN_DATA.cursor()

    (consider_psd_slasher, custom_width, custom_height, custom_count_images,
     cruel_slash, ignorable_edges_pixels, type_images_output, switch_count, consider_psd_gif, save_originals, quality_jpg, do_gif) = get_settings()

    cursor.execute("INSERT INTO presets (name, consider_psd_slasher, custom_width, custom_height, custom_count_images, cruel_slash, "
                   "ignorable_edges_pixels, type_images_output, switch_count, consider_psd_gif, save_originals, quality_jpg, do_gif) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (name, consider_psd_slasher, custom_width, custom_height, custom_count_images,
                    cruel_slash, ignorable_edges_pixels, type_images_output, switch_count, consider_psd_gif, save_originals, quality_jpg, do_gif))
    CONN_DATA.commit()


def get_all_templates():
    cursor = CONN_DATA.cursor()
    cursor.execute('SELECT * FROM presets')
    rows = cursor.fetchall()
    return rows


def delete_by_name(name):
    cursor = CONN_DATA.cursor()
    # Проверяем существование записи с указанным именем
    cursor.execute(f"SELECT * FROM presets WHERE name = ?", (name,))
    record = cursor.fetchone()

    if record:
        # Если запись существует, удаляем её
        cursor.execute(f"DELETE FROM presets WHERE name = ?", (name,))
        CONN_DATA.commit()
    else:
        pass


def set_template_to_preset(name):
    cursor = CONN_DATA.cursor()
    cursor.execute("SELECT * FROM presets WHERE name = ?", (name,))
    result = cursor.fetchone()
    (name, consider_psd_slasher, custom_width, custom_height, custom_count_images, cruel_slash,
     ignorable_edges_pixels, type_images_output, switch_count, consider_psd_gif, save_originals, quality_jpg, do_gif) = result
    save_slasher(consider_psd_slasher, custom_width, custom_height, custom_count_images, cruel_slash, ignorable_edges_pixels, type_images_output, switch_count)
    save_gifs(consider_psd_gif, save_originals, quality_jpg, do_gif)

