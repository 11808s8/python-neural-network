import random
import settings

''' Script que lê  um arquivo com as entradas codificadas e gera o 
    dataset de teste com base no arquivo lido.
'''

def funcao_escreve_arquivo_novo_sem_letra_identificando():
    with open('novoarquivo_com_saida.txt','w') as arquivo_escrita:
        with open('codificacao_sem_letras.txt') as f:
            lista_saida = [ '0' for i in range(36)]
            lista_saida[-1] = '1'
            onde_esta_i = len(lista_saida)-1
            for linha in f:
                sem_igual = linha.split('=')
                if(len(sem_igual)>1):
                    novalinha = sem_igual[1].replace(' ','').replace('\n', '')
                    arquivo_escrita.write(novalinha + " " + ''.join(lista_saida) + "\n")
                    lista_saida[onde_esta_i] = '0'
                    onde_esta_i -= 1
                    lista_saida[onde_esta_i] = '1'
                    # onde_esta_i -= 1
                    print(novalinha)

def monta_dataset_teste():
    todos_caracteres = []
    bits = None
    with open(nome_arquivo_treino) as novoarquivo:
        for linha in novoarquivo:
            todos_caracteres.append(linha.replace('\n',''))

        with open(arquivo_teste,'w') as dt:
            entradas = random.sample(todos_caracteres,34)
            for entrada in entradas:
                dt.write(entrada + '\n')


    #2% de ruído
    for _ in range(20):
        bits = random.choice(todos_caracteres)
        
        lista_bits = [bits[i] for i in range(len(bits))]

        with open(arquivo_teste,'a') as dt:
            dt.write(quantos_inverte(2,lista_bits) + '\n')

    #6% de ruído
    for _ in range(20):
        bits = random.choice(todos_caracteres)
        
        lista_bits = [bits[i] for i in range(len(bits))]

        with open(arquivo_teste,'a') as dt:
            dt.write(quantos_inverte(6,lista_bits) + '\n')

    #12% de ruído
    for _ in range(20):
        bits = random.choice(todos_caracteres)
        
        lista_bits = [bits[i] for i in range(len(bits))]

        with open(arquivo_teste,'a') as dt:
            dt.write(quantos_inverte(12,lista_bits) + '\n')


def quantos_inverte(quantos, lista_inverte):
    bits_inverte = []
    print("Original "+ ''.join(lista_inverte))
    for _ in range(quantos):
        bits_randomicos = random.randint(0,47)
        while(bits_randomicos in bits_inverte):
            bits_randomicos = random.randint(0,47)
        bits_inverte.append(bits_randomicos)
        lista_inverte[bits_inverte[-1]] = inverte_bit(lista_inverte[bits_inverte[-1]])
    print("Novo     "+ ''.join(lista_inverte))
    return ''.join(lista_inverte)


                    
def inverte_bit(bit):

    if(bit=='0' or bit==0):
        return '1'
    else:
        return '0'

monta_dataset_teste()
# funcao_escreve_arquivo_novo_sem_letra_identificando()
