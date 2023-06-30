import re

import scrapy
from scrapy import Selector
from scrapy.selector import SelectorList
from scrapy_splash import SplashRequest, SplashJsonResponse

from chemical_scraper.items import ChemicalProductItem
from chemical_scraper.services.currency_converter import CurrencyConverter

lua_script = """
function main(splash, args)
    assert(splash:go(args.url))

  while not splash:select('div.pro_casinfor div table') do
    splash:wait(0.1)
    print('waiting...')
  end
  return {html=splash:html()}
end
"""


class AccelpharmtechSpider(scrapy.Spider):
    name = "accelpharmtech_spider"

    def start_requests(self):
        url = "http://www.accelpharmtech.com/products/549.html"
        yield SplashRequest(
            url,
            callback=self.parse,
            endpoint="execute",
            args={
                "wait": 0.5,
                "lua_source": lua_script,
                url: "http://www.accelpharmtech.com/products/549.html",
            },
        )

    def parse(self, response: SplashJsonResponse, *args, **kwargs):
        for chemical_product in response.css("div.pro_casinfor"):
            table_items = self.__get_table_items(chemical_product)
            dict_of_lists = self.__get_dict_of_lists(table_items)

            yield ChemicalProductItem(
                **{
                    "company_name": "Accelpharmtech",
                    "product_url": chemical_product.css("td.blue a::attr(href)").get(),
                    "availability": self.__get_availability(table_items),
                    "numcas": chemical_product.css("td a::text").getall()[1],
                    "name": chemical_product.css("td a::text").getall()[0],
                    "qt_list": dict_of_lists["qt_list"],
                    "unit_list": dict_of_lists["unit_list"],
                    "currency_list": dict_of_lists["currency_list"],
                    "price_pack_list": dict_of_lists["price_pack_list"],
                }
            )

        next_page = response.css("div.padding span")[3].css("span a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SplashRequest(
                next_page,
                callback=self.parse,
                endpoint="execute",
                args={"wait": 0.5, "lua_source": lua_script},
            )

    @staticmethod
    def __get_availability(table_items: SelectorList[Selector]) -> bool:
        return any(
            item.css("tr::attr(leadtime)").get() == "In stock" for item in table_items
        )

    @staticmethod
    def __get_table_items(chemical_product: Selector) -> SelectorList[Selector]:
        return chemical_product.css("table.goodstable tr")[1:]

    @staticmethod
    def __get_dict_of_lists(table_items: SelectorList[Selector]) -> dict[str, list]:
        dict_of_lists = {
            "qt_list": [],
            "unit_list": [],
            "currency_list": [],
            "price_pack_list": [],
        }
        price_pattern = r"([^\d.]+)(\d+)"
        unit_pattern = r"(\d+)(\D+)"
        for item in table_items:
            price = item.css("td")[2].css("td::text").getall()[-1]
            price_result = re.match(price_pattern, price)
            currency = (
                CurrencyConverter.convert_currency(price_result.group(1))
                if price_result
                else None
            )
            price_amount = int(price_result.group(2)) if price_result else None

            weight = item.css("td")[3].css("td::text").get().strip()
            weight_result = re.match(unit_pattern, weight)
            weight_number = int(weight_result.group(1)) if weight_result else None
            weight_unit = weight_result.group(2).lower() if weight_result else None

            dict_of_lists["qt_list"].append(weight_number)
            dict_of_lists["unit_list"].append(weight_unit)
            dict_of_lists["currency_list"].append(currency)
            dict_of_lists["price_pack_list"].append(price_amount)
        return dict_of_lists
