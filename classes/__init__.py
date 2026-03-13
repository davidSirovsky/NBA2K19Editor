# Инициализация пакета classes
# Экспортируем все классы UI элементов для удобного импорта

from .base_element import BaseElement
from .frame import Frame
from .button import TextButton
from .close_button import CloseButton
from .minimize_button import MinimizeButton
from .copy_dna_button import CopyDNAButton
from .text_input import TextInput
from .context_menu import ContextMenu
from .checkbox import Checkbox
from .scrollbar import Scrollbar
from .text_field import TextField
from .button_ribbon import ButtonRibbon
from .window import Window

# Список всех экспортируемых классов
__all__ = [
    'BaseElement',
    'Frame',
    'TextButton',
    'CloseButton',
    'MinimizeButton',
    'CopyDNAButton',
    'TextInput',
    'ContextMenu',
    'Checkbox',
    'Scrollbar',
    'TextField',
    'ButtonRibbon',
    'Window'
]