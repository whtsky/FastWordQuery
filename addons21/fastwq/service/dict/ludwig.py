import random
from ..base import *

oxford_download_mp3 = True


@register("Ludwig")
class Ludwig(WebService):
    def __init__(self):
        super().__init__()

    def _get_from_api(self):
        data = self.get_response(f"https://ludwig.guru/s/{self.quote_word}")
        soup = parse_html(data)
        result = {"def": "", "examples": []}

        # def
        element = soup.find("div", class_="-id-__definition--1E88I")
        if element:
            e_list = element.find_all("p")
            if e_list:
                result["def"] = "".join(str(c) for c in e_list)

        # examples
        e_list = soup.find_all("p", class_="-id-__exact--SVDfq")
        if e_list:
            e_arr = []
            for n in e_list:
                e_arr.append(str(n.get_text()))
            result["examples"] = e_arr
        return self.cache_this(result)

    @export("DEF")
    def fld_definate(self):
        return self._get_field("def")

    @export("EXAMPLE")
    def fld_example(self):
        return self._range_examples([i for i in range(0, 100)])

    @export(["随机例句", "Random example"])
    def fld_random_example(self):
        return self._range_examples()

    @export(["首2个例句", "First 2 examples"])
    def fld_first2_example(self):
        return self._range_examples([0, 1])

    def _range_examples(self, range_arr=None):
        maps = self._get_field("examples")
        if maps:
            range_arr = (
                range_arr if range_arr else [random.randrange(0, len(maps) - 1, 1)]
            )
            my_str = ""
            for i, n in enumerate(maps):
                if i in range_arr:
                    my_str += f"<li>{n}</li>"
            return f"<ul>{my_str}</ul>"
        return ""
