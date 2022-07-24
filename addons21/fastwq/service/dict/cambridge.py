import os
import re

from bs4 import Tag

from ..base import *

cambridge_url_base = "https://dictionary.cambridge.org/"
cambridge_download_mp3 = True
cambridge_download_img = True


class Cambridge(WebService):
    def __init__(self):
        super().__init__()

    def _get_url(self):
        return cambridge_url_base

    def _get_from_api(self):
        data = self.get_response(f"{self._get_url()}{self.quote_word}")
        soup = parse_html(data)
        result = {
            "pronunciation": {"AmE": "", "BrE": "", "AmEmp3": "", "BrEmp3": ""},
            "image": "",
            "thumb": "",
            "def": "",
            "def_list": [],
        }

        # english
        page = "page" if type(self).__name__ == "CambridgeEE" else "di-body"
        element = soup.find("div", class_=page)
        if element:
            # 页
            elements = element.find_all("div", class_="entry-body__el")
            header_found = False
            for element in elements:
                if element:
                    # 音
                    if not header_found:
                        header = element.find("div", class_="pos-header")
                        if header:
                            tags = header.find_all("span", class_="dpron-i")
                            if tags:
                                for tag in tags:
                                    r = tag.find("span", class_="region")
                                    reg = r.get_text() if r else ""
                                    pn = "AmE" if reg == "us" else "BrE"
                                    p = tag.find("span", class_="pron")
                                    result["pronunciation"][pn] = (
                                        p.get_text() if p else ""
                                    )
                                    snd = tag.find("source", type="audio/mpeg")
                                    if snd:
                                        result["pronunciation"][
                                            pn + "mp3"
                                        ] = cambridge_url_base + snd.get("src")
                                    header_found = True

                    # 义
                    senses = element.find_all("div", class_="pos-body")
                    # 词性
                    span_posgram = element.find("div", class_="posgram")
                    pos_gram = span_posgram.get_text() if span_posgram else ""

                    if senses:
                        for sense in senses:
                            # 像ambivalent之类词语含有ambivalence解释，词性不同
                            runon_title = None
                            if sense["class"][0] == "runon":
                                runon_pos = sense.find("span", class_="pos")
                                runon_gram = sense.find("span", class_="gram")
                                if runon_pos is not None:
                                    pos_gram = runon_pos.get_text() + (
                                        runon_gram.get_text() if runon_gram else ""
                                    )
                                h3_rt = sense.find("h3", class_="runon-title")
                                runon_title = h3_rt.get_text() if h3_rt else None

                            sense_body = sense.find(
                                "div",
                                class_=re.compile("sense-body|runon-body pad-indent"),
                            )

                            if sense_body:
                                l = result["def_list"]

                                def extract_sense(block, phrase=None):
                                    if isinstance(block, Tag) is not True:
                                        return

                                    block_type = block["class"][0]
                                    if block_type == "def-block":
                                        pass
                                    elif block_type == "phrase-block":
                                        _phrase_header = block.find(
                                            "span", class_="phrase-head"
                                        )
                                        _phrase_body = block.find(
                                            "div", class_="phrase-body pad-indent"
                                        )
                                        if _phrase_body:
                                            for p_b in _phrase_body:
                                                extract_sense(
                                                    p_b,
                                                    _phrase_header.get_text()
                                                    if _phrase_header
                                                    else None,
                                                )
                                        return
                                    elif block_type == "runon-body":
                                        pass
                                    else:
                                        return

                                    span_df = block.find("span", class_="def-info")
                                    def_info = (
                                        span_df.get_text().replace("›", "")
                                        if span_df
                                        else ""
                                    )
                                    d = block.find("div", class_="def")
                                    tran = block.find("span", class_="trans")
                                    examps = block.find_all(
                                        "div", class_="examp dexamp"
                                    )
                                    l.append(
                                        "<li>{}{}{}{}{} {}{}</li>".format(
                                            '<span class="epp-xref">{}</span>'.format(
                                                pos_gram
                                            )
                                            if pos_gram != ""
                                            else "",
                                            '<span class="epp-xref">{}</span>'.format(
                                                runon_title
                                            )
                                            if runon_title
                                            else "",
                                            '<span class="epp-xref">{}</span>'.format(
                                                phrase
                                            )
                                            if phrase
                                            else "",
                                            '<span class="epp-xref">{}</span>'.format(
                                                def_info
                                            )
                                            if def_info.strip() != ""
                                            else "",
                                            f'<b class="def">{d.get_text()}</b>'
                                            if d
                                            else "",
                                            '<span class="trans">{}</span>'.format(
                                                tran.get_text()
                                            )
                                            if tran
                                            else "",
                                            "".join(
                                                '<div class="examp">{}</div>'.format(
                                                    e.get_text()
                                                )
                                                if e
                                                else ""
                                                for e in examps
                                            ),
                                        )
                                    )

                                for b in sense_body:
                                    extract_sense(b)
                                result["def"] = "<ul>" + "".join(s for s in l) + "</ul>"
                                img = sense.find("img", class_="lightboxLink")
                                if img:
                                    result["image"] = cambridge_url_base + img.get(
                                        "data-image"
                                    )
                                    result["thumb"] = cambridge_url_base + img.get(
                                        "src"
                                    )

        return self.cache_this(result)

    @with_styles(need_wrap_css=True, cssfile="_cambridge.css")
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

    def _fld_img(self, fld):
        image_url = self._get_field(fld)
        if cambridge_download_img and image_url:
            filename = get_hex_name(self.unique.lower(), image_url, "jpg")
            if os.path.exists(filename) or self.net_download(filename, image_url):
                return self.get_anki_label(filename, "img")
        return ""

    def _fld_mp3(self, fld):
        audio_url = self._get_field("pronunciation")[fld]
        if cambridge_download_mp3 and audio_url:
            filename = get_hex_name(self.unique.lower(), audio_url, "mp3")
            if os.path.exists(filename) or self.net_download(filename, audio_url):
                return self.get_anki_label(filename, "audio")
        return ""

    @export("IMAGE")
    def fld_image(self):
        return self._fld_img("image")

    @export(["缩略图", "Thumbnails"])
    def fld_thumbnail(self):
        return self._fld_img("thumb")

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
