from neuronio import Neuronio
# from settings import ultimo_id_neuronio
import random

class Camada:
    '''Classe que define uma camada contendo
        uma lista de neuronios, a quantidade de neuronios
        e o identificador do último neuronio inserido na
        lista, para controle.
        
    '''
    def __init__(self, quantos_neuronios):
        self.neuronios = []
        self.quantos_neuronios = quantos_neuronios
        self.id_ultimo_neuronio = 0


    '''Método que lê as entradas e cria os neurônios de acordo
        nome_arquivo : string
        quantas_entradas : int
        ultimo_id_neuronio : int
        learning_rate : float
        momentum : float
    '''
    def le_camada_entrada(self, nome_arquivo, quantas_entradas, ultimo_id_neuronio, learning_rate,momentum ):
        with open(nome_arquivo, 'r') as arquivo_leitura_entrada:
            quantos_leu = 0
            for linha in arquivo_leitura_entrada:
                linha_quebrada = linha.split(' ')
                for i in linha_quebrada[0]: # pega as ENTRADAS somente (desconsidera saída esperada AINDA)

                    n = Neuronio(ultimo_id_neuronio,i, learning_rate, momentum) # passando peso -1 como teste apenas
                    n.entradas = [float(i)]
                    n.saida = float(i) # coloca entrada na saída para primeira camada
                    self.neuronios.append(n)
                    ultimo_id_neuronio += 1

                quantos_leu += 1
                if(quantos_leu == quantas_entradas):
                    self.exibe_neuronios()
                    break
            return ultimo_id_neuronio
    
    '''Método que lê as entradas
        nome_arquivo : string
        quantas_entradas : int
        ultimo_id_neuronio : int
        learning_rate : float
        momentum : float
    '''
    def le_entrada(self,nome_arquivo, quantas_entradas,qual_pos_le):
        with open(nome_arquivo, 'r') as arquivo_leitura_entrada:
            quantos_leu = 0
            indice_neuronio=0
            linha_leitura=0
            for linha in arquivo_leitura_entrada:
                if(linha_leitura==qual_pos_le):
                    linha_quebrada = linha.split(' ')
                    
                    for i in linha_quebrada[0]: # pega as ENTRADAS somente (desconsidera saída esperada AINDA)
                        self.neuronios[indice_neuronio].saida = i
                        indice_neuronio += 1
                    quantos_leu += 1
                    if(quantos_leu == quantas_entradas):
                        break
                    
                else:
                    linha_leitura += 1

    def __gera_peso_aleatorio__(self):
        return round(random.uniform(0,0.1),4)

    def exibe_neuronios(self):
        for neuronio in self.neuronios:
            print(neuronio)


    def fator_erro_camada_intermediaria(self,proxima_camada):
        
        for i  in range(len(self.neuronios)):
            fator_erro = 0
            for j in range(len(proxima_camada.neuronios)):
                indice_neuronio_conexao = proxima_camada.neuronios[j].retorna_indice_neuronio_entrada_por_id(self.neuronios[i].id)
                fator_erro += (proxima_camada.neuronios[j].erro * proxima_camada.neuronios[j].pesos[indice_neuronio_conexao])
            self.neuronios[i].fator_erro = fator_erro
            
        return self.neuronios


    def atualiza_neuronios(self, novos_neuronios):
        for novo_neuronio in novos_neuronios:
            for i in range(len(self.neuronios)):
                self.neuronios[i].atualiza_entrada_por_id(novo_neuronio)

    def update_pesos(self):
        for i in range(len(self.neuronios)):
            self.neuronios[i].update_pesos()

    def calculo_fator_erro_erro(self, proxima_camada):
        self.neuronios = self.fator_erro_camada_intermediaria(proxima_camada)
        for i in range(len(self.neuronios)):
            self.neuronios[i].calculo_erro()
        
    def update_saida(self):
        for i in range(len(self.neuronios)):
            self.neuronios[i].summation_unit()
            self.neuronios[i].transfer_function()
