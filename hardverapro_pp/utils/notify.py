from typing import Optional

import requests

from hardverapro_pp.utils.config import Config


class Ntfy:
    def __init__(self) -> None:
        config = Config()
        self._access_token = config.key("ntfy").key("token").str("")
        self._base_url = config.key("ntfy").key("url").str()
        self._timeout = config.key("network").key("requests-timeout").int(10)

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

        push = requests.post(self._base_url + "/" + topic, data=message, headers=headers, timeout=self._timeout)

        return push.status_code == 200
