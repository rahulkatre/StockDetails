import json

import requests
from bs4 import BeautifulSoup as Soup
from lxml import html


class StockScrape:
    def __init__(self, url, storage, header):
        self.url = url
        self.storage = storage
        self.header = header
        self.stocks = {}

    def scraper_bs4(self):
        """method is used to scrap the URL and provide output in a format
        which could be dumped as json in a file
        i.e, {'stock_name': [stock details]} using BeautifulSoup."""
        data = requests.get(self.url)
        parsed_data = Soup(data.text, "html.parser")
        req_div = parsed_data.find_all(
            "div", {"class": "bsr_table hist_tbl_hm"})
        rows = req_div[0].find('tbody').find_all('tr', recursive=False)
        for row in rows:
            stock_name = row.find('a').text.strip()
            stock_details = [float(col.text.strip().replace(',', ''))
                             for col in row.find_all('td')[1:7]]
            self.stocks[stock_name] = stock_details

    def scraper_lxml(self):
        """method is used to scrap the URL and provide output in a format
        which could be dumped as json in a file
        i.e, {'stock_name': [stock details]} using lxml."""
        stock_page = requests.get(self.url)
        parser = html.fromstring(stock_page.text)
        rows = parser.xpath(
            '//div[@class="bsr_table hist_tbl_hm"]/table/tbody/tr')
        for data in rows:
            columns = data.getchildren()
            stock_name = columns[0].xpath(".//a")[0].text.strip()
            stock_details = [float(col.text.strip().replace(',', ''))
                             for col in columns[1:7]]
            self.stocks[stock_name] = stock_details

    def formatted_data(self):
        """Formats and processes the stock details generated from scraper method.
         Provides the data in printable output format"""
        try:
            formatted_output = "\033[93m{:<30} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}\033[0m\n".format(
                *self.header)
            fp = open(self.storage, 'r')
            prev_stocks = json.loads(fp.read())
            fp.close()
            for key, value in self.stocks.items():
                try:
                    prev_data = prev_stocks[key]
                    formatted_output += "{:<30} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}".format(
                        '{}....'.format(key[:25]) if len(key) > 28 else key, *value)
                    gain_loss = (
                        (value[2] - prev_data[2]) / prev_data[2]) * 100
                    value.append(gain_loss)
                    if gain_loss >= 0:
                        formatted_output += "\033[92m{:<18}\033[0m\n".format(
                            round(gain_loss, 4))
                    else:
                        formatted_output += "\033[91m{:<18}\033[0m\n".format(
                            round((-1) * gain_loss, 4))
                except KeyError:
                    value.append('New Entrant')
                    formatted_output += "{:<30} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}\n".format(
                        '{}....'.format(key[:25]) if len(key) > 28 else key, *value)
        except FileNotFoundError:
            for key, value in self.stocks.items():
                value.append('New Entrant')
                formatted_output += "{:<30} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18}\n".format(
                    '{}....'.format(key[:25]) if len(key) > 28 else key, *value)
        with open(self.storage, 'w') as fp:
            fp.write(json.dumps(self.stocks))

        return formatted_output


def main():
    gainers_resources = {
        'url': 'https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php',
        'storage': 'gainers.json',
        'header': [
            'name',
            'high',
            'low',
            'last_price',
            'prev_close',
            'change',
            '% Gain',
            'Gain/Lost']}

    losers_resources = {
        'url': 'https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php',
        'storage': 'losers.json',
        'header': [
            'name',
            'high',
            'low',
            'last_price',
            'prev_close',
            'change',
            '% Loss',
            'Gain/Lost']}

    gainers_stock = StockScrape(**gainers_resources)
    gainers_stock.scraper_lxml()
    print("\033[1m\033[95mNSE - TOP GAINERS - NIFTY 50 \033[0m")
    print(gainers_stock.formatted_data())

    losers_stock = StockScrape(**losers_resources)
    losers_stock.scraper_lxml()
    print("\033[1m\033[95mNSE - TOP LOSERS - NIFTY 50 \033[0m")
    print(losers_stock.formatted_data())


if __name__ == '__main__':
    main()
