import os
from ..base import *

yahoo_download_mp3 = True


@register(["雅虎奇摩字典", "Yahoo-Dict"])
class Yahoo_Dict(WebService):
    def __init__(self):
        super().__init__()

    def _get_from_api(self):
        url = "https://tw.dictionary.search.yahoo.com/search?p={}".format(
            self.quote_word
        )
        html = self.get_response(url, timeout=10)
        soup = parse_html(html)
        result = {
            "phon": "",
            "def": "",
            "audio_url": "",
            "detail": "",
        }

        # 基本
        element = soup.find(
            "div", class_="dd cardDesign dictionaryWordCard sys_dict_word_card"
        )
        if element:
            # 音标
            tag = element.find("div", class_="compList ml-25 d-ib")
            if tag:
                result["phon"] = tag.get_text()

            # 发音
            result[
                "audio_url"
            ] = f"https://s.yimg.com/bg/dict/dreye/live/f/{self.word}.mp3"

            # 词性及中文解释
            tag = element.find("div", class_="compList mb-25 ml-25 p-rel")
            if tag:
                result["def"] = (
                    '<div class="dd cardDesign">' + str(tag.find("ul")) + "</div>"
                )

        # 释义
        tag = soup.find(
            "div",
            class_="grp grp-tab-content-explanation tabsContent tab-content-explanation tabActived",
        )
        if tag:
            result["detail"] = (
                '<div class="dd cardDesign">' + str(tag.find("ul")) + "</div>"
            )

        return self.cache_this(result)

    @with_styles(need_wrap_css=True, cssfile="_yahoo.css")
    def _css(self, val):
        return val

    @export("PHON")
    def fld_pinyin(self):
        return self._get_field("phon")

    @export("PRON")
    def fld_pron(self):
        audio_url = self._get_field("audio_url")
        if yahoo_download_mp3 and audio_url:
            filename = get_hex_name(self.unique.lower(), audio_url, "mp3")
            if os.path.exists(filename) or self.download(audio_url, filename, 5):
                return self.get_anki_label(filename, "audio")

        return ""

    @export("DEF")
    def fld_basic(self):
        val = self._get_field("def")
        if val is None or val == "":
            return ""
        return self._css(val)

    @export(["详细释义", "Detailed Interpretation"])
    def fld_detail(self):
        val = self._get_field("detail")
        if val is None or val == "":
            return ""
        return self._css(val)
