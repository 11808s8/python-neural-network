
ultimo_id_neuronio = 0

quanto_em_quanto_faz_checkpoint = 250
nome_arquivo_checkpoint = 'backup-rede-neuralzinha-'
extensao_checkpoint = '.nn'

pasta_arquivos_backups = './backups/'
nome_arquivo_backup_pesos_sem_extensao = 'backup-rede-neuralzinha-2248-lr-01'
nome_arquivo_backup_pesos = pasta_arquivos_backups + 'old_backups/' + nome_arquivo_backup_pesos_sem_extensao + '.nn'


le_de_arquivo = True

somente_testa = True

momentum = 0.9

taxa_aprendizagem = 0.1

quantidade_neuronios_camada_escondida = 40
quantidade_neuronios_camada_saida = 36
quantidade_neuronios_camada_entrada = 48

def remove_ponto(string):
    return string.replace('.','')

def gera_nome_arquivo_backup(i):
    return pasta_arquivos_backups + nome_arquivo_checkpoint  + str(i) + '-lr-' + remove_ponto(str(taxa_aprendizagem)) + '-momentum-' + remove_ponto(str(momentum)) + '-neurons-' + str(quantidade_neuronios_camada_escondida) + extensao_checkpoint