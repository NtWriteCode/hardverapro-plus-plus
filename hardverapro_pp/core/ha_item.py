import os
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
    
    def __str__(self) -> str:
        return (
            f'Id:\t\t{self.id}{os.linesep}'
            f'Title:\t\t{self.title}{os.linesep}'
            f'Price:\t\t{self.price}{os.linesep}'
            f'Seller:\t\t{self.seller}{os.linesep}'
            f'S. Repu:\t{self.reputation}{os.linesep}'
            f'Upload at:\t{self.upload_date}{os.linesep}'
            f'Url:\t\t{self.url}{os.linesep}'
            f'Thumbnail:\t{self.thumbnail}{os.linesep}'
        )
