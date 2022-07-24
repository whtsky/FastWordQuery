from ..base import *
from .cambridge import Cambridge


@register(["剑桥词典-英英", "Cambridge(English)"])
class CambridgeEE(Cambridge):
    def __init__(self):
        super().__init__()

    def _get_url(self):
        return "https://dictionary.cambridge.org/dictionary/english/"
