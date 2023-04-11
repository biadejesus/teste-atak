from bottle import route, run, template, request
import requests
import json
import lxml
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
    }

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

    
@route('/')
def index():
    return template('''

    <body style="display: flex;justify-content: center;">
    <div >
        <h1>Pesquisa Google</h1>
        <form action="/" method="get">
            <input type="text" name="entrada" id="entrada">
            <input type="submit" value="Buscar">
        </form>
    </div>
    </body>
    ''')

@route('/', method='GET')
def scrape():
    entrada = request.query.get('entrada')
    if entrada:
        results = json.loads(get_title(entrada))
        output = ""
        for result in results: #percorre cada item do json e deixa no formato desejado
            output += "{}<br>".format(result['title'])
            output += "[<a href='{}' target='_blank' >{}</a>]<br><br>".format(result['link'], result['link'])
        return template('''
            <h1 style="display: flex;justify-content: center;">Pesquisa Google</h1>
            {{!output}}
        ''', entrada=entrada, output=output)
         #a ! indica ao bottle que o output deve ser renderizado diretamente no HTML
    else:
        return index() #se nao for escrito nada, volta pra página inicial.


run(host='localhost', port=8080, debug=True)
