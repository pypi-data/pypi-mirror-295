# utils/localization.py
import gettext
import os

class Localization:
    def __init__(self, locale_dir):
        self.locale_dir = locale_dir
        self.translations = {}

    def load_language(self, language):
        if language not in self.translations:
            try:
                translation = gettext.translation('messages', localedir=self.locale_dir, languages=[language])
                self.translations[language] = translation.gettext
            except FileNotFoundError:
                print(f"Translation file for {language} not found. Using default language.")
                self.translations[language] = lambda x: x

    def get_text(self, key, language):
        if language not in self.translations:
            self.load_language(language)
        return self.translations[language](key)

# Usage example:
# localization = Localization('path/to/locale/directory')
# print(localization.get_text('welcome_message', 'es'))