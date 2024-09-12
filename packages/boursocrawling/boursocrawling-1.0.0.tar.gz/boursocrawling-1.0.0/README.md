Goal
====

Get data from the website Boursorama:
- Query results
- Stock data
- Recommendations

How to install
==============

`pip install boursocrawling`

How to use
==========

Search engine
-------------

```pycon
from boursocrawling.stockdata import StockData

my_stock = StockData.find_by_search_engine("Alstom")
my_stock = StockData.find_by_search_engine("ASSYSTEM")
my_stock = StockData.find_by_search_engine("FR0000074148")
```

This returns a `StockData` instance.

The StockData instance
----------------------

If you already know the code of the stock, you can instance the StockData directly from its code:

```pycon
from boursocrawling.stockdata import StockData

my_stock = StockData("1rPASY")
```

You can plot a quick 5-day summary using `plot_all`:

```pycon
from boursocrawling.stockdata import StockData

my_stock = StockData("1rPASY")
my_stock.plot_all()
```

Alternatively, you can access instance data using its attributes:
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
- volume: Volume of the day

Forecasts
---------
```pycon
from boursocrawling.forecasts import ForecastsBourso

forecast_manager = ForecastsBourso()
print(forecast_manager.forward_potential)
```
The Forecast manager returns all the forecasts sorted by potential.

Copyright
---------

Alexandre Delaisement

Data stored by Boursorama belong to Boursorama. I am not affiliated with them.