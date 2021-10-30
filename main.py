from flask import Flask
from flask import send_file
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route("/Hello World/")
def Hello_World():

    url = "https://www.investing.com/equities/"

    http_string = requests.get(
        url,
        headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
        ).text

    dom_tree = BeautifulSoup(http_string, "html.parser")

    "CSS_selector"

    content_cell_wrapper = dom_tree.select_one("#cross_rate_markets_stocks_1")
    content_cells = content_cell_wrapper.select("tbody > tr")

    result = {"Stock_title":[],"Last_price":[],"Turnover":[]}

    for cell in content_cells:
      stock_id = cell['id'].split("_")[-1]
      stock_title = cell.select_one(".bold.left.noWrap.elp.plusIconTd").text
      last_price = cell.select_one(f".pid-{stock_id}-last").text
      turnover = cell.select_one(f".pid-{stock_id}-turnover").text
      result["Stock_title"].append(stock_title)
      result["Last_price"].append(last_price)
      result["Turnover"].append(turnover)

    df = pd.DataFrame(result)

    df.to_csv("output.csv")
    return send_file("output.csv", as_attachment=True)