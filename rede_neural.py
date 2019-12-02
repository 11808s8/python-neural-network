from camada import Camada
from camada_saida import CamadaSaida
from neuronio import Neuronio
import settings
import json
import time

import matplotlib.pyplot as plt

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
                novo_neuronio = Neuronio(neuronio['id'],[],settings.taxa_aprendizagem, settings.momentum)
                for i in range(len(neuronio['entradas'])):
                    novo_neuronio.entradas.append(Neuronio(neuronio['entradas'][i]['id'],[],settings.taxa_aprendizagem, settings.momentum))
                    novo_neuronio.pesos.append(neuronio['entradas'][i]['peso'])
                nova_camada.neuronios.append(novo_neuronio)
            camadas.append(nova_camada)
        
        return camadas

epocas = 1000

nome_arquivo_leitura = 'novoarquivo_com_saida1.txt'



settings.quantidade_neuronios_camada_saida = 36
settings.quantidade_neuronios_camada_entrada = 48

taxas_aprendizagem = [0.1, 0.3, 0.6, 1]
quantidades_neuronio_camada_escondida = [ 10, 20, 30]

total_linhas_arquivo_treino = conta_linhas_arquivo(nome_arquivo_leitura)


for indice_array_neuronios_camada_escondida in  range(len(quantidades_neuronio_camada_escondida)):
    for indice_array_taxas_aprendizagem in range(len(taxas_aprendizagem)):
        checkpoint_counter = 1 

        settings.taxa_aprendizagem = taxas_aprendizagem[indice_array_taxas_aprendizagem]
        settings.ultimo_id_neuronio = 0 
        settings.quantidade_neuronios_camada_escondida = quantidades_neuronio_camada_escondida[indice_array_neuronios_camada_escondida]

        linha_arquivo_treino = 0
        i=0
        if(settings.le_de_arquivo==True):
            # nome_arquivo_backup_pesos = 'backup-rede-neuralzinha-2248-lr-01.nn'
            nome_arquivo_backup_pesos = settings.nome_arquivo_backup_pesos

            camadas = read_weights_on_file(nome_arquivo_backup_pesos)
            camada_entrada = Camada(settings.quantidade_neuronios_camada_entrada)
            camada_escondida = camadas[0]
            camada_saida = camadas[1]
            camada_entrada.le_camada_entrada(nome_arquivo_leitura,1, settings.ultimo_id_neuronio, settings.taxa_aprendizagem, settings.momentum)
            camada_escondida.atualiza_neuronios(camada_entrada.neuronios)
            nome_arquivo_backup_pesos_split = nome_arquivo_backup_pesos.split('-')
            
            i = int(nome_arquivo_backup_pesos_split[3])
        else:
            
            camada_entrada = Camada(settings.quantidade_neuronios_camada_entrada)

            settings.ultimo_id_neuronio = camada_entrada.le_camada_entrada(nome_arquivo_leitura,1, settings.ultimo_id_neuronio, settings.taxa_aprendizagem, settings.momentum)

            quantos_neuronios_camada_escondida = settings.quantidade_neuronios_camada_escondida

            camada_escondida = Camada(quantos_neuronios_camada_escondida)

            quantos_neuronios_camada_saida = settings.quantidade_neuronios_camada_saida
            camada_saida = CamadaSaida(quantos_neuronios_camada_saida)

            camada_saida.le_saida_esperada(nome_arquivo_leitura,1, linha_arquivo_treino)
            
            # LEITURA DA CAMADA ESCONDIDA
            for indice_neuronio_escondido in range(quantos_neuronios_camada_escondida):
                neuronio_novo = Neuronio(settings.ultimo_id_neuronio,[],settings.taxa_aprendizagem, settings.momentum)

                neuronio_novo.entradas = [ neuronio for neuronio in camada_entrada.neuronios ]
                neuronio_novo.pesos = [ camada_escondida.__gera_peso_aleatorio__() for neuronio in camada_entrada.neuronios ]
                camada_escondida.neuronios.append(neuronio_novo)
                settings.ultimo_id_neuronio += 1
                    # camada_escondida.neuronios.append(neuronio)

            # LEITURA DA CAMADA DE SAÍDA
            for _ in range(quantos_neuronios_camada_saida):
                    neuronio_novo = Neuronio(settings.ultimo_id_neuronio, [],settings.taxa_aprendizagem, settings.momentum)
                    for neuronio in camada_escondida.neuronios:
                            neuronio_novo.entradas.append(neuronio)
                            neuronio_novo.pesos.append(camada_saida.__gera_peso_aleatorio__())
                            # neuronio_novo.pesos_antigos.append(neuronio_novo.pesos[-1])
                    camada_saida.neuronios.append(neuronio_novo)
                    settings.ultimo_id_neuronio += 1

        print('Rodando treinamento para')
        print('taxa de aprendizagem: ' + str(settings.taxa_aprendizagem))
        print('neuronios camada escondida: ' + str(settings.quantidade_neuronios_camada_escondida))
        settings.ultimo_id_neuronio = 0 
        

        # TREINAMENTO EM ORDEM DO PDF...
        if(settings.somente_testa == False):
            while(i <epocas):
                if(checkpoint_counter % settings.quanto_em_quanto_faz_checkpoint == 0):
                    nome_arquivo_backup = './backups/' + settings.nome_arquivo_checkpoint  + str(i) + '-lr-' + settings.remove_ponto(str(settings.taxa_aprendizagem)) + '-momentum-' + settings.remove_ponto(str(settings.momentum)) + '-neurons-' + str(settings.quantidade_neuronios_camada_escondida) + settings.extensao_checkpoint
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

quantos_reconheceu = 0
quantos_nao_reconheceu = 0

classes = {}

with open(nome_arquivo_leitura, 'r') as arquivo_treino:
    for linha in arquivo_treino:
        linha_quebrada = linha.split(' ')
        classes[linha_quebrada[1]] = { 'id' : linha_quebrada[2].replace('\n',''), 'quanto_reconheceu' : 0}
        
print(classes)
classes_avaliacao = {}
for classe in classes:
    # classes_avaliacao[] = {'id': classe['id'], 'avaliacao':{}}
    # print(classes[classe])
    # exit()
    classes_avaliacao[classe] = {}
    classes_avaliacao[classe]['id'] = classes[classe]['id']
    classes_avaliacao[classe]['avaliacao'] = {}
    for classe_interna in classes:
        classes_avaliacao[classe]['avaliacao'][classe_interna] = 0 
        # classes_avaliacao[classe]['avaliacao']['quanto_reconheceu'] =  0
    # for classe_interna in classes_avaliacao:
    # print(json.dumps(classes_avaliacao[classe], indent=4))
    # input()

# print(classes_avaliacao)
# print(json.dumps(classes_avaliacao, indent=4))
# exit()
for i in range(tamanho_arquivo_teste):
    camada_entrada.le_entrada(arquivo_teste,1,i)
    camada_saida.le_saida_esperada(arquivo_teste, 1, i)
    camada_escondida.atualiza_neuronios(camada_entrada.neuronios)
    
    camada_escondida.update_saida()

    # camada_escondida.atualiza_neuronios(camada_escondida.neuronios)
    camada_saida.atualiza_neuronios(camada_escondida.neuronios)

    # Calcula as saídas das camadas de saída

    camada_saida.update_saida()
    
    saida_formatada = camada_saida.retorna_saida_neuronios_formatada()
    saida_esperada_formatada = camada_saida.retorna_saida_esperada_formatada()
    if(saida_esperada_formatada in classes):
        print("Classe!")
        print(classes_avaliacao[saida_formatada]['id'])
        classes_avaliacao[saida_esperada_formatada]['avaliacao'][saida_formatada]+=1
        print(classes_avaliacao[saida_esperada_formatada]['avaliacao'][saida_formatada])
        # input()
    print("Saída do teste")
    camada_saida.print_saida_neuronios()
    print("Saída esperada")
    camada_saida.print_saida_esperada_neuronios()
    if(camada_saida.reconheceu_saida()):
        quantos_reconheceu+=1
    else:
        quantos_nao_reconheceu +=1
    # input()

cabecalho = []

cabecalho = [ classes_avaliacao[classe]['id'] for classe in classes_avaliacao ]
cabecalho.sort()

# input()
# print(cabecalho)
# input()
linhas = []
for classe in classes_avaliacao:
    linhas.append([])
    for classe_interna in classes_avaliacao:
        linhas[len(linhas)-1].append(str(classes_avaliacao[classe]['avaliacao'][classe_interna]))
# print()

with open('matriz_confusao.txt', 'w') as arquivo_escrita:
    arquivo_escrita.write('    ' + ' '.join(cabecalho) + '\n')
    arquivo_escrita.write('    ' + ' '.join([ '-' for i in range(len(cabecalho))]) + '\n')
    pass

i = 0
for linha in linhas:
    linha_formatada = str(cabecalho[i]) + ' | ' + ' '.join(linha)  + '\n'
    i += 1
    with open('matriz_confusao.txt', 'a') as arquivo_escrita:
        arquivo_escrita.write(linha_formatada)


false_positives = []
true_positives = []
true_negatives = []
sensitividades = []
fprs = []
tprs = []
precisoes = []
especificidades = []

for linha in range(len(linhas)):
    
    fp = 0
    
    for coluna in range(len(linhas[linha])):
        if(linha != coluna):
            fp+=int(linhas[linha][coluna])
        if(linha == coluna):
            true_positives.append(int(linhas[linha][coluna]))
            tn = 0
            for i in range(len(linhas)):
                if(linha != i and coluna != i):
                    tn+=int(linhas[i][i])
            true_negatives.append(tn)
    false_positives.append(fp)
    # print("Falso positivo primeiro bobao")
    # print(fp)
    # input()

false_negatives = []
for coluna in range(len(linhas)):
    fn = 0
    
    for linha in range(len(linhas[coluna])):
        if(linha != coluna):
            fn+=int(linhas[linha][coluna])
    false_negatives.append(fn)
for i in range(len(linhas)):
    # print(cabecalho[i])
    # print(str((int(true_positives[i]))))
    # print(str(int(false_negatives[i])))
    # input()
    if((int(true_positives[i])+int(false_negatives[i]))==0):
        sensitividades.append(-1)    
    else:
        sensitividades.append(int(true_positives[i])/(int(true_positives[i])+int(false_negatives[i])))
    if((int(false_positives[i])+int(true_negatives[i]))==0):
        fprs.append(1)
    else:
        fprs.append(int(false_positives[i])/(int(false_positives[i])+int(true_negatives[i])))
    tprs.append(sensitividades[-1])
    
    precisoes.append(int(true_positives[i])/(int(true_positives[i])+int(false_positives[i])))
    especificidades.append(int(true_negatives[i])/(int(true_negatives[i])+int(false_positives[i])))

tprs, fprs =  (list(t) for t in zip(*sorted(zip(tprs, fprs))))

print(false_positives)
print(false_negatives)
print(true_positives)
print(true_negatives)
print("Sensitividades")
print(sensitividades)
print("Precisões")
print(precisoes)
print("Especificidades")
print(especificidades)
print("TPRS")
print(tprs)
print("FPRS")
print(fprs)
# acuracia = (VP+VN)/(VP+FP+VN+FN)
acuracia = (sum(true_positives)+sum(true_negatives))/(sum(true_positives)+sum(false_positives)+sum(true_negatives)+sum(false_negatives))
erro = 1 - acuracia
print("Acuracia")
print(acuracia)
print("Erro")
print(erro)
precisao = (quantos_reconheceu/(quantos_reconheceu+quantos_nao_reconheceu)) * 100
print("Precisão")
print(precisao)

# y_pos = np.arange(len(cabecalho))
# performance = [10,8,6,4,2,1]

# plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
# plt.legend(loc=4)
# plt.show()


fig,((ax1, ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8), (ax9, ax10)) = plt.subplots(5, 2)
ax1.bar(cabecalho, sensitividades, align='center', alpha=0.5)
ax2.bar(cabecalho, precisoes, align='center', alpha=0.5)
ax3.bar(cabecalho, especificidades, align='center', alpha=0.5)
ax4.bar(cabecalho, fprs, align='center', alpha=0.5)
ax5.bar(cabecalho, tprs, align='center', alpha=0.5)
ax6.bar(cabecalho, false_positives, align='center', alpha=0.5)
ax7.bar(cabecalho, false_negatives, align='center', alpha=0.5)
ax8.bar(cabecalho, true_positives, align='center', alpha=0.5)
ax9.plot(fprs,tprs)
ax1.xaxis.labelpad = 4
ax2.xaxis.labelpad = 4
# plt.xticks(y_pos, cabecalho,rotation='vertical')
# ax1.xticks(y_pos, cabecalho)
# ax1.ylabel('Sensitividade')
ax1.set_title('Sensitividades')
ax2.set_title('Precisões')
ax3.set_title('Especificidades')
ax4.set_title('False Positive Rates')
ax5.set_title('True Positive Rates')
ax6.set_title('False Positives')
ax7.set_title('False Negatives')
ax8.set_title('True Positives')
fig.add_subplot(ax1)
fig.add_subplot(ax2)
fig.add_subplot(ax3)
fig.add_subplot(ax4)
fig.add_subplot(ax5)
fig.add_subplot(ax6)
fig.add_subplot(ax7)
fig.add_subplot(ax8)
fig.add_subplot(ax9)
fig.set_size_inches(12,20)

nome_figura = 'output/images/' + settings.nome_arquivo_backup_pesos_sem_extensao + time.strftime("%Y%m%d-%H%M%S") + '.png'
fig.savefig(nome_figura)
# fig = plt.gcf()
# matplotlib.pypl
# ot.show()
# plt.subplots_adjust(hspace=0.41,top=0.94,bottom=0.05)
# plt.show(block=True)