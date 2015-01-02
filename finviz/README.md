FinvizSpider grabs Finviz statistics for every ticker. Run: 
```sh
scrapy crawl FinvizSpider -o finviz.csv
```

YahooOptionsSpider reads statistics from Yahoo most active options. Run: 
```sh
scrapy crawl YahooOptionsSpider -o yahoo_options.csv
```

YahooGeneralSpider reads Yahoo summary and key statistics for every ticker. 
Results are stored in `yahoo_summary.csv` and `yahoo_keystat.csv`. Run: 
```sh
scrapy crawl YahooGeneralSpider
```
