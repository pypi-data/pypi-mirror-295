from PyQt6.QtWidgets import QWidget, QCheckBox, QLabel, QDialog, QPushButton, QTableWidget


def path(widget: QWidget):
    return Path([widget])


class Path:
    def __init__(self, widgets: list[QWidget]) -> None:
        self.widgets: list[QWidget] = widgets

    def get(self, index: int = 0) -> QWidget:
        return self.widgets[index]

    def checkbox(self, index: int = 0):
        return self.child(QCheckBox, index)

    def label(self, index: int = 0):
        return self.child(QLabel, index)

    def dialog(self, index: int = 0):
        return self.child(QDialog, index)

    def button(self, index: int = 0):
        return self.child(QPushButton, index)

    def table(self, index: int = 0):
        return self.child(QTableWidget, index)

    def child(self, clazz: type[QWidget], index: int):
        return Path([self.widgets[0].findChildren(clazz)[index]])
