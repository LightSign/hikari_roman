from flask import make_response
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

def first_scray(URL):
    headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    }
    df = pd.DataFrame(index=[] , columns=[])
    res = requests.get(URL ,headers=headers)
    soup = bs(res.content, "html.parser")
    items = soup.select("div.s-item-container")
    for item in items:
        try:
            title = item.select("img")[0].get("alt")
            item_url = "https://www.amazon.co.jp" + item.select("a")[0].get("href")
            if item.find(class_="a-icon a-icon-jp a-icon-prime-jp a-icon-small s-align-text-bottom"):
                prime = "prime"
            else:
                prime = "no prime"
            pic_split = item.select("img")[0].get("srcset").split()
            pic_txt = ",".join(pic_split).split()
            picures_list = []
            for p_txt in pic_txt:
                if "jpg" in p_txt:
                    picures_list.append(p_txt)
            se = pd.Series(
                [title, item_url, prime, picures_list],
                ["title", "item_url", "prime", "picures_list"]
            )
            df = df.append(se, ignore_index=True)
        except Exception as e:
            pass
    return df

import csv
import io as cStringIO
import random
def download(df):
    txt = """
    社歌！
    早く円陣くめっ！
    男のロマンで迫るなら
    試練の道さえ怖くない
    この世で一匹光通信（あるいは代理店名）の営業マンは
    泣き言なんか言わないで
    根性、根性、ド根性
    俺がやらずに誰がやる
    おっす完全オーダーやります
    どっこい気合いであげてやる！
    いいかお前ら！（おっす！）
    昨日までのことは忘れて今日の数字を上げて
    全員オーダーするからな！（おっす！）
    入って来たばかりの新人も既存のメンバーも関係ねーんだよ
    ぜってー数字にからめよ！（おっす！）
    そん中でも、真っ先に受注あげんのはこの俺だー
    （俺だっ、俺だっ、俺だっ、俺だっ、俺だっ、俺だっ、俺だっ…俺だっ！）
    さらに、上乗せでアメックスのカードも社長にやらせんのはーこのー （俺だっっ！！！）
    頑張れよ、せーの（パンッ！）（オッス！！！）
    さー迷惑電話の開始ゾス！
    """
    txt_split = txt.split()
    file_name = random.choice(txt_split)

    f = cStringIO.StringIO()
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writerow(['item_url','pic_list','prime','title'])
    for i in range(len(df)):
        writer.writerow([
            df.item_url[i],
            df.picures_list[i],
            df.prime[i],
            df.title[i]
        ])
    res = make_response()
    res.data = f.getvalue()
    res.headers['Content-Type'] = 'text/csv'
    res.headers['Content-Disposition'] = 'attachment; filename='+ file_name +'.csv'
    return res
