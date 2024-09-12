import requests
import bs4
from dataclasses import dataclass
from typing import Union, Literal
from tqdm import tqdm


@dataclass
class Entry:
    """
    Represents a Boursorama recommendation entry
    """
    name: str
    advice : str
    last: Union[str, float]
    obj_100d : float
    potential: Union[str, float]
    nb_analysts : str
    BNA_year: float
    rend_year: Union[str, float]
    per_year: Union[str, float]
    per_last_year: Union[str, float]


class ForecastsBourso:
    """
    Object to handle Boursorama recommendations
    Useful methods:
    forward_potential
    backward_potential
    """
    def __init__(self):
        self.list_entry = []
        self.set_gathered_stocks = set()
        prefix_url = "https://www.boursorama.com/bourse/actions/consensus/recommandations-paris/"
        postfix_url = "?national_market_filter%5Bmarket%5D=SRD&national_market_filter%5Bsector%5D=&national_market_filter%5Banalysts%5D=1&national_market_filter%5Bperiod%5D=2024&national_market_filter%5Bfilter%5D=&sortColumn=consPotential&orderAsc=1"

        N_max = 20
        list_urls = [prefix_url+postfix_url] + [prefix_url+f"page-{k}"+postfix_url for k in range(1, N_max+1) if k != 1]
        res_end = None
        for url_i in tqdm(list_urls):
            if res_end == "End reached":
                break
            res = requests.get(url_i,
                               headers={'User-Agent': 'Mozilla/5.0'})
            # Checking for Bad download
            try:
                res.raise_for_status()
            except Exception as exc:
                raise TimeoutError("There was a problem: %s" % (exc))
            soup_res = bs4.BeautifulSoup(res.text, 'html.parser')
            self.soup_res = soup_res
            soup_2 = soup_res.find("table", {"class": "c-table c-table--generic c-table--generic c-shadow-overflow__table-fixed-column"}).find("tbody")
            check_in = 0
            for soup_i in soup_2.find_all("tr", {"class": "c-table__row"}):
                res_end = self._parse_entry(soup_i, check_in=(check_in>4))
                if res_end == "End reached":
                    break
                check_in += 1


    @property
    def forward_potential(self):
        return reversed(self.list_entry)

    @property
    def backward_potential(self):
        return self.list_entry

    def _parse_entry(self, soup_i, check_in) -> Union[None, Literal["End reached"]]:
        name = soup_i.find("a", {"class": "c-link c-link--animated"}).contents[0]
        if name in self.set_gathered_stocks:
            if check_in:
                return "End reached"
            else:
                return None
        else:
            self.set_gathered_stocks.add(name)
        advice = soup_i.find("span", {"class": "u-only-clipboard"}).contents[0]
        L = []
        for data_i in soup_i.find_all("td"):
            content = str(data_i.contents[0])
            if content is None:
                continue
            content = content.strip()
            if "c-table__cell--negative" in data_i["class"]:
                if content not in ["-", "\n-"]:
                    #print(content)
                    content = "-" + content
            L.append(content)
        L = L[2:]
        last = self._format_to_float(L[0])
        obj_100d = self._format_to_float(L[1])
        potential = self._format_to_float(L[2])
        nb_analysts = L[3]
        BNA_year = self._format_to_float(L[4])
        rend_year = self._format_to_float(L[5])
        per_year = self._format_to_float(L[6])
        per_last_year = self._format_to_float(L[7])
        new_entry = Entry(
            name=name,
            advice=advice,
            last=last,
            obj_100d=obj_100d,
            potential=potential,
            nb_analysts=nb_analysts,
            BNA_year=BNA_year,
            rend_year=rend_year,
            per_year=per_year,
            per_last_year=per_last_year
        )
        self.list_entry.append(new_entry)
        return None

    def _format_to_float(self, string_in):
        if string_in in ["Atteint", "-"]:
            return string_in
        percent = False
        if "%" in string_in:
            string_in = string_in.replace("%", "")
            percent = True
        string_in = string_in.replace(",", ".").replace(" ", "").replace("USD", "").replace("EUR", "").replace("GBP", "")
        fl = float(string_in)
        if percent:
            fl = fl/100
        return fl

if __name__ == "__main__":
    ForecastsBourso()