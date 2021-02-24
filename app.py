from flask import Flask,jsonify,request
import json

app = Flask(__name__)

List_Dev = [{'id':0,'nome':'Pablo',
            'habilidades': ['Python','Flask','Linux']
             },
            {'id':1, 'nome':'Fabiana',
             'habilidades':['Redes sociais','textos']}
]

# altera dados de um dev atraves do ID
@app.route("/dev/<int:id>/", methods=['GET','PUT','DELETE'])
def desenvolvedor(id):
    if request.method == 'GET':
        try:
            response = List_Dev[id]
        except IndexError:
            msg = 'Desenvolvedor de ID {} não existe'.format(id)
            response= {'status':'erro','mensagem':msg}
        except Exception:
            msg  = 'Erro Desconhecido'
            response = {'status': 'erro', 'mensagem': msg}
        return jsonify(response)
    elif request.method == 'POST':
        dados = json.loads(request.data)
        List_Dev[id] = dados
        return jsonify(dados)
    elif request.method == 'DELETE':
        List_Dev.pop(id)
        return jsonify( {'status':'Registro Excluido'})

#lista todos os desenvolvedores e incluir novo desenvolvedor
@app.route("/dev/", methods=['GET','POST'])
def lista_devs():
    if request.method == 'POST':
        dados = json.loads(request.data)
        posicao = len(List_Dev)
        dados['id'] = posicao
        List_Dev.append(dados)
        return jsonify(List_Dev[posicao])
    elif request.method == 'GET':
        return jsonify(List_Dev)

@app.route('/dev/<int:id>/<hab>/', methods=['POST'])
def inc_habilidade(id,hab):
    if request.method == 'POST':
        dev_dados = List_Dev[id] #pego o dict do dev
        inc_h = dev_dados['habilidades'] # pego as habilidades
        incluir = 1
        for i in inc_h:
            if hab == i:
                incluir=0
                msg = 'Habiliade já existe'
                break
        if incluir:
            inc_h.append(hab) # incluo a nova habilidade
            List_Dev[id].update({"habilidades": inc_h})
            msg = 'sucesso inc habilidade'

        return(msg)



if __name__ == '__main__':
    app.run(debug=True)

