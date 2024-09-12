import json
import requests as r
from urllib3.exceptions import InsecureRequestWarning
r.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class Lab(object):
    """Manages tasks"""
    def __init__(self, host='127.0.0.1', port='8443', apikey=None):
        super(Lab, self).__init__()
        self.host   = host
        self.port   = port
        self.apikey = apikey
        self.header = {'X-Go-Lab-EHPY':self.apikey}
        self.url    = f'https://{self.host}:{self.port}'

    def Help(self):
        self.help = '''
        Registrar um novo usuário (Utilize um email válido):
        lab.Register('user', 'email')

        GUARDE A CHAVE DE API!!!

        Para iniciar comunicação com o servidor:
        lab = PyLab.Lab(host='<serverIP>', apikey='<chave_de_api>')

        Receber sua pontuação e questões já resolvidas:
        lab.GetMyScore()

        Ver o ScoreBoard:
        lab.GetScoreBoard()

        Receber todas as perguntas:
        lab.GetQuestions()

        Receber o enunciado de uma pergunta específica:
        lab.GetQuestions(<num>)

        Receber dados de uma questão:
        lab.GetQuestionData(<num>)

        Enviar <data> como resposta da questão <num>:
        lab.SendAnswer(<num>, <data>)

        Respondendo à questão #01:
        lab.SendAnswer(1, lab.GetQuestionData(1))

        Gerando uma nova chave da API:
        lab.NewKey('<email-usado-no-cadastro>')
        '''
        print(self.help)

    def Register(self, username, email):
        self.username = username
        self.email = email
        try:
            req = r.post(self.url + '/register', json={"username":self.username, "email":self.email}, verify=False)
        except:
            raise
        if req.status_code == 201:
            jsonResp         = json.loads(req.content)
            self.apikey      = jsonResp['apikey']
            self.header['X-Go-Lab-EHPY'] = self.apikey
            print(f'New player has been registered under the name {self.username}!\nYour AIP key is {self.apikey}.\nStore it safely.')
        elif req.status_code == 400:
            print('New player was not created. Check the data sent.')
        elif req.status_code == 403:
            jsonResp = json.loads(req.content)
            print(jsonResp['error'])

    def NewKey(self, email):
        uri = f'/newKey'
        jsonReq = {"email":email}
        try:
            req = r.post(self.url + uri, json=jsonReq, headers=self.header, verify=False)
        except:
            raise
        if req.status_code == 200:
            resp = json.loads(req.content)['success']
            print(resp)
        elif req.status_code == 400:
            print('Error. Check the data sent.')
        elif req.status_code == 403:
            print('Operation not allowed.')
        elif req.status_code == 404:
            print('Email not found in database')

    def GetScoreBoard(self, rows=None):
        try:
            req = r.get(self.url + '/getScoreBoard', headers=self.header, verify=False)
        except:
            raise
        if req.status_code == 200:
            jsonResp = json.loads(req.content)
            sortedlist = sorted(jsonResp, key=lambda i: (-i['points'], i['timestamp']))
            if isinstance(rows, int): sortedlist = sortedlist[:rows % len(sortedlist)]
            for idx, item in enumerate(sortedlist):
                print(f'#{idx+1} - {item["name"]}: {item["points"]} points.')
        else:
            print('Could not get data.')

    def GetMyScore(self):
        try:
            req = r.get(self.url + '/getMyScore', headers=self.header, verify=False)
            jsonResp = json.loads(req.content)
        except:
            raise
        if req.status_code == 200:
            print(f'You have {jsonResp["points"]} points.\nQuestions done: {",".join(sorted(jsonResp["questionsdone"], key=int))}')
        else:
            print(jsonResp['error'])

    def GetQuestions(self, id=False):
        uri = '/getQuestions'
        if id:
            uri += '/'+str(id)
        try:
            req = r.get(self.url + uri, headers=self.header, verify=False)
        except:
            raise
        try:
            jsonResp = json.loads(req.content)
        except:
            print(f'Malformed response: {req.text}')
        if req.status_code == 200:
            for key in sorted(jsonResp, key=int):
                print(f'Question #{key}: {jsonResp[key]}')
        elif req.status_code == 403:
            print('You don\'t have permission to perform this type of request.')
        elif req.status_code == 404:
            print('Question id not found.')
        else:
            print(f'Unknown error: {req.status_code}')

    def GetQuestionData(self,id):
        uri = '/getQuestionData/'+str(id)
        try:
            req = r.get(self.url + uri, headers=self.header, verify=False)
        except:
            raise
        if req.status_code == 403:
            print('You don\'t have permission to perform this type of request.')
        try:
            jsonResp = json.loads(req.content)
            return jsonResp[str(id)]
        except:
            print('Malformed response.')

    def SendAnswer(self, idq, answer):
        jsonReq = {'id':str(idq),'answer':answer}
        try:
            req = r.post(self.url + '/sendAnswer', json=jsonReq, headers=self.header, verify=False)
            jsonResp = json.loads(req.content)
        except:
            raise

        if req.status_code == 403:
            print('You don\'t have permission to perform this type of request.')

        if req.status_code == 200:
            print('Your answer is correct!')
        elif req.status_code == 401:
            print('You have already answered this question.')
        elif req.status_code == 404:
            print(jsonResp['error'])

    def ToggleRegistration(self, email='all', enabled=False):
        self.email = email
        uri = f'/registration/{self.email}/{enabled}'
        self.enabled = json.loads(enabled)
        try:
            req = r.get(self.url + uri, headers=self.header, verify=False)
        except:
            raise
        if req.status_code == 200:
            print(f'Registration {["enabled" if self.enabled else "disabled"][0]} for {self.email}!')
        elif req.status_code == 400:
            print('Registration not changed. Check the data sent.')
        elif req.status_code == 403:
            print('Toggle registration was not allowed.')
