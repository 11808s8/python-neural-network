
ultimo_id_neuronio = 0

quanto_em_quanto_faz_checkpoint = 250
nome_arquivo_checkpoint = 'backup-rede-neuralzinha-'
extensao_checkpoint = '.nn'

le_de_arquivo = False

somente_testa = True

momentum = 0.9

taxa_aprendizagem = 0.1

quantidade_neuronios_camada_escondida = 42
quantidade_neuronios_camada_saida = 36
quantidade_neuronios_camada_entrada = 48

def remove_ponto(string):
    return string.replace('.','')