import re
import os
from ..base import *

bing_download_mp3 = True


@register(["Bing", "Bing"])
class Bing(WebService):
    def __init__(self):
        super().__init__()

    def _get_from_api(self):
        data = self.get_response(
            f"https://cn.bing.com/dict/search?q={self.quote_word}&mkt=zh-cn"
        )
        soup = parse_html(data)
        result = {
            "pronunciation": {"AmE": "", "BrE": "", "AmEmp3": "", "BrEmp3": ""},
            "def": [],
            "sams": [],
        }

        # 音
        element = soup.find("div", class_="hd_tf_lh")
        if element:
            audios = element.find_all("a")
            # 美式英标
            tag = element.find("div", class_="hd_prUS")
            if tag:
                result["pronunciation"]["AmE"] = str(tag)
                # 美音
                if audios:
                    tag = audios[0]
                    audio_url = tag.get("onclick")
                    if audio_url:
                        result["pronunciation"]["AmEmp3"] = "".join(
                            re.findall(r"https://.*\.mp3", audio_url)
                        )

            # 英式音标
            tag = element.find("div", class_="hd_pr")
            if tag:
                result["pronunciation"]["BrE"] = str(tag)
                # 英音
                if audios:
                    tag = audios[1]
                    audio_url = tag.get("onclick")
                    if audio_url:
                        result["pronunciation"]["BrEmp3"] = "".join(
                            re.findall(r"https://.*\.mp3", audio_url)
                        )

        # 释义
        element = soup.find("div", class_="qdef")
        if element:
            element = getattr(element, "ul", "")
            if element:
                result["def"] = "".join([str(content) for content in element.contents])

        # 例句
        element = soup.find("div", id="sentenceSeg")
        if element:
            # 英文例句
            tags = element.find_all("div", {"class": "sen_en"})
            result["sams"] = [{"eng": "".join(tag.find_all(text=True))} for tag in tags]
            # 例句翻译
            tags = element.find_all("div", {"class": "sen_cn"})
            for i, tag in enumerate(tags):
                result["sams"][i]["chn"] = "".join(tag.find_all(text=True))

        return self.cache_this(result)

    @with_styles(
        css=".pos{font-weight:bold;margin-right:4px;}",
        need_wrap_css=True,
        wrap_class="bing",
    )
    def _css(self, val):
        return val

    @export("AME_PHON")
    def fld_phonetic_us(self):
        seg = self._get_field("pronunciation")
        return seg.get("AmE", "") if seg else ""

    @export("BRE_PHON")
    def fld_phonetic_uk(self):
        seg = self._get_field("pronunciation")
        return seg.get("BrE", "") if seg else ""

    def _fld_mp3(self, fld):
        seg = self._get_field("pronunciation")
        audio_url = seg[fld] if seg else ""
        if bing_download_mp3 and audio_url:
            filename = get_hex_name("bing", audio_url, "mp3")
            if os.path.exists(filename) or self.net_download(filename, audio_url):
                return self.get_anki_label(filename, "audio")
        return ""

    @export("AME_PRON")
    def fld_mp3_us(self):
        return self._fld_mp3("AmEmp3")

    @export("BRE_PRON")
    def fld_mp3_uk(self):
        return self._fld_mp3("BrEmp3")

    @export("DEF")
    def fld_definition(self):
        val = self._get_field("def")
        if val == None or val == "":
            return ""
        return self._css(val)

    @export("EXAMPLE")
    def fld_samples(self):
        max_numbers = 10
        segs = self._get_field("sams")
        if segs:
            sentences = ""
            for i, seg in enumerate(segs):
                sentences += """<li><div class="se_li1">
                                <div class="sen_en">{}.{}</div>
                                <div class="sen_cn">{}</div>
                            </div></li>""".format(
                    i + 1, seg["eng"], seg["chn"]
                )
                if i == 9:
                    break
            if sentences:
                return """<div class="se_div">
                                <div class="sentenceCon">
                                    <div id="sentenceSeg"><ol>{}</ol></div>
                                </div>
                        </div>""".format(
                    sentences
                )
        return ""
