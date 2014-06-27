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

def conectar_CAGR(username, password):
    br = mechanize.Browser()
    response = br.open("https://sistemas.ufsc.br/login?service=https%3A%2F%2Fcagr.sistemas.ufsc.br%2Fj_spring_cas_security_check&userType=padrao&convertToUserType=alunoGraduacao&lockUserType=1")

    for form1 in br.forms():
        form = form1

    br.select_form(nr=0)

    form["username"] = username
    form["password"] = password

    response = br.submit()

    return br.open("https://cagr.sistemas.ufsc.br/modules/aluno/historicoEscolar")

def get_IAA(text, size):
    for i in range(0,2):
        size = text.rfind("IAA", 0, size)

        inicio = size
        fim = text.find("IAP", inicio, len(text))
    text = strip_tags(text [inicio + 4:fim])
    text = [t.replace(',', '.') for t in text]
    IAA = text[1:len(text)-1]
    return float("".join(IAA))

def get_cargaHoraria(text, size):
    inicio = text.rfind("total:", 0, size)
    fim = text.find(" a", inicio, size)
    text = text [inicio + 7 : fim - 2]
    return int(text)

def get_nome(text, size):
    inicio = text.find("rich-panel-header", 0, size)
    inicio = text.find(">", inicio, size)
    fim = text.find("<", inicio, size)
    text = text [inicio + 1:fim]
    return text

#PROGRAMA COMECA AQUI

username = raw_input("Insira sua matrícula:\n")
password = getpass.getpass("\nInsira sua senha do CAGR:\n")

response = conectar_CAGR(username, password);

text_file = open("output.txt", "w")
text_file.write(response.read())
text_file.close()

pagina = open('output.txt').read()

IAA = get_IAA(pagina, len(pagina))
cargaHoraria = get_cargaHoraria(pagina, len(pagina))
nome = get_nome(pagina,len(pagina))

print "Olá " + nome + "!"
print "Atualmente seu IAA é " + str(IAA) + " e sua carga horária total cursada é de " + str(cargaHoraria) + " horas"

totalAulas = int(raw_input("\nInsira a quantidade de matérias que você está cursando atualmente:\n"))

horasAulasTotal = 0
somatorio = 0
for i in range(0,totalAulas):
    horasAulas = int(raw_input("Insira a quantidade de horas/aula da matéria " + str(i+1) + "\n"))
    horasAulasTotal += horasAulas
    notaAula = float(raw_input("Insira a nota da matéria " + str(i+1) + "\n"))
    somatorio += notaAula*horasAulas
horasAulasTotal += cargaHoraria
somatorio += IAA*cargaHoraria

print "De acordo com o que você me informou, seu possível IAA será " + str("{0:.2f}".format(somatorio/horasAulasTotal))

os.remove("output.txt")