from ..base import *
from .cambridge import Cambridge


@register(["剑桥词典-英汉繁", "Cambridge(英汉繁)"])
class CambridgeCT(Cambridge):
    def __init__(self):
        super().__init__()

    def _get_url(self):
        return "https://dictionary.cambridge.org/us/dictionary/english-chinese-traditional/"
