import requests
from datetime import datetime
from bs4 import BeautifulSoup, element
from hardverapro_pp.utils.config import Config
from hardverapro_pp.core.ha_item import HardveraproItem


class HardveraproParser:
    def __init__(self, config: Config, content: str) -> None:
        self._content = content
        self._soup = BeautifulSoup(content, "html.parser")
        self._timeout = config.key("network").key("requests-timeout").int(10)

    def _get_price(self, li: element.Tag) -> str:
        default_value = "? Ft"

        media_body = li.find("div", class_="media-body")
        if type(media_body) is element.Tag:
            uad_info = media_body.find("div", class_="uad-info")
            if type(uad_info) is element.Tag:
                uad_price = uad_info.find("div", class_="uad-price")
                if uad_price:
                    return uad_price.getText()
        return default_value

    def _get_title(self, li: element.Tag) -> str:
        default_value = "Ismeretlen termék"

        media_body = li.find("div", class_="media-body")
        if type(media_body) is element.Tag:
            uad_info = media_body.find("div", class_="uad-title")
            if type(uad_info) is element.Tag:
                link = uad_info.find("a")
                if link:
                    return link.getText()
        return default_value

    def _get_url(self, li: element.Tag) -> str:
        default_value = "https://hardverapro.hu/index.html"

        media_body = li.find("div", class_="media-body")
        if type(media_body) is element.Tag:
            uad_info = media_body.find("div", class_="uad-title")
            if type(uad_info) is element.Tag:
                link = uad_info.find("a")
                if type(link) is element.Tag:
                    return str(link.get("href"))
        return default_value

    def _get_thumbnail(self, li: element.Tag) -> str:
        default_value = "https://cdn.rios.hu/dl/uad/noimage.png"

        img = li.find("img")
        if type(img) is element.Tag:
            raw_url = str(img["data-retina-url"])
            return f"https:{raw_url}" if raw_url.startswith("/") else raw_url
        return default_value

    def _get_author(self, li: element.Tag) -> str:
        default_value = "Ismeretlen feltöltő"

        media_body = li.find("div", class_="media-body")
        if type(media_body) is element.Tag:
            uad_misc = media_body.find("div", class_="uad-misc")
            if type(uad_misc) is element.Tag:
                link = uad_misc.find("a")
                if link:
                    return link.getText()
        return default_value

    def _get_date(self, li: element.Tag, url: str) -> str:
        default_value = datetime.now().strftime(r"%Y-%m-%d %H:%M")

        media_body = li.find("div", class_="media-body")
        if type(media_body) is element.Tag:
            time = media_body.find("time")
            if type(time) is element.Tag:
                time_extracted = time.getText()
                if "előresorolt" not in time_extracted.lower() and "hirdetés" not in time_extracted.lower():
                    return time_extracted

        # Make a second request to the item's URL and retrieve the date from there
        try:
            response = requests.get(url, timeout=self._timeout)
            if response and response.status_code == 200:
                content = response.content.decode("utf-8")
                soup = BeautifulSoup(content, "html.parser")
                span = soup.find("span", title="Feladás időpontja")

                if type(span) is element.Tag:
                    return span.getText().strip()
        except:  # nosec B110
            pass
        return default_value

    def _get_reputation(self, li: element.Tag) -> str:
        default_value = "0"

        media_body = li.find("div", class_="media-body")
        if type(media_body) is element.Tag:
            uad_misc = media_body.find("div", class_="uad-misc")
            if type(uad_misc) is element.Tag:
                uad_rating = uad_misc.find("span", class_="uad-rating")
                if type(uad_rating) is element.Tag:
                    return uad_rating.getText()
        return default_value

    def get_items(self) -> list[HardveraproItem]:
        default_value: list[HardveraproItem] = []
        if "Sajnos a megadott keresési feltételekkel nincs egy találat sem." in self._content:
            return default_value

        uad_list_div = self._soup.find("div", class_="uad-list")
        if type(uad_list_div) is not element.Tag:
            return default_value

        ul_list = uad_list_div.find("ul", class_="list-unstyled")
        if type(ul_list) is not element.Tag:
            return default_value

        li_elements = ul_list.find_all("li", class_="media")
        if not li_elements:
            return default_value

        items = []
        for li in li_elements:
            item = HardveraproItem(
                self._get_title(li),
                self._get_price(li),
                self._get_url(li),
                self._get_thumbnail(li),
                self._get_author(li),
                None,
                self._get_reputation(li),
            )
            item.upload_date = self._get_date(li, item.url)

            items.append(item)
        return items
