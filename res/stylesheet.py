# from qdarktheme import load_stylesheet

style_for_temp = """
QPushButton {
    color: rgb(237, 239, 255);
    border-radius: 3%;
    padding: 4px;
    font-size: 14px;
    background: rgba(240, 51, 107, 1);
}
QPushButton:!window {
    color: rgb(237, 239, 255);
    background: rgba(240, 51, 107, 1);
}
QPushButton:default {
    color: #0f0f0f;
    background: #43e689;
}
QPushButton:hover,
QPushButton:flat:hover {
    background: rgba(68, 16, 145, 0.666);
}
QPushButton:pressed,
QPushButton:flat:pressed,
QPushButton:checked:pressed,
QPushButton:flat:checked:pressed {
    background: rgba(68, 16, 145, 0.333);
}
QPushButton:checked,
QPushButton:flat:checked {
    background: rgba(68, 16, 145, 0.933);
}
QPushButton:default:hover {
    background: rgba(68, 16, 145, 0.666);
}
QPushButton:default:pressed {
    background: rgba(68, 16, 145, 0.333);
}
QPushButton:default:disabled {
    background: #747a80;
}
"""


FONT_SIZE = "14px"
BACK_COLOUR = "#0f0f0f"
BORDER_COLOUR = "#666c71"

LIGHT_STYLE_SHEET = f"""

* {{
    font-family: Inter;
}}

QLabel {{
    font-size: {FONT_SIZE};
}}

QCheckBox {{
    min-height: 1.1em;
    font-size: {FONT_SIZE};
}}
QTabWidget::pane {{
    font-size: {FONT_SIZE};
}}

QGroupBox {{
    border: 1px solid {BORDER_COLOUR};
    border-radius: 3%;
    font-weight: 500;
    font-size: {FONT_SIZE};
    margin-top: 1.1em;
    padding: 1px;
}}

QGroupBox::title {{
    top: -9px;
    left: 8px;
}}



QWidget {{
    background: {BACK_COLOUR};
    color: #edefff;
    selection-color: {BACK_COLOUR};
}}
QWidget:item:selected,
QWidget:item:checked
{{
    background: rgb(68, 16, 145);
    color: {BACK_COLOUR};
}}



QTabWidget::tab-bar {{
    left: 10px; /* позиционирование относительно левого края */
}}


QTabBar {{
    font-size: {FONT_SIZE};
    width: 14px;
    height: 14px;
    margin-left: 100px;
}}
QTabBar::tab {{
    color: #c0c0c0;
    background: #1a1a1a;
    margin-right: 5px;
    padding: 5px;
    border: 1px solid #5b5b5b;
    border-radius: 3%;
}}
QTabBar::tab:hover {{
    background: rgba(68, 16, 145, 0.666);
}}
QTabBar::tab:selected {{
    color: rgb(237, 239, 255);
    background: rgba(68, 16, 145, 0.333);
}}
QTabBar::tab:selected:disabled {{
    background: {BORDER_COLOUR};
    color: #babdc2;
}}


QPushButton {{
    font-size: 13px;
    border-radius: 3%;
    color: rgb(237, 239, 255);
    padding: 2px;
    background: rgba(240, 51, 107, 1);
    padding-left: 10px;
    padding-right: 10px;
    padding: 2px;
    min-height: 1.2em;
}}
QPushButton:!window {{
    color: rgb(237, 239, 255);
    background: rgba(240, 51, 107, 1);
}}
QPushButton:default {{
    color: {BACK_COLOUR};
    background: #43e689;
}}
QPushButton:hover,
QPushButton:flat:hover {{
    background: rgba(68, 16, 145, 0.666);
}}
QPushButton:pressed,
QPushButton:flat:pressed,
QPushButton:checked:pressed,
QPushButton:flat:checked:pressed {{
    background: rgba(68, 16, 145, 0.333);
}}
QPushButton:checked,
QPushButton:flat:checked {{
    background: rgba(68, 16, 145, 0.933);
}}
QPushButton:default:hover {{
    background: rgba(68, 16, 145, 0.666);
}}
QPushButton:default:pressed {{
    background: rgba(68, 16, 145, 0.333);
}}
QPushButton:default:disabled {{
    background: {BORDER_COLOUR};
}}


QLineEdit {{
    padding: 2px;
    border: 1px solid {BORDER_COLOUR};
    border-radius: 3%;
    font-size: {FONT_SIZE};
    width: 90%;
    min-height: 1.1em;
}}
QLineEdit:focus {{
    border-radius: 3%;
    border: 1px solid rgba(240, 51, 107, 1);
    color: rgba(240, 51, 107, 1);
}}

QTextEdit:focus,
QTextEdit:selected,
QPlainTextEdit:focus,
QPlainTextEdit:selected {{
    border-radius: 3%;
    border: 1px solid rgba(240, 51, 107, 1);
    selection-background-color: rgb(68, 16, 145);
}}


QComboBox {{
    padding: 2px;
    border: 1px solid {BORDER_COLOUR};
    border-radius: 3%;
    font-size: {FONT_SIZE};
    width: 90%;
    min-height: 1.1em;
    background: rgba(255.000, 255.000, 255.000, 0.000);
}}
QComboBox:focus,
QComboBox:open {{
    border: 1px solid rgba(240, 51, 107, 1);
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 4px;
}}
QComboBox::down-arrow {{
        width: 8px;
        height: 8px;
        border: 2px solid #666;
        border-top: none;
        border-left: none;
        transform: rotate(45deg);
        margin-top: 0px;
}}
QComboBox::item:selected {{
    border: none;
    background: rgb(68, 16, 145);
    color: {BACK_COLOUR};
}}
QComboBox QAbstractItemView {{
    background: {BACK_COLOUR};
    border: 1px solid {BORDER_COLOUR};
    selection-background-color: rgb(68, 16, 145);
    selection-color: #edefff;
}}

QProgressBar {{
    font-size: {FONT_SIZE};
    border: 1px solid grey;
    border-radius: 3%;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: #e91e63;
    width: 1px;
    margin: 0px;
    spacing: 0px;
}}


QCheckBox::indicator:checked,
QAbstractItemView::indicator:checked {{
    border-radius: 3%;
    min-height: 1.1em;
    border: 1px solid #f0336b;
    background-color: #f0336b;
}}
QCheckBox::indicator:checked::hover,
QAbstractItemView::indicator:checked::hover {{
    border-radius: 3%;
    min-height: 1.1em;
    border: 1px solid #441091;
    background-color: #441091;
}}
QCheckBox::indicator:checked::focus,
QAbstractItemView::indicator:checked::focus {{
    border-radius: 3%;
    min-height: 1.1em;
    border: 1px solid #441091;
    background-color: #441091;
}}


QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border-radius: 3%;
    border: 1px solid #5b5b5b;
    background-color: #1a1a1a;
}}
QCheckBox::indicator:hover {{
    border: 1px solid #666666;
}}
QCheckBox::indicator:unchecked {{
    background-color: #1a1a1a;
}}
QCheckBox::indicator:unchecked:hover {{
    background-color: #262626;
}}

"""


def load_styling():
    return LIGHT_STYLE_SHEET
