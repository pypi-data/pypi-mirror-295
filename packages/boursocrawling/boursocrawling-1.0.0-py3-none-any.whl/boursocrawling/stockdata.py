import requests
import bs4
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from typing import Any

class StockData:
    """
    This represents a stock

    Useful attributes:
    - short_code
    - url: Boursorama URL
    - soup_res: Beautiful_Soup result
    - name: Name of the stock
    - ISIN: ISIN code of the stock
    - price: price of the stock currently
    - DER: Last of the day
    - OUV: Opening of the day
    - highest: Highest of the day
    - lowest: Lowest of the day
    - Volume: Volume of the day

    Useful method:
    plot_all

    """
    def __init__(self, short_code: str):
        """
        The StockData class

        :param short_code: code of the Boursorama format.
        Example: 1rPASY

        """
        self.short_code = short_code
        BASE_BOURSO_LINK = "https://www.boursorama.com/cours/"
        # PARSING
        self.url = BASE_BOURSO_LINK + self.short_code
        res = requests.get(self.url,
                           headers={'User-Agent': 'Mozilla/5.0'})
        # Checking for Bad download
        try:
            res.raise_for_status()
        except Exception as exc:
            raise TimeoutError("There was a problem: %s" % (exc))
        soup_res = bs4.BeautifulSoup(res.text, 'html.parser')
        self.soup_res = soup_res
        self._get_data_from_soup(soup_res)


    def _get_data_from_soup(self, soup_res):
        # name c-faceplate__company-link
        self.name = soup_res.find('a', {
            'class': 'c-faceplate__company-link'}).contents[0].split("\n")[
            1].strip()
        # price c-instrument c-instrument--last
        price_str = soup_res.find('span', {
            'class': 'c-instrument c-instrument--last'}).contents[0]
        self.price = float(price_str.replace(",", "."))

        # isin code c-faceplate__isin
        self.ISIN_code, self.short_code = soup_res.find('h2', {
            'class': 'c-faceplate__isin'}).contents[0].split(" ")

        # tables
        tables = soup_res.find("table",
                               {"class": "c-table c-table--generic"})
        head_table = self._find_head(tables)
        data_table = self._find_data(tables, len_max=len(head_table))
        self.head_table = head_table
        self.data_table = data_table
        assert len(data_table) == 5
        self.DER = [data_table[0], head_table]
        self.OUV = [data_table[1], head_table]
        self.highest = [data_table[2], head_table]
        self.lowest = [data_table[3], head_table]
        self.volume = [data_table[4], head_table]

    def _find_head(self, table_in):
        L = []
        CURRENT_YEAR = datetime.now().year
        for head_i in table_in.find_all("th"):
            date_bs = head_i.find("span", {"aria-hidden":"true"})
            if date_bs is None:
                continue

            day, month = date_bs.contents[0].split("-")
            day_dt = datetime(year=CURRENT_YEAR, month=int(month), day=int(day))
            L.append(day_dt)
        return L

    def _find_data(self, table_in, len_max):
        L = []
        tables_i = table_in.find_all('td', {
            'class': 'c-table__cell c-table__cell--dotted c-table__cell--tiny'})
        L2 = []
        for str_i in tables_i:
            value_str = str_i.contents[0].split("\n")[1].strip()
            value_float = float(value_str.replace(",", ".").replace(" ", ""))
            L2.append(value_float)
            if len(L2) >= len_max:
                L.append(L2)
                L2 = []
        return L


    def plot(self, index_data=0):
        label_list = ["LAST OF DAY", "OPENING OF DAY", "HIGHEST OF DAY", "LOWEST OF DAY", "VOLUME"]
        label = label_list[index_data]
        data_table = self.data_table[index_data]
        plt.plot(self.head_table, data_table, label=label)
        plt.title(label)
        plt.show()

    def plot_all(self):
        label_list = ["LAST OF DAY", "OPENING OF DAY", "HIGHEST OF DAY", "LOWEST OF DAY"]
        hour_shift = {
            0: timedelta(hours=17, minutes=30), # Closing at 17h30
            1: timedelta(hours=9), # Morning, opening at 9h
            2: timedelta(hours=14), # Mid-day, opening at 14h
            3: timedelta(hours=14), # Mid-day, opening at 14h
        }


        for i in range(len(label_list)):
            time_serie = [k+hour_shift[i] for k in self.head_table]
            plt.scatter(time_serie, self.data_table[i], label=label_list[i])
        plt.title(f"{self.name}/ISIN:{self.ISIN_code}")
        plt.legend()
        plt.show()


    @classmethod
    def find_by_search_engine(cls,
                     query: str) -> Any: # Self:
        """
        Finds a stock using the Boursorama search engine
        :param query: string of the query
        :return: Self
        """
        url_find = f"https://www.boursorama.com/recherche/?query={query}&seeAllResults=tous-les-resultats"
        res = requests.get(url_find,
                           headers={'User-Agent': 'Mozilla/5.0'})
        # Checking for Bad download
        try:
            res.raise_for_status()
        except Exception as exc:
            raise TimeoutError("There was a problem: %s" % (exc))
        soup_res = bs4.BeautifulSoup(res.text, 'html.parser')
        soup_res = soup_res.find("tbody", {"class": "c-table__body"})
        soup_res = soup_res.find("tr")
        stock_code = soup_res["data-ist"]
        print(f"Found {stock_code} for query {query}")
        return cls(stock_code)
