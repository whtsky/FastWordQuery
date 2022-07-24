import re

from aqt.utils import showInfo, showText
from ..base import LocalService, export, register, with_styles

path = "D:\\dicts\\LDOCE\\d.txt"


@register("txt测试")
class TxtTest(LocalService):
    def __init__(self):
        super().__init__(path)
        try:
            self.handle = open(path, "rb")
        except:
            self.handle = None

    @export("all")
    def fld_phonetic(self):
        if not self.handle:
            return
        for line in self.handle:
            line = line.decode("UTF-8")
            m = re.search(self.word, line)
            if m:
                return line
