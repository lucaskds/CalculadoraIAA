#!/usr/bin/python2
# -*- coding: utf-8 -*-

import mechanize
import getpass

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

def get_history(br):
    hist = "https://cagr.sistemas.ufsc.br/modules/aluno/historicoEscolar/"
    return br.open(hist)

def get_mirror(br):
    mirror = "https://cagr.sistemas.ufsc.br/modules/aluno/espelhoMatricula/"
    return br.open(mirror)

def conectar_CAGR(username, password):
    br = mechanize.Browser()
    cagr_link = ("https://sistemas.ufsc.br/login?service=https%3A%2F%2F"
                "cagr.sistemas.ufsc.br%2Fj_spring_cas_security_check&userType="
                "padrao&convertToUserType=alunoGraduacao&lockUserType=1")
    response = br.open(cagr_link)

    for form1 in br.forms():
        form = form1

    br.select_form(nr=0)

    form["username"] = username
    form["password"] = password

    response = br.submit()

    return br

def get_IAA(text, size):
    for i in range(2):
        size = text.rfind("IAA", 0, size)
        start = size
        end = text.find("IAP", start, len(text))
    text = strip_tags(text [start + 4:end])
    text = [t.replace(',', '.') for t in text]
    IAA = text[1:len(text)-1]
    try:
        return float("".join(IAA))
    except:
        print("Problema de autenticação!")

def get_cargaHoraria(text):
    size = len(text)
    start = text.rfind("total:", 0, size)
    end = text.find(" a", start, size)
    text = text[start+7:end-2]
    return int(text)

def get_nome(text):
    size = len(text)
    start = text.find("rich-panel-header", 0, size)
    start = text.find(">", start, size)
    end = text.find("<", start, size)
    text = text[start+1:end]
    return text

def get_length(text):
    ret = 0
    size = len(text)
    types = [">Ob<",">Ex<",">Op<"]
    for s in types:
        i = 0
        while i != -1:
            i = text.find(s, i+1, size)
            if i != -1:
                ret += 1
    return ret-1

def dName(text, pos):
    size = len(text)
    strr = "%s:j_id213\">" % pos
    start = text.rfind(strr, 0, size)
    end = text.find("</td>", start, size)
    text = text[start + len(strr):end]
    fixed_text = HTMLParser().unescape(text)
    return fixed_text.encode('utf-8', 'ignore')

def dHA(text, pos):
    size = len(text)
    strr = "%s:j_id219\" style=\"text-align: center\">" % pos
    start = text.rfind(strr, 0, size)
    end = text.find("</td>", start, size)
    text = text[start + len(strr):end]
    return int(text)

username = raw_input("Insira sua matrícula: ")
password = getpass.getpass("Insira sua senha do CAGR: ")

response = conectar_CAGR(username, password);
history = get_history(response)

pagina = history.read()

IAA = get_IAA(pagina, len(pagina))
cargaHoraria = get_cargaHoraria(pagina)
nome = get_nome(pagina)

print("Olá, %s!" % nome)
print("Seu IAA é %.2f e sua carga horária cursada é de %dh." % (IAA, cargaHoraria))

mirror = get_mirror(response)
pagina = mirror.read()
totalAulas = get_length(pagina)
horasAulasTotal, somatorio = 0, 0

for i in range(totalAulas):
    horasAulas = dHA(pagina, i)*18
    horasAulasTotal += horasAulas
    notaAula = float(raw_input("Insira a possível nota em %s: " % dName(pagina, i)))
    while notaAula > 10 or notaAula < 0:
        notaAula = float(raw_input("Nota inválida. Possível nota: "))
    somatorio += notaAula*horasAulas
horasAulasTotal += cargaHoraria
somatorio += IAA*cargaHoraria
IAAFinal = somatorio/horasAulasTotal

print ("Com as notas informadas, seu possível IAA será %.2f." % IAAFinal)
