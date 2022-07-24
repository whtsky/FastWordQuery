import xml.etree.ElementTree
from ..base import *


@register(["有道词典-韩语", "Youdao-Korean"])
class Youdaoko(WebService):
    def __init__(self):
        super().__init__()

    def _get_from_api(self, lang="ko"):
        url = (
            "http://dict.youdao.com/fsearch?client=deskdict"
            "&keyfrom=chrome.extension&pos=-1"
            "&doctype=xml&xmlVersion=3.2"
            "&dogVersion=1.0&vendor=unknown"
            "&appVer=3.1.17.4208"
            "&le={}&q={}"
        ).format(lang, self.quote_word)
        result = {
            "phonetic": "",
            "explains": "",
        }
        try:
            html = self.get_response(url, timeout=5)
            # showInfo(str(result))
            doc = xml.etree.ElementTree.fromstring(html)
            # fetch explanations
            explains = "<br>".join(
                [
                    node.text
                    for node in doc.findall(".//custom-translation/translation/content")
                ]
            )
            result.update({"explains": explains})
        except:
            pass
        return self.cache_this(result)

    @export(["基本释义", "Explanations"])
    def fld_explains(self):
        return (
            self.cache_result("explains")
            if self.cached("explains")
            else self._get_from_api().get("explains", "")
        )

    @with_styles(cssfile="_youdao.css", need_wrap_css=True, wrap_class="youdao")
    def _get_singledict(self, single_dict, lang="ko"):
        url = "http://m.youdao.com/singledict?q={}&dict={}&le={}&more=false".format(
            self.quote_word, single_dict, lang
        )
        try:
            html = self.get_response(url, timeout=5)
            return (
                '<div id="{}_contentWrp" class="content-wrp dict-container">'
                '<div id="{}" class="trans-container {} ">{}</div>'
                "</div>"
                '<div id="outer">'
                '<audio id="dictVoice" style="display: none"></audio>'
                "</div>"
            ).format(single_dict, single_dict, single_dict, html.decode("utf-8"))
        except:
            return ""

    @export(["网络释义", "Web translation"])
    def fld_web_trans(self):
        return self._get_singledict("web_trans")

    @export(["双语例句", "Biligual example"])
    def fld_blng_sents_part(self):
        return self._get_singledict("blng_sents_part")

    @export(["百科", "baike"])
    def fld_baike(self):
        return self._get_singledict("baike")

    @export(["汉语词典(中)", "Chinese dictionary"])
    def fld_hh(self):
        return self._get_singledict("hh")
