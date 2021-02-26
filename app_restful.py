##---------------------------------------##
# Pacotes
##---------------------------------------##
from flask import Flask,request
from flask_restful import Resource, Api
import json

##---------------------------------------##
# Criando a instancia Flask
##---------------------------------------##
app = Flask(__name__)
api = Api(app)

##---------------------------------------##
# Lista , simulando um banco de dados
##---------------------------------------##

List_Dev = [{'id':0,'nome':'Pablo',
            'habilidades': ['Python','Flask','Linux']
             },
            {'id':1, 'nome':'Fabiana',
             'habilidades':['Redes sociais','textos']}
]

##---------------------------------------##
# altera dados de um dev atraves do ID
##---------------------------------------##
class Desenvolvedor(Resource):
    def get(self,id):
        try:
            response = List_Dev[id]
        except IndexError:
            msg = 'Desenvolvedor de ID {} não existe'.format(id)
            response= {'status':'erro','mensagem':msg}
        except Exception:
            msg  = 'Erro Desconhecido'
            response = {'status': 'erro', 'mensagem': msg}
        return response

    def put(self, id):
        dados = json.loads(request.data)
        if len(List_Dev) <= id:
            List_Dev.append(dados)
        else:
            List_Dev[id] = dados
        return dados

    def delete(self, id):
        List_Dev.pop(id)
        return ("Esse ID {} foi excluido com sucesso!".format(id))

##------------------------------------------------------------##
# lista todos os desenvolvedores e incluir novo desenvolvedor
#-------------------------------------------------------------##
class ListaDevs(Resource):
    def get(self):
        return (List_Dev)

    def post(self):
        dados = json.loads(request.data)
        posicao = len(List_Dev)
        dados['id'] = posicao
        List_Dev.append(dados)
        return (List_Dev[posicao])

##-----------------------------##
#      Inclusão de Habilidades
##-----------------------------##
class IncHabilidade(Resource):
    def post(self,id,hab):
        dev_dados = List_Dev[id]  # pego o dict do dev
        inc_h = dev_dados['habilidades']  # pego as habilidades
        incluir = 1
        for i in inc_h:
            if hab == i:
                incluir = 0
                msg = 'Habiliade já existe'
                break
        if incluir:
            inc_h.append(hab)  # incluo a nova habilidade
            List_Dev[id].update({"habilidades": inc_h})
            msg = 'sucesso inc habilidade'

        return (msg)

    def delete(self, id, hab):
        try:
            dev_dados = List_Dev[id]
        except IndexError:
            msg_ret = {'status': 'erro', 'mensagem': 'Desenvolvedor de ID {} não existe'.format(id)}
        except Exception:
            msg_ret = {'status': 'erro', 'mensagem': 'Erro Desconhecido'}
        else:
            inc_h = dev_dados['habilidades']  # pego as habilidades
            for i in inc_h:
                if hab == i:
                    pos = inc_h.index(i)
                    break
            try:
                inc_h.pop(pos)
            except UnboundLocalError:
                msg_ret = "A habilidade {} nao existe para o ID {}".format(hab, id)
            else:
                List_Dev[id].update({"habilidades": inc_h})
                msg_ret = "A habilidade {} foi excluida para o ID {}".format(hab, id)
        return (msg_ret)

class HabilidadesTodas(Resource):
    def get(self):
        HabTotal = []
        for i in List_Dev:
            hab_list = i['habilidades']
            for x in hab_list:
                HabTotal.append(x)
            x = set(HabTotal)
            HabTotal = list(x)
        return HabTotal

##-----------------------------##
#      Rotas Implementadas
##-----------------------------##
api.add_resource(Desenvolvedor,'/dev/<int:id>/')
api.add_resource(ListaDevs,'/dev/')
api.add_resource(IncHabilidade,'/dev/<int:id>/<hab>/')
api.add_resource(HabilidadesTodas,'/dev/hab/')



##---------------------------------------##
#  Só executar se chamar por ele mesmo
##---------------------------------------##
if __name__ == '__main__':
    app.run(debug=True)



