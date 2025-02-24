import deepl

from config import get_settings

settings = get_settings()
auth_key = settings.DEEPL_API_KEY

translator = deepl.Translator(auth_key)


def translate_greek_to_russian(text):
    if text is None:
        return None
    return translator.translate_text(text, target_lang="EL").text
