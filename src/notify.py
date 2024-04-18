import requests
import yaml


class Ntfy:
    def __init__(self) -> None:
        with open('config.yml', 'r', encoding='utf-8') as file:
            cfg = yaml.safe_load(file)
            self.access_token = cfg['ntfy']['token']
            self.url = cfg['ntfy']['url']

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
