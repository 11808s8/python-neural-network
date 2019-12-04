from neuronio import Neuronio
from settings import ultimo_id_neuronio
from camada import Camada
import random

class CamadaSaida(Camada):
    '''Camada que herda as funcionalidades de uma camada comum,
        mas possui especificidades da camada de saída, como:
            Leitura de saída esperada
    '''
    def __init__(self, quantos_neuronios):
        super(CamadaSaida, self).__init__(quantos_neuronios)
        self.saida_esperada = []
    

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
              
    def retorna_saida_esperada_formatada(self):
        return ''.join(self.saida_esperada)

    def retorna_saida_neuronios_formatada(self):
        saida_formatada = self.__formata_saida_neuronios__()
        return ''.join(saida_formatada)

    def print_saida_neuronios(self):
        print(self.retorna_saida_neuronios_formatada())

    def __formata_saida_neuronios__(self):
        valor_maximo = max(neuronio.saida for neuronio in self.neuronios)
        return [ '1' if neuronio.saida >= valor_maximo else '0' for neuronio in self.neuronios ]

    def print_saida_esperada_neuronios(self):
        print(''.join(self.saida_esperada))


    def popula_saida_esperada(self, lista_saida_esperada):
        self.saida_esperada = lista_saida_esperada

    def fator_erro_camada_saida(self):
        for i  in range(len(self.neuronios)):
            self.neuronios[i].fator_erro = float(self.saida_esperada[i]) - float(self.neuronios[i].saida)
        return self.neuronios
        
    def calculo_fator_erro_erro_saida(self):
        self.neuronios = self.fator_erro_camada_saida()
        
        for i in range(len(self.neuronios)):
            self.neuronios[i].calculo_erro()
    
    def reconheceu_saida(self):
        return True if ''.join(self.__formata_saida_neuronios__()) == ''.join(self.saida_esperada) else False