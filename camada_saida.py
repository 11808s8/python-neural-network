from neuronio import Neuronio
from settings import ultimo_id_neuronio
from camada import Camada
import random

class CamadaSaida(Camada):

    def __init__(self, quantos_neuronios):
        super(CamadaSaida, self).__init__(quantos_neuronios)
        self.saida_esperada = []
    

    # @TODO: ESTE CARA AQUI ESTÁ BUGADO!
    def le_saida_esperada(self, nome_arquivo, quantas_saidas, linha_leitura):
        with open(nome_arquivo, 'r') as arquivo_entrada:
            linha_atual = 0
            quantos_leu = 0
            for linha in arquivo_entrada:
                if(linha_atual == linha_leitura):
                    linha_quebrada = linha.split(' ')[1].split('\n')
                    
                    # Le a saida esperada
                    self.popula_saida_esperada([saida for saida in linha_quebrada[0]])
                    
                    quantos_leu += 1
                    if(quantos_leu == quantas_saidas):
                        # self.exibe_neuronios()
                        break
                else:
                    linha_atual += 1
                


    def popula_saida_esperada(self, lista_saida_esperada):
        self.saida_esperada = lista_saida_esperada

    def fator_erro_camada_saida(self):
        # print(len(self.saida_esperada))
        # print(self.saida_esperada)
        # print([self.neuronios[i].saida for i in range(len(self.neuronios))])
        # input()
        for i  in range(len(self.neuronios)):
            # print(str(float(self.saida_esperada[i])))
            # print(str(float(self.neuronios[i].saida)))
            self.neuronios[i].fator_erro = float(self.saida_esperada[i]) - float(self.neuronios[i].saida)
        return self.neuronios
        # print(self.neuronios[0])
        # print(self.neuronios[0].fator_erro)
        #     print(str(float(self.saida_esperada[i]) - float(self.neuronios[i].saida)))
        # input()

    def calculo_fator_erro_erro_saida(self):
        # print("Fatores erro ANTES (SAIDA)")
        # for i in range(len(self.neuronios)):
        #     print(self.neuronios[i].fator_erro)
        # input()
        # print('t')
        # for i in range(len(self.neuronios)):
        #     print(self.neuronios[i].fator_erro)
        
        # print('t1')
        # print(self.neuronios[0])
        # print(self.neuronios[0].fator_erro)
        # print('22312')
        self.neuronios = self.fator_erro_camada_saida()
        # input()
        # s = ''
        # print([ self.neuronios[i].erro for i in range(len(self.neuronios)) ])
            # print()
        for i in range(len(self.neuronios)):
            self.neuronios[i].calculo_erro()
        # print("Pos erro")
        # print(self.neuronios[0])
        # print(self.neuronios[0].fator_erro)
        # input()
        # input()
        # print("Fatores erro depois")
        # print([ self.neuronios[i].erro for i in range(len(self.neuronios)) ])
        # input()