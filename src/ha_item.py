import hashlib


class HardveraproItem():
    def __init__(self, title: str, price: str, url: str, thumbnail: str, seller: str, upload_date: str, reputation: str) -> None:
        self.title = title
        self.price = price
        self.url = url.strip()
        self.thumbnail = thumbnail
        self.seller = seller
        self.upload_date = upload_date
        self.reputation = reputation
        self.id = hashlib.sha1(url.encode()).hexdigest().lower()

    def __eq__(self, other) -> bool:
        return isinstance(other, HardveraproItem) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.url)
