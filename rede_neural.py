from camada import Camada
from camada_saida import CamadaSaida
from neuronio import Neuronio
import settings
import json

def conta_linhas_arquivo(arquivo):
    with open(arquivo, 'r') as arquivo_contagem_linhas:
        linhas = 0
        for _ in arquivo_contagem_linhas:
            linhas+=1
        return linhas

def exibe_neuronios_camada(camada):
        for neuronio in camada.neuronios:
                print("Neuronio: " + str(neuronio.id))
                print("Saída: " + str(neuronio.saida))
                print("Erro: " + str(neuronio.erro))
                print("Fator erro: " + str(neuronio.fator_erro))
                print("Pesos: ")
                print(neuronio.pesos)

def exibe_neuronios_camada_saida(camada):
    for neuronio in camada.neuronios:
        print("Neuronio: " + str(neuronio.id))
        print("Saída: " + str(neuronio.saida))
        print("Erro: " + str(neuronio.erro))
        print("Fator erro: " + str(neuronio.fator_erro))
                

def backup_weights_on_file(camadas, tipo_camadas, nome_arquivo_backup):

    json_serializacao = [ {'tipo_camada': tipo_camada, 'neuronios':[], 'total_neuronios':0} for tipo_camada in tipo_camadas] 
    
    for indice_camada in range(len(camadas)):
        
        json_serializacao[indice_camada]['total_neuronios'] = len(camadas[indice_camada].neuronios)

        for n in camadas[indice_camada].neuronios:
            
            json_serializacao[indice_camada]['neuronios'].append({'id':n.id, 'entradas': []})
            
            for indice_peso_entrada in range(len(n.entradas)):
                json_serializacao[indice_camada]['neuronios'][-1]['entradas'].append({'id':n.entradas[indice_peso_entrada].id, 'peso':n.pesos[indice_peso_entrada]})
    
    with open(nome_arquivo_backup, 'w') as arquivo_backup:
        json.dump(json_serializacao,arquivo_backup)
        # arquivo_backup.write(json.dumps(json_serializacao,indent=4,sort_keys=True))
    

def read_weights_on_file(nome_arquivo_backup):
    with open(nome_arquivo_backup,'r') as arquivo_backup:
        print("leitura")
        camadas = []
        json_deserializacao = json.load(arquivo_backup)
        for indice_camada in range(len(json_deserializacao)):
            if(json_deserializacao[indice_camada]['tipo_camada'] == 'output'):
                # print(json_deserializacao[indice_camada]['total_neuronios'])
                # input()
                nova_camada = CamadaSaida(json_deserializacao[indice_camada]['total_neuronios'])
            else:
                nova_camada = Camada(json_deserializacao[indice_camada]['total_neuronios'])
            for neuronio in json_deserializacao[indice_camada]['neuronios']:
                novo_neuronio = Neuronio(neuronio['id'],[])
                for i in range(len(neuronio['entradas'])):
                    novo_neuronio.entradas.append(Neuronio(neuronio['entradas'][i]['id'],[]))
                    novo_neuronio.pesos.append(neuronio['entradas'][i]['peso'])
                nova_camada.neuronios.append(novo_neuronio)
            camadas.append(nova_camada)
        
        return camadas

epocas = 2001

nome_arquivo_leitura = 'novoarquivo_com_saida1.txt'

settings.ultimo_id_neuronio = 0 

checkpoint_counter = 1 

linha_arquivo_treino = 0
total_linhas_arquivo_treino = conta_linhas_arquivo(nome_arquivo_leitura)

if(settings.le_de_arquivo==True):
    nome_arquivo_backup_pesos = 'backup-rede-neuralzinha-1500.nn'

    camadas = read_weights_on_file(nome_arquivo_backup_pesos)
    camada_entrada = Camada(48)
    camada_escondida = camadas[0]
    camada_saida = camadas[1]
    camada_entrada.le_camada_entrada(nome_arquivo_leitura,1, settings.ultimo_id_neuronio)
    camada_escondida.atualiza_neuronios(camada_entrada.neuronios)
    nome_arquivo_backup_pesos_split = nome_arquivo_backup_pesos.split('-')
    
    i = int(nome_arquivo_backup_pesos_split[-1].split('.')[0])
else:
    
    camada_entrada = Camada(48)

    settings.ultimo_id_neuronio = camada_entrada.le_camada_entrada(nome_arquivo_leitura,1, settings.ultimo_id_neuronio)

    quantos_neuronios_camada_escondida = 42

    camada_escondida = Camada(quantos_neuronios_camada_escondida)

    quantos_neuronios_camada_saida = 36
    camada_saida = CamadaSaida(quantos_neuronios_camada_saida)

    camada_saida.le_saida_esperada(nome_arquivo_leitura,1, linha_arquivo_treino)
    
    # LEITURA DA CAMADA ESCONDIDA
    for indice_neuronio_escondido in range(quantos_neuronios_camada_escondida):
        neuronio_novo = Neuronio(settings.ultimo_id_neuronio,[])

        neuronio_novo.entradas = [ neuronio for neuronio in camada_entrada.neuronios ]
        neuronio_novo.pesos = [ camada_escondida.__gera_peso_aleatorio__() for neuronio in camada_entrada.neuronios ]
        camada_escondida.neuronios.append(neuronio_novo)
        settings.ultimo_id_neuronio += 1
            # camada_escondida.neuronios.append(neuronio)

    # LEITURA DA CAMADA DE SAÍDA
    for _ in range(quantos_neuronios_camada_saida):
            neuronio_novo = Neuronio(settings.ultimo_id_neuronio, [])
            for neuronio in camada_escondida.neuronios:
                    neuronio_novo.entradas.append(neuronio)
                    neuronio_novo.pesos.append(camada_saida.__gera_peso_aleatorio__())
                    # neuronio_novo.pesos_antigos.append(neuronio_novo.pesos[-1])
            camada_saida.neuronios.append(neuronio_novo)
            settings.ultimo_id_neuronio += 1



# TREINAMENTO EM ORDEM DO PDF...
if(settings.somente_testa == False):
    while(i <epocas):
        if(checkpoint_counter % settings.quanto_em_quanto_faz_checkpoint == 0):
            nome_arquivo_backup = settings.nome_arquivo_checkpoint  + str(i) + settings.extensao_checkpoint
            backup_weights_on_file([camada_escondida, camada_saida], ['hidden', 'output'], nome_arquivo_backup)

        for linha_arquivo_treino in range(total_linhas_arquivo_treino):
            camada_entrada.le_entrada(nome_arquivo_leitura,1,linha_arquivo_treino)
            camada_saida.le_saida_esperada(nome_arquivo_leitura, 1, linha_arquivo_treino)
            camada_escondida.atualiza_neuronios(camada_entrada.neuronios)
            # camada_escondida.atualiza_neuronios(camada_saida.neuronios)
            camada_saida.atualiza_neuronios(camada_escondida.neuronios)

            # Calcula as saídas das camadas escondidas
            camada_escondida.update_saida()
            camada_saida.atualiza_neuronios(camada_escondida.neuronios)

            # Calcula as saídas das camadas de saída
            camada_saida.update_saida()

            # Calcula o fator de erro e o erro da camada de saída
            camada_saida.calculo_fator_erro_erro_saida()
            
            camada_escondida.atualiza_neuronios(camada_saida.neuronios)

            # Calcula o fator de erro e o erro da camada intermediária
            camada_escondida.calculo_fator_erro_erro(camada_saida)
            
            camada_saida.atualiza_neuronios(camada_escondida.neuronios)

            camada_saida.update_pesos()
            camada_escondida.update_pesos()

        checkpoint_counter += 1


        print("Rodou época " + str(i))
        i+=1



arquivo_teste = 'dataset_teste.txt'
#arquivo_teste = 'teste_dataset_2_entradas.txt'

tamanho_arquivo_teste = conta_linhas_arquivo(arquivo_teste)

for i in range(tamanho_arquivo_teste):
    camada_entrada.le_entrada(arquivo_teste,1,i)
    camada_saida.le_saida_esperada(arquivo_teste, 1, i)
    camada_escondida.atualiza_neuronios(camada_entrada.neuronios)
    
    camada_escondida.update_saida()

    # camada_escondida.atualiza_neuronios(camada_escondida.neuronios)
    camada_saida.atualiza_neuronios(camada_escondida.neuronios)

    # Calcula as saídas das camadas de saída

    camada_saida.update_saida()
    
    print("Saída do teste")
    camada_saida.print_saida_neuronios()
    print("Saída esperada")
    camada_saida.print_saida_esperada_neuronios()
    input()
