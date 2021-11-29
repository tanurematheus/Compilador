# tok1 - Operador
#   tok100 - +
#   tok101 - -
#   tok102 - *
#   tok103 - /
#   tok104 - ^
#   tok105 - %
#   tok106 - !

# tok2 - Delimitador
#   tok200 - (
#   tok201 - )

# tok3 - Numero
# tok300 - Numero Inteiro
# tok301 - Numero Real

# tok4 - Palavra reservada
#   tok400 - cos
#   tok401 - sen
#   tok402 - tg
#   tok403 - pi

# tok500 - ERROS LEXICOS
# Simbolo nao pertencente ao conjunto de simbolos terminais da linguagem
# Numero mal formado
# Fim de arquivo inesperado (comentario de bloco nao fechado)

import sys
import os.path
import string


class AnalisadorLexico():
    def __init__(self):
        self.arquivo_e = "teste.txt"
        self.arquivo_s = "tokens.txt"

    def mudaEntrada(self, string):
        self.arquivo_e = string

    def getEntrada(self):
        return self.arquivo_e

    def getSaida(self):
        return self.arquivo_s

    def ehDigito(self, caracter):
        digito = '0123456789'
        if caracter in digito:
            return True
        return False

    def ehLetra(self, caracter):
        letra = "cosentgpi"
        if caracter in letra:
            return True
        return False

    def ehDelimitador(self, caracter):
        delimitadores = "()"
        if caracter in delimitadores:
            return True
        return False

    def qualTokenDelimitador(self, entrada):
        delimitadores = "()"
        posicao = delimitadores.find(entrada)
        return "tok20"+str(posicao)

    def ehOperador(self, entrada):
        operadores = "+-*/^%!"
        if entrada in operadores:
            return True
        return False

    def qualTokenOperador(self, entrada):
        operadores = "+-*/^%!"
        posicao = operadores.find(entrada)
        return "tok10"+str(posicao)

    def ehReservada(self, entrada):
        reservadas = "cos sen tg pi".split()
        if entrada in reservadas:
            return True
        return False

    def qualTokenReservada(self, entrada):
        reservadas = "cos sen tg pi".split()
        posicao = 0
        for x in reservadas:
            if x == entrada:
                break
            posicao += 1
        return "tok40"+str(posicao)

    def analisa(self):
        arquivo_saida = open(self.arquivo_s, 'w')

        if not os.path.exists(self.arquivo_e):
            arquivo_saida.write("Arquivo de entrada inexistente")
            return

        arquivo = open(self.arquivo_e, 'r')

        linha_programa = arquivo.readline()

        numero_linha = 1

        while linha_programa:
            i = 0
            tamanho_linha = len(linha_programa)

            while i < tamanho_linha:
                caracter_atual = linha_programa[i]

                if (self.ehDelimitador(caracter_atual)):
                    arquivo_saida.write(self.qualTokenDelimitador(
                        caracter_atual)+'_'+caracter_atual+'->'+str(numero_linha)+'\n')

                elif self.ehOperador(caracter_atual):
                    arquivo_saida.write(self.qualTokenOperador(
                        caracter_atual)+'_'+caracter_atual+'->'+str(numero_linha)+'\n')

                # ===================================================================================
                elif (self.ehDigito(caracter_atual)):
                    string_temp = caracter_atual
                    i += 1
                    j = 0
                    if(i < tamanho_linha):
                        caracter_atual = linha_programa[i]

                    while (self.ehDigito(caracter_atual) and (i+1 < tamanho_linha)):
                        string_temp += caracter_atual
                        i += 1
                        caracter_atual = linha_programa[i]

                    if (caracter_atual == '.'):
                        if ((i+1) < tamanho_linha):
                            string_temp += caracter_atual
                            i += 1
                            caracter_atual = linha_programa[i]
                            while self.ehDigito(caracter_atual) and i+1 < tamanho_linha:
                                j += 1
                                string_temp += caracter_atual
                                i += 1
                                caracter_atual = linha_programa[i]
                                if(caracter_atual == '.'):
                                    arquivo_saida.write(
                                        'tok500_Erro Lexico - Numero mal formado - Linha: %d\n' % numero_linha)

                        else:
                            arquivo_saida.write(
                                'tok500_Erro Lexico - Numero mal formado - Linha: %d\n' % numero_linha)

                        if (j > 0):
                            i -= 1
                            arquivo_saida.write(
                                'tok301_'+string_temp+'->'+str(numero_linha)+'\n')
                        else:
                            arquivo_saida.write(
                                'tok500_Erro Lexico - Numero mal formado - Linha: %d\n' % numero_linha)
                    else:
                        i -= 1
                        arquivo_saida.write(
                            'tok300_'+string_temp+'->'+str(numero_linha)+'\n')
                # ===================================================================================

                elif (self.ehLetra(caracter_atual)):
                    string_temp = caracter_atual
                    i += 1
                    while i < tamanho_linha:
                        caracter_atual = linha_programa[i]
                        if (self.ehLetra(caracter_atual)):
                            string_temp += caracter_atual
                        else:
                            i -= 1
                            break
                        i += 1

                    if (self.ehReservada(string_temp)):
                        arquivo_saida.write(self.qualTokenReservada(
                            string_temp)+'_'+string_temp+'->'+str(numero_linha)+'\n')
                    else:
                        arquivo_saida.write(
                            'tok500_Erro Lexico - Palavra reservada invalida - Linha: %d\n' % numero_linha)

                elif caracter_atual != '\n' and caracter_atual != ' ' and caracter_atual != '\t' and caracter_atual != '\r':
                    arquivo_saida.write(
                        'tok500_Erro Lexico - Caracter Invalido: ' + caracter_atual + ' - linha: %d\n' % numero_linha)

                i += 1

            arquivo_saida.write("\n")
            linha_programa = arquivo.readline()
            numero_linha += 1

        arquivo_saida.write('$')

        arquivo.close()

        arquivo_saida.close
