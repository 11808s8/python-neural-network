def remove_ponto(string):
    return string.replace('.','')

def gera_nome_arquivo_backup(i):
    return settings.pasta_arquivos_backups + settings.nome_arquivo_checkpoint  + str(i) + '-lr-' + remove_ponto(str(settings.taxa_aprendizagem)) + '-momentum-' + remove_ponto(str(settings.momentum)) + '-neurons-' + str(settings.quantidade_neuronios_camada_escondida) + settings.extensao_checkpoint

def converte_lista_string(lista):
    return ' '.join([ str(item) for item in lista])