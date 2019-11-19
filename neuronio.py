import math

class Neuronio:
    """Classe que define as funcionalidades e atributos de um neurônio.
        A implementação envolve unidade de somatório, transferência 
                                        (gera a saída do neurônio)
        e o cálculo de erro baseado no fator de erro do neurônio.
        Além disso, há a atualização de pesos com base no cálculo considerando: 
                                                    erro e taxa de aprendizagem
    """

    def __init__(self,id, entradas, learning_rate):
        self.id = id
        self.entradas = entradas # x (vetor)
        self.conexoes = []
        self.pesos = []       # w (vetor)
        self.pesos_antigos = []
        self.somatorio = 0
        self.saida = 0
        self.erro = 0
        self.fator_erro = 0
        self.momentum = 0.9
        self.taxa_de_aprendizagem = learning_rate

    def atualiza_entrada_por_id(self, novo_neuronio):
        for i in range(len(self.entradas)):
            if(self.entradas[i].id == novo_neuronio.id):
                self.entradas[i] = novo_neuronio
                # print("Atualizou")


    def retorna_indice_neuronio_entrada_por_id(self, id):
        for i in range(len(self.entradas)):
            if(self.entradas[i].id == id):
                return i
        # print("K")
        # input()
        return -1

    def summation_unit(self):
        self.somatorio = 0

        for i in range(0,len(self.entradas)):
            self.somatorio += (float(self.entradas[i].saida) * self.pesos[i])
        
    def transfer_function(self):
        self.saida = 1/(1+math.exp(-self.somatorio))
        
    def calculo_erro(self):
        self.erro = float(self.saida) * (1.0 - float(self.saida)) * self.fator_erro

    def update_pesos(self):
        
        for i in range(len(self.pesos)):
            self.pesos[i] = self.pesos[i]  + self.taxa_de_aprendizagem * round(float(self.entradas[i].saida),4) * self.erro
            
    # def __str__(self):
    #     return "Neuronio " + str(self.id) + " Entradas: " + str(self.entradas) + " Pesos: " + str(self.pesos)
