import base64
import os
import re
import urllib.request as urllib2

from ..base import *

css = ""
eudict_download_mp3 = True


@register(["欧路词典", "eudict"])
class Eudict(WebService):
    def __init__(self):
        super().__init__()

    def _get_from_api(self):
        url = f"http://dict.eudic.net/mdicts/en/{self.quote_word}"
        try:
            result = {}
            html = self.get_response(url, timeout=5)
            soup = parse_html(html)

            def _get_from_element(dict, key, soup, tag, id=None, class_=None):
                baseURL = "http://dict.eudic.net/"
                # element = soup.find(tag, id=id, class_=class_)  # bs4
                if id:
                    element = soup.find(tag, {"id": id})
                if class_:
                    element = soup.find(tag, {"class": class_})
                if element:
                    dict[key] = str(element)
                    dict[key] = re.sub(r'href="/', 'href="' + baseURL, dict[key])
                    dict[key] = re.sub(r"声明：.*。", "", dict[key])
                    dict[key] = dict[key]
                return dict

            def _sentence_audio(soup, tag, class_):
                el_list = soup.findAll(tag, {"class": class_})
                if el_list:
                    url = "https://api.frdic.com/api/v2/speech/speakweb?langid=ting&voicename={0}&txt=QYN{1}"
                    maps = []
                    for element in el_list:
                        # 例句
                        i_str = str(element)
                        m = element.find("div", {"class": "content"})
                        if m:
                            # i_str = str(m)
                            # 声音
                            sound = url.format(
                                element.get("source"),
                                urllib2.quote(base64.b64encode(m.text.encode("utf-8"))),
                            )
                            maps.append([sound, i_str])
                my_str = ""
                for i, e in enumerate(maps):
                    i_str = e[1]
                    sound = e[0]
                    mp3 = self._fld_mp3(sound)
                    my_str = my_str + "<li>" + i_str + " " + mp3 + "</li>"
                return my_str

            result = _get_from_element(
                result, "phonitic", soup, "span", class_="Phonitic"
            )
            result = _get_from_element(
                result, "fccf", soup, "div", id="FCChild"
            )  # 西汉-汉西词典
            result = _get_from_element(
                result, "example", soup, "div", id="LJChild"
            )  # 西语例句库
            result = _get_from_element(
                result, "syn", soup, "div", id="SYNChild"
            )  # 近义、反义、派生词典
            result = _get_from_element(result, "ff", soup, "div", id="FFChild")  # 西西词典
            result["oexample"] = _sentence_audio(soup, "div", class_="lj_item")  # 原声例句

            return self.cache_this(result)
        except Exception as e:
            return {}

    def _fld_mp3(self, audio_url):
        if eudict_download_mp3 and audio_url:
            filename = get_hex_name("eudict", audio_url, "mp3")
            if os.path.exists(filename) or self.net_download(filename, audio_url):
                return self.get_anki_label(filename, "audio")
        return ""

    @export(["真人发音", "Real person pronounciation"])
    def fld_sound(self):
        url = "https://api.frdic.com/api/v2/speech/speakweb?langid=es&txt=QYN{word}".format(
            word=urllib2.quote(base64.b64encode(self.word.encode("utf-8")))
        )
        filename = get_hex_name(self.unique.lower(), url, "mp3")
        if os.path.exists(filename) or self.net_download(filename, url):
            return self.get_anki_label(filename, "audio")
        return ""

    @export("PHON")
    def fld_phonetic(self):
        return self._get_field("phonitic")

    @export(["英汉-汉英词典", "English-chinese/Chinese-english"])
    @with_styles(need_wrap_css=True, cssfile="_eudict.css")
    def fld_fccf(self):
        return self._get_field("fccf")

    @export(["英语例句库", "English examples"])
    @with_styles(need_wrap_css=True, cssfile="_eudict.css")
    def fld_example(self):
        return self._get_field("example")

    @export(["近义词词典", "Synonyms"])
    def fld_syn(self):
        return self._get_field("syn")

    @export(["英英词典", "English-english"])
    @with_styles(need_wrap_css=True, cssfile="_eudict.css")
    def fld_ff(self):
        return self._get_field("ff")

    @export(["原声例句", "Original examples"])
    @with_styles(need_wrap_css=True, cssfile="_eudict.css")
    def fld_oexample(self):
        return self._get_field("oexample")
