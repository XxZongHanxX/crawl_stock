import scrapy
import bs4

class StockInfoSpider(scrapy.Spider):
    name = 'stock_info'
    allowed_domains = ['mops.twse.com.tw']
    stockid = 2330
    url = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=" + str(stockid) + "&SYEAR=2021&SSEASON=1&REPORT_ID=C"
    start_urls = [url]


    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        ymq = ["2021Q1","2020Q4","2020Q3","2020Q2","2020Q1","2019Q4","2019Q3","2019Q2","2019Q1","2018Q4",
               "2018Q3","2018Q2","2018Q1","2017Q4","2017Q3","2017Q2","2017Q1","2016Q4","2016Q3","2016Q2","2016Q1"]
        ymq_ch = ["107年第4季","107年第3季","107年第2季","107年第1季","106年第4季","106年第3季","106年第2季","106年第1季",
                  "105年第4季","105年第3季","105年第2季","105年第1季"]
        stockid_ymq = soup.head.title.text.split(" ")
        url = ""
        ba = ["None"]*15
        inc = ["None"]*10
        mo = ["None"]*6
        before_after = 0
        if len(stockid_ymq)!=1:
            for i in range(9):
                if stockid_ymq[2] == ymq[i]:
                    quarter = ymq[i]
                    temp1 = ymq[i+1]
                    url = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID="+stockid_ymq[1]+"&SYEAR="+temp1[0:4]+"&SSEASON="+temp1[-1]+"&REPORT_ID=C"
                    before_after = 1
                    break
        else:
            ti = soup.find(id="content_d")
            temp2 = ti.find("center").find_all("center")
            temp2 = temp2[1].text.split(" ")
            temp2 = temp2[0].split("\u3000")
            for i in range(11):
                if temp2[1] == ymq_ch[i]:
                    quarter = ymq[i+9]
                    temp1 = ymq[i+10]
                    url = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID="+temp2[0]+"&SYEAR="+temp1[0:4]+"&SSEASON="+temp1[-1]+"&REPORT_ID=C"
                    break
        if before_after == 1:
            bss = ["1XXX","11XX","1100","1170","1180","1210","130X","1550","1600","1780","1840","1900","2XXX","21XX","2570"]
            ins = ["4000","5000","5900","6000","6900","7000","7900","7950","8200","9750"]
            mf = ["AAAA","BBBB","CCCC","EEEE","E00100","E00200"]
            temp=0
            bass = soup.find_all("table")[0]
            baid = bass.select("tr")
            for i in range(2,len(baid)):
                for j in range(15):
                    if bss[j] == baid[i].select("td")[0].text:
                        ba[j] = baid[i].select("td")[2].text
            incs = soup.find_all("table")[1]
            incid = incs.select("tr")
            for i in range(2,len(incid)):
                for j in range(10):
                    if ins[j] == incid[i].select("td")[0].text:
                        inc[j] = incid[i].select("td")[2].text
            mof = soup.find_all("table")[2]
            mofid = mof.select("tr")
            for i in range(2,len(mofid)):
                for j in range(6):
                    if mf[j] == mofid[i].select("td")[0].text:
                        mo[j] = mofid[i].select("td")[2].text
        if before_after == 0:
            bss = ["資產總計","流動資產合計","透過損益按公允價值衡量之金融資產－流動","應收帳款淨額","應收帳款－關係人淨額",
                   "其他應收款－關係人","存貨","採用權益法之投資","不動產、廠房及設備","無形資產","遞延所得稅資產",
                   "其他非流動資產","負債總計","流動負債合計","遞延所得稅負債"]
            ins = ["營業收入合計","營業成本合計","營業毛利（毛損）","營業費用合計","營業利益（損失）","營業外收入及支出合計",
                   "繼續營業單位稅前淨利（淨損）","所得稅費用（利益）合計","本期淨利（淨損）","基本每股盈餘合計"]
            mf = ["營業活動之淨現金流入（流出）","投資活動之淨現金流入（流出）","籌資活動之淨現金流入（流出）",
                  "本期現金及約當現金增加（減少）數","期初現金及約當現金餘額","期末現金及約當現金餘額"]
            bass = soup.find_all("table")[1]
            baid = bass.select("tr")
            for i in range(2,len(baid)):
                temp = baid[i].select("td")[0].text
                temp = temp.replace("\u3000","")
                temp = temp.replace(" ","")
                for j in range(15):
                    if bss[j] == temp:
                        ba[j] = baid[i].select("td")[1].text
                        ba[j] = ba[j].replace("\u3000","")
                        ba[j] = ba[j].replace(" ","")
            incs = soup.find_all("table")[2]
            incid = incs.select("tr")
            for i in range(2,len(incid)):
                temp = incid[i].select("td")[0].text
                temp = temp.replace("\u3000","")
                temp = temp.replace(" ","")
                for j in range(10):
                    if ins[j] == temp:
                        inc[j] = incid[i].select("td")[1].text
                        inc[j] = inc[j].replace("\u3000","")
                        inc[j] = inc[j].replace(" ","")
            mof = soup.find_all("table")[3]
            mofid = mof.select("tr")
            for i in range(2,len(mofid)):
                temp = mofid[i].select("td")[0].text
                temp = temp.replace("\u3000","")
                temp = temp.replace(" ","")
                for j in range(6):
                    if mf[j] == temp:
                        mo[j] = mofid[i].select("td")[1].text
                        mo[j] = mo[j].replace("\u3000","")
                        mo[j] = mo[j].replace(" ","")
        balance_sheet_statement = {
            "1XXX" : ba[0],     #資產總計
            "11XX" : ba[1],     #流動資產合計
            "1100" : ba[2],     #透過損益按公允價值衡量之金融資產 - 流動
            "1170" : ba[3],     #應收帳款淨額
            "1180" : ba[4],     #應收帳款 - 關係人淨額
            "1210" : ba[5],     #其他應收款 - 關係人
            "130X" : ba[6],     #存貨
            "1550" : ba[7],     #採用權益法之投資
            "1600" : ba[8],     #不動產、廠房及設備
            "1780" : ba[9],     #無形資產
            "1840" : ba[10],    #遞延所得稅資產
            "1900" : ba[11],    #其他非流動資產
            "2XXX" : ba[12],    #負債總計
            "21XX" : ba[13],    #流動負債合計
            "2570" : ba[14]     #遞延所得稅負債
            }
        income_statement = {
            "4000" : inc[0],    #營業收入合計
            "5000" : inc[1],    #營業成本合計
            "5900" : inc[2],    #營業毛利(毛損)
            "6000" : inc[3],    #營業費用合計
            "6900" : inc[4],    #營業利益(損失)
            "7000" : inc[5],    #營業外收入及支出合計
            "7900" : inc[6],    #繼續營業單位稅前(淨損)
            "7950" : inc[7],    #所得稅費用(利益)合計
            "8200" : inc[8],    #本期淨利(淨損)
            "9750" : inc[9]     #基本每股盈餘合計
            }
        money_flow = {
            "AAAA" : mo[0],     #營業活動之淨現金流入(流出)
            "BBBB" : mo[1],     #投資活動之淨現金流入(流出)
            "CCCC" : mo[2],     #籌資活動之淨現金流入(流出)
            "EEEE" : mo[3],     #本期現金及約當現金增加(減少)數
            "E00100" : mo[4],   #期初現金及約當現金餘額
            "E00200" : mo[5]    #期末現金及約當現金餘額
            }
        if url == "":
            quarter = ymq[-1]
        all_info = {
            "quarter" : quarter,                                #季別
            "balance_sheet_statement" : balance_sheet_statement,#資產負債表
            "income_statement" : income_statement,              #損益表
            "money_flow" : money_flow                           #現金流量表
            }
        yield all_info
        if url !="":
            yield response.follow(url, callback=self.parse)
