import requests
from hardverapro_pp.utils.config import Config

class Ntfy:
    def __init__(self) -> None:
        cfg = Config()
        self.access_token = cfg.key('ntfy').key('token').str()
        self.url = cfg.key('ntfy').key('url').str()

    def push(self, topic: str, title: str, message: str, tags: str, url: str, thumbnail: str, icon: str) -> int:
        push = requests.post(self.url + '/' + topic, data=message.encode('utf-8'),
                             headers={
                                 'Authorization': 'Bearer ' + self.access_token,
                                 'Title': title.encode('utf-8'),
                                 'Tags': tags.encode('utf-8'),
                                 'Attach': thumbnail,
                                 'Actions': f'view, HardverApró, {url}'.encode('utf-8'),
                                 'Click': url,
                                 'Icon': icon,
                             })

        return push.status_code == 200
