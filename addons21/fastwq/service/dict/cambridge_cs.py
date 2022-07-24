from ..base import *
from .cambridge import Cambridge


@register(["剑桥词典-英汉简", "Cambridge(英汉简)"])
class CambridgeCS(Cambridge):
    def __init__(self):
        super().__init__()

    def _get_url(self):
        return (
            "https://dictionary.cambridge.org/us/dictionary/english-chinese-simplified/"
        )
