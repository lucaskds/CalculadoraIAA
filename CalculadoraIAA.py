#coding: utf-8

import mechanize
import getpass
import os

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def getHistory(br):
    return br.open("https://cagr.sistemas.ufsc.br/modules/aluno/historicoEscolar/")

def getMirror(br):
    return br.open("https://cagr.sistemas.ufsc.br/modules/aluno/espelhoMatricula/")

def conectar_CAGR(username, password):
    br = mechanize.Browser()
    response = br.open("https://sistemas.ufsc.br/login?service=https%3A%2F%2Fcagr.sistemas.ufsc.br%2Fj_spring_cas_security_check&userType=padrao&convertToUserType=alunoGraduacao&lockUserType=1")

    for form1 in br.forms():
        form = form1

    br.select_form(nr=0)

    form["username"] = username
    form["password"] = password

    response = br.submit()

    return br


def get_IAA(text, size):
    for i in range(0,2):
        size = text.rfind("IAA", 0, size)

        inicio = size
        fim = text.find("IAP", inicio, len(text))
    text = strip_tags(text [inicio + 4:fim])
    text = [t.replace(',', '.') for t in text]
    IAA = text[1:len(text)-1]
    return float("".join(IAA))

def get_cargaHoraria(text):
    size = len(text)
    inicio = text.rfind("total:", 0, size)
    fim = text.find(" a", inicio, size)
    text = text [inicio + 7 : fim - 2]
    return int(text)

def get_nome(text):
    size = len(text)
    inicio = text.find("rich-panel-header", 0, size)
    inicio = text.find(">", inicio, size)
    fim = text.find("<", inicio, size)
    text = text [inicio + 1:fim]
    return text

def getLgth(text):
    ret = 0; 
    size = len(text)
    types = [">Ob<",">Ex<",">Op<"]
    for s in types:    
        i = 0
        while i <> -1:
            i = text.find(s, i+1, size)
	    if i <> -1:
	        ret = ret+1
   
    return ret-1;

def dName(text, pos):
    size = len(text)
    strr = "{}:j_id213\">".format(pos)
    init = text.rfind(strr, 0, size)
    fim = text.find("</td>", init, size)
    text = text [init + len(strr):fim]
    return text

def dHA(text, pos):
    size = len(text)
    strr = "{}:j_id219\" style=\"text-align: center\">".format(pos)
    init = text.rfind(strr, 0, size)
    fim = text.find("</td>", init, size)
    text = text [init + len(strr):fim]
    return int(text)

#PROGRAMA COMECA AQUI

username = raw_input("Insira sua matrícula:\n")
password = getpass.getpass("\nInsira sua senha do CAGR:\n")

response = conectar_CAGR(username, password);

history = getHistory(response)

pagina = history.read()

IAA = get_IAA(pagina,len(pagina))
cargaHoraria = get_cargaHoraria(pagina)
nome = get_nome(pagina)

print("Olá {} !".format(nome))
print("Atualmente seu IAA é {} e sua carga horária total cursada é de {} horas".format(str(IAA), str(cargaHoraria)))


mirror = getMirror(response)

pagina = mirror.read()
totalAulas = getLgth(pagina)

horasAulasTotal = 0
somatorio = 0
for i in range(0,totalAulas):
    horasAulas = dHA(pagina, i)
    horasAulasTotal += horasAulas
    notaAula = float(raw_input("Insira a possivel nota em {}\n".format(dName(pagina, i))))
    somatorio += notaAula*horasAulas
horasAulasTotal += cargaHoraria
somatorio += IAA*cargaHoraria

print ("De acordo com o que você me informou, seu possível IAA será {}".format(str("{0:.2f}".format(somatorio/horasAulasTotal))))
