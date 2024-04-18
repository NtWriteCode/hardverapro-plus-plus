import yaml
import time
import schedule
from notify import Ntfy
from ha_query import HardveraproQuery
from ha_item import HardveraproItem
from ha_parser import HardveraproParser
from item_database import ItemDatabase


def get_queries() -> list[tuple[HardveraproQuery, str]]:
    queries = []
    with open('config.yml', 'r', encoding='utf-8') as file:
        cfg = yaml.safe_load(file)
        default_topic = cfg['ntfy']['default-topic']
        for item in cfg['item-urls']:
            topic = default_topic
            if 'topic' in item:
                topic = item['topic']
            queries.append((HardveraproQuery(item), topic))

    return queries


def generate_hapro_item_ntfy(ntfy: Ntfy, item: HardveraproItem, topic: str):
    tags = 'rotating_light'
    icon = 'https://cdn.rios.hu/design/ha/logo-compact.png'
    ntfy.push(topic, item.title, f'Ára: {item.price}, {item.upload_date}-kor új terméket rakott fel {item.seller} ({item.reputation}) tag', tags, item.url, item.thumbnail, icon)


def crawl(queries: list[tuple[HardveraproQuery, str]], ntfy: Ntfy):
    for query, topic in queries:
        content = query.make_query()
        parser = HardveraproParser(content)
        items = parser.get_items()
        itemdb = ItemDatabase(query)

        for item in items:
            if not itemdb.exists(item):
                if not itemdb.is_new_database():
                    generate_hapro_item_ntfy(ntfy, item, topic)
                itemdb.insert(item)


def get_schedule_interval():
    with open('config.yml', 'r', encoding='utf-8') as file:
        cfg = yaml.safe_load(file)
        return cfg['re-check']


if __name__ == "__main__":
    interval = get_schedule_interval()
    queries = get_queries()
    ntfy = Ntfy()

    schedule.every(interval).seconds.do(crawl, queries=queries, ntfy=ntfy)
    while True:
        schedule.run_pending()
        time.sleep(1)
