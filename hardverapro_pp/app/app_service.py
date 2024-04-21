import time
import schedule
import requests
from hardverapro_pp.utils import log
from hardverapro_pp.utils.config import Config
from hardverapro_pp.utils.notify import Ntfy
from hardverapro_pp.core.ha_query import HardveraproQuery
from hardverapro_pp.core.ha_item import HardveraproItem
from hardverapro_pp.core.ha_parser import HardveraproParser
from hardverapro_pp.utils.database import ItemDatabase


def generate_queries(cfg: Config) -> list[tuple[HardveraproQuery, str]]:
    queries = []
    default_topic = cfg.key("ntfy").key("default-topic").str()
    user_agent = cfg.key("network").key("user-agent").str(requests.utils.default_headers()["User-Agent"])
    for item in cfg.key("item-urls").list():
        topic = item.key("topic").str(default_topic)
        queries.append((HardveraproQuery(item, user_agent), topic))

    return queries


def generate_hapro_item_ntfy(ntfy: Ntfy, item: HardveraproItem, topic: str):
    tags = "rotating_light"
    icon = "https://cdn.rios.hu/design/ha/logo-compact.png"
    ntfy.push(
        topic,
        item.title,
        f"Ára: {item.price}, {item.upload_date}-kor új terméket rakott fel {item.seller} ({item.reputation}) tag",
        tags,
        item.url,
        item.thumbnail,
        icon,
    )


def crawl_queries(queries: list[tuple[HardveraproQuery, str]], ntfy: Ntfy, config: Config):
    for query, topic in queries:
        content = query.make_query()
        parser = HardveraproParser(config, content)
        items = parser.get_items()
        itemdb = ItemDatabase(query.get_id())

        for item in items:
            if not itemdb.exists(item):
                if not itemdb.is_new_database():
                    generate_hapro_item_ntfy(ntfy, item, topic)
                itemdb.insert(item)


def loop():
    config = Config()
    log.initialize(None, None, None)
    ntfy = Ntfy()
    interval = config.key("item-re-check-interval").int(60)
    queries = generate_queries(config)

    schedule.every(interval).seconds.do(crawl_queries, queries=queries, ntfy=ntfy, config=config)
    while True:
        schedule.run_pending()
        time.sleep(1)
