import scrapy
import bs4

class DividendInfoSpider(scrapy.Spider):
    name = 'dividend_info'
    allowed_domains = ['goodinfo.tw']
    stockid = 2330
    url = "https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID="+str(stockid)+"&SHOW_ROTC="
    start_urls = [url]

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        year = ["2021","2020","2019","2018","2017","2016"]
        cash_dividend = ["None"]*6
        stock_dividend = ["None"]*6
        all_dividend = ["None"]*6
        c = soup.find(id="divDetail").select("tr")
        for i in range(4,len(c)):
            for j in range(6):
                if c[i].select("td")[0].select_one('nobr').select_one("b").text == year[j]:
                    cash_dividend[j] = c[i].select("td")[3].text
                    stock_dividend[j] = c[i].select("td")[6].text
                    all_dividend[j] = c[i].select("td")[7].text
            if all_dividend[5]!="None":
                break
        for i in range(6):
            dividend = {
                "year" : year[i],                       #年分
                "cash_dividend" : cash_dividend[i],     #現金股利
                "stock_dividend" : stock_dividend[i],   #股票股利
                "all_dividend" : all_dividend[i]        #合季股利
                }
            yield dividend
