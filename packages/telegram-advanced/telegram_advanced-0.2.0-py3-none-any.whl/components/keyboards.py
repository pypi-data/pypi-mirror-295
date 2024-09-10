# components/keyboards.py
from ..api.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_inline_keyboard(buttons):
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            keyboard_row.append(InlineKeyboardButton(**button))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)