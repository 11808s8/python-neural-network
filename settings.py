import time
# ------ Configurações Rede!
le_de_arquivo = True # vai ler os pesos de um arquivo no formato .nn

somente_testa = True # apenas realizará os testes, após ter os pesos definidos
somente_treina = False # Define se apenas ocorrerá o treinamento, sem testes
gera_graficos = True # Define se serão gerados gráficos ou não

momentum = 0.9 # Não utilizado

taxa_aprendizagem = 0.1

quantidade_epocas = 1000

quanto_em_quanto_faz_checkpoint = 250 # A cada N épocas gera um backup da rede (pesos)

quantidade_neuronios_camada_escondida = 40
quantidade_neuronios_camada_saida = 36
quantidade_neuronios_camada_entrada = 48

# DEFINIR AQUI O NOME DOS DATASETS A SEREM UTILIZADOS

arquivo_teste = DIRETORIO_DATASETS +'dataset_teste.txt'
nome_arquivo_treino = DIRETORIO_DATASETS +'dataset_treino.txt'

# --

# Caso vá ler um arquivo de BACKUP (formato .nn), definir o nome do arquivo abaixo
nome_arquivo_backup_pesos_sem_extensao = 'backup-rede-neuralzinha-999-lr-1-momentum-09-neurons-30'


taxas_aprendizagem = [0.1, 0.3, 0.6, 1] # para varios treinamentos em sequência
quantidades_neuronio_camada_escondida = [ 10, 20, 30] # Para varios treinamentos em sequência

# ---------------------------

ultimo_id_neuronio = 0
debug = False

nome_arquivo_checkpoint = 'backup-rede-neuralzinha-'
extensao_checkpoint = '.nn'

# --- Configuração para leitura de arquivo de backup
pasta_arquivos_backups = './backups/'

nome_arquivo_backup_pesos = pasta_arquivos_backups + '30_neurons/' + nome_arquivo_backup_pesos_sem_extensao + '.nn'

hora_para_arquivos_gerados = time.strftime("%Y%m%d-%H%M%S")

arquivo_matriz_confusao = './confusion_matrix/cm-' + nome_arquivo_backup_pesos_sem_extensao+'-'+hora_para_arquivos_gerados+ '.txt'

arquivo_dados_gerados = './analysis/' + nome_arquivo_backup_pesos_sem_extensao+'-'+hora_para_arquivos_gerados+ '.txt'

DIRETORIO_DATASETS = './datasets/'


destino_figura = 'output/images/' + nome_arquivo_backup_pesos_sem_extensao +'-'+ hora_para_arquivos_gerados + '.png'

