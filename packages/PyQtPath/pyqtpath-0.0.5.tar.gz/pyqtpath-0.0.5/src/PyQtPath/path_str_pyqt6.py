from types import ModuleType
from typing import Optional
import importlib

from PyQt6.QtWidgets import QWidget


def child(widget: QWidget, path: str) -> Optional:
    if widget is None or path is None or len(path) == 0:
        return None
    normalized_path: list[(type[QWidget], int)] = __normalize_path(path)
    return __nested_child(widget, normalized_path)


def __nested_child(widget: QWidget, path: list[(type[QWidget], int)]) -> Optional:
    current_widget: QWidget = widget
    for part in path:
        clazz: type[QWidget] = part[0]
        index: int = part[1]
        children: list[QWidget] = current_widget.findChildren(clazz)
        if len(children) == 0:
            return None
        current_widget = children[index]
    return current_widget


def __normalize_path(path: str) -> list[(type[QWidget], int)]:
    if path is None or len(path) == 0:
        return []
    parts: list[str] = path.split("/")
    for i, part in enumerate(parts):
        if part.isdigit():
            continue
        next_part: str = parts[i + 1] if i < len(parts) - 1 else None
        module: ModuleType = importlib.import_module("PyQt6.QtWidgets")
        clazz: type[QWidget] = getattr(module, part)
        if next_part is not None and next_part.isdigit():
            yield clazz, int(next_part)
        else:
            yield clazz, 0
