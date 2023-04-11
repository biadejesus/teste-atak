from bottle import route, run, template, request
import json
from API import get_title
 
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
