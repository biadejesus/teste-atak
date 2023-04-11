import requests
import json
from bs4 import BeautifulSoup

def get_title(entrada):
    params = {
        "q": entrada,       # busca feita
        "hl": "pt",          # linguagem
        "gl": "br",          # país da pesquisa
        "start": 0,          # número da página
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    } #qual buscador ele vai usar

    data = []
    r = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(r.text, 'lxml')

    for result in soup.select(".tF2Cxc"): #".tF2Cxc" é o código CSS contido em cada pesquisa na página do Google
        title = result.select_one("h3").text #pega o título da página
        link = result.select_one("a")["href"] #pega o link
        data.append({
            "title": title,
            "link": link
        })

    return json.dumps(data, ensure_ascii=False)
