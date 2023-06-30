# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChemicalProductItem:
    company_name: str
    product_url: str
    numcas: str
    name: str
    qt_list: list[int]
    unit_list: list[str]
    currency_list: list[str]
    price_pack_list: list[int]
    availability: Optional[bool] = field(default=None)

