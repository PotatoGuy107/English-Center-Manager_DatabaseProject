"""Common UI styles for input visibility and consistency."""

# QLineEdit and QTextEdit styling
INPUT_STYLE = """
    QLineEdit, QTextEdit {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QLineEdit:focus, QTextEdit:focus {
        border: 2px solid #8b0000;
        background-color: #fff5f5;
    }
    QLineEdit::placeholder {
        color: #999;
    }
"""

# QComboBox styling
COMBO_STYLE = """
    QComboBox {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QComboBox:focus {
        border: 2px solid #8b0000;
    }
    QComboBox QAbstractItemView {
        background-color: white;
        color: #222;
        selection-background-color: #bc1823;
        selection-color: white;
    }
    QComboBox QAbstractItemView::item {
        padding: 5px 10px;
        color: #222;
    }
    QComboBox QAbstractItemView::item:hover {
        background-color: #ffecee;
        color: #bc1823;
    }
"""

# QDateEdit styling
DATE_STYLE = """
    QDateEdit {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QDateEdit:focus {
        border: 2px solid #8b0000;
        background-color: #fff5f5;
    }
    QDateEdit::drop-down {
        border: none;
        width: 25px;
    }
"""

# QSpinBox and QDoubleSpinBox styling
SPINBOX_STYLE = """
    QSpinBox, QDoubleSpinBox {
        background-color: white;
        color: #222;
        border: 2px solid #bc1823;
        border-radius: 5px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QSpinBox:focus, QDoubleSpinBox:focus {
        border: 2px solid #8b0000;
        background-color: #fff5f5;
    }
"""

# QTableWidget styling
TABLE_STYLE = """
    QTableWidget {
        background-color: white;
        color: #222;
        gridline-color: #ccc;
    }
    QTableWidget::item {
        color: #222;
        padding: 5px;
        background-color: white;
    }
    QTableWidget::item:selected {
        background-color: #bc1823;
        color: white;
    }
    QHeaderView::section {
        background-color: #bc1823;
        color: white;
        font-weight: bold;
        padding: 5px;
    }
"""

# Dialog styling
DIALOG_STYLE = """
    QDialog {
        background-color: white;
        border: 2px solid #bc1823;
    }
    QLabel {
        color: #bc1823;
        font-weight: bold;
    }
"""


def apply_input_styles(widget):
    """Apply standard input styles to a widget based on its type."""
    from PyQt6.QtWidgets import QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox
    
    if isinstance(widget, (QLineEdit, QTextEdit)):
        widget.setStyleSheet(INPUT_STYLE)
    elif isinstance(widget, QComboBox):
        widget.setStyleSheet(COMBO_STYLE)
    elif isinstance(widget, QDateEdit):
        widget.setStyleSheet(DATE_STYLE)
    elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
        widget.setStyleSheet(SPINBOX_STYLE)
