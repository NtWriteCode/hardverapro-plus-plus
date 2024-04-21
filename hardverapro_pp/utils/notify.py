import requests
from typing import Optional
from hardverapro_pp.utils.config import Config


class Ntfy:
    def __init__(self) -> None:
        cfg = Config()
        self._access_token = cfg.key("ntfy").key("token").str("")
        self._base_url = cfg.key("ntfy").key("url").str()

    def push(
        self,
        topic: str,
        title: Optional[str],
        message: str,
        tags: Optional[str],
        url: Optional[str],
        thumbnail: Optional[str],
        icon: Optional[str],
    ) -> bool:
        headers: dict[str, str] = {}

        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        if title:
            headers["Title"] = title
        if tags:
            headers["Tags"] = tags
        if thumbnail:
            headers["Attach"] = thumbnail
        if url:
            headers["Actions"] = f"view, HardverApró, {url}"
            headers["Click"] = url
        if icon:
            headers["Icon"] = icon

        push = requests.post(self._base_url + "/" + topic, data=message, headers=headers)

        return push.status_code == 200
