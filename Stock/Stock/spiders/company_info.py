import scrapy
import bs4

class CompanyInfoSpider(scrapy.Spider):
    name = 'company_info'
    allowed_domains = ['goodinfo.tw']
    stockid = 2330
    url = "https://goodinfo.tw/StockInfo/BasicInfo.asp?STOCK_ID="+str(stockid)
    start_urls = [url]

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        c = soup.body.find_all("table")[15].select("tr")
        a = ["None"]*12
        company = ["公司名稱","產業別","上市/上櫃","資本額","成立日期","上市日期","董事長","總經理","發言人","總機電話","公司網址","主要業務"]
        for i in range(len(c)):
            temp = c[i].select("td")
            if len(temp)!=1:
                for j in range(12):
                    if temp[0].text == company[j]:
                        temp1 = temp[1].text.replace("\xa0","")
                        a[j] = temp1
            if len(temp)==4:
                for j in range(12):
                    if temp[2].text == company[j]:
                        temp1 = temp[3].text.replace("\xa0","")
                        a[j] = temp1
        company_info = {
            "company_name" : a[0],      #公司名稱
            "industry" : a[1],          #產業別
            "listed_counter" : a[2],    #上市/上櫃
            "capital" : a[3],           #資本額
            "found_date" : a[4],        #成立日期
            "listed_date" : a[5],       #上市日期
            "chairman" : a[6],          #董事長
            "manager" :a[7],            #總經理
            "spokesman" : a[8],         #發言人
            "phone" : a[9],             #總機電話
            "web" : a[10],              #公司網址
            "operating_item" : a[11]    #主要業務
            }
        yield company_info
