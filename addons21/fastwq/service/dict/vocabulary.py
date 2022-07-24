import random
from ..base import *


@register("Vocabulary.com")
class Vocabulary(WebService):
    def __init__(self):
        super().__init__()

    def _get_from_api(self):
        data = self.get_response(
            f"https://www.vocabulary.com/dictionary/{self.quote_word}"
        )
        soup = parse_html(data)
        result = {
            "short": "",
            "long": "",
        }

        # short
        element = soup.find("p", class_="short")
        if element:
            result["short"] = "".join(str(e) for e in element.contents)

        # long
        element = soup.find("p", class_="long")
        if element:
            result["long"] = "".join(str(e) for e in element.contents)

        return self.cache_this(result)

    @export(["简短释义", "Short definition"])
    def fld_definate(self):
        return self._get_field("short")

    @export(["详细释义", "Long definition"])
    def fld_example(self):
        return self._get_field("long")
