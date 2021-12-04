import sys
import os.path


class AnalisadorSintatico():

    def __init__(self):
        self.arquivo_entrada = "tokens.txt"
        self.arquivo_saida = "resp-sint.txt"

        self.arquivo_saida = open(self.arquivo_saida, 'w')

        if not os.path.exists(self.arquivo_entrada):
            print("Arquivo de entrada inexistente")
            self.arquivo_saida.write("Arquivo de entrada inexistente")
            return

        self.arquivo = open(self.arquivo_entrada, 'r')
        self.tokens = self.arquivo.readlines()
        self.arquivo.close()

        self.i = 0
        self.linha_atual = ""
        self.tem_erro = False

    def next_token(self):
        self.i += 1
        self.linha_atual = self.tokens[self.i][self.tokens[self.i].find(
            '->')+2: -1]

    def conteudo_token(self):
        return self.tokens[self.i][: self.tokens[self.i].find('->')]

    def analisa(self):

        while("$" not in self.tokens[self.i]):
            self.tem_erro = False
            manter_linha = self.linha_atual
            anterior = ""
            count_de_parenteses = 0

            while (manter_linha == self.linha_atual):

                if("tok500" in self.tokens[self.i]):
                    self.tem_erro = True
                    self.arquivo_saida.write('Erro Lexico\n')

                elif(anterior == "" or 'tok200' in anterior):
                    if('tok3' in self.tokens[self.i] or 'tok4' in self.tokens[self.i] or 'tok200' in self.tokens[self.i] or 'tok101' in self.tokens[self.i]):
                        if('tok200' in self.tokens[self.i]):
                            count_de_parenteses = count_de_parenteses + 1
                    else:
                        self.tem_erro = True
                        if 'tok2' in anterior:
                            self.arquivo_saida.write(
                                'Erro Sintatico - Entrada invalida apos ( \n')
                        else:
                            self.arquivo_saida.write(
                                'Erro Sintatico - Inicio de programa invalido \n')

                elif('tok3' in anterior or 'tok403' in anterior or 'tok201' in anterior):
                    if(not ('tok1' in self.tokens[self.i] or 'tok201' in self.tokens[self.i])):
                        self.tem_erro = True
                        if 'tok2' in anterior:
                            self.arquivo_saida.write(
                                'Erro Sintatico - Esperado um operador ou ) apos um ) \n')
                        else:
                            self.arquivo_saida.write(
                                'Erro Sintatico - Esperado um operador ou ) apos um numero \n')
                    elif ('tok201' in self.tokens[self.i]):
                        count_de_parenteses = count_de_parenteses - 1

                elif('tok1' in anterior):
                    if 'tok106' in anterior:
                        self.tem_erro = True
                        self.arquivo_saida.write(
                            'Erro Sintatico - Nao pode existir informacao depois de fatorial \n')
                    else:
                        if not(('tok3' in self.tokens[self.i]) or ('tok200' in self.tokens[self.i])):
                            self.tem_erro = True
                            self.arquivo_saida.write(
                                'Erro Sintatico - Esperado um numero ou ( apos um operador \n')
                        elif ('tok200' in self.tokens[self.i]):
                            count_de_parenteses = count_de_parenteses + 1

                elif ('tok4' in anterior):
                    if not 'tok200' in self.tokens[self.i]:
                        self.tem_erro = True
                        self.arquivo_saida.write(
                            'Erro Sintatico - Esperado um ( apos uma palavra reservada \n')
                    else:
                        count_de_parenteses = count_de_parenteses + 1

                anterior = self.conteudo_token()

                self.next_token()

                if not (manter_linha == self.linha_atual):
                    if not self.tem_erro:
                        if count_de_parenteses == 0:
                            self.arquivo_saida.write('Cadeia de tokens ok\n')
                        elif (count_de_parenteses > 0):
                            self.arquivo_saida.write(
                                'Erro Sintatico - Faltou algum )\n')
                        else:
                            self.arquivo_saida.write(
                                'Erro Sintatico - Faltou algum (\n')

                if("$" in self.tokens[self.i]):
                    self.arquivo_saida.close()
                    return
