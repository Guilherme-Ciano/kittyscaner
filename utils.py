from enum import Enum

class Cores(Enum):
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    RESET = '\033[0m'
    
def showMessage(mensagem, cor):
    cor_ansi = cor.value
    mensagem_colorida = f"{cor_ansi}{mensagem}{Cores.RESET.value}"
    print(mensagem_colorida)

def formatar_tamanho(tamanho_bytes):
    # Função auxiliar para formatar o tamanho para GB ou MB
    gb = tamanho_bytes / (1024 ** 3)
    mb = tamanho_bytes / (1024 ** 2)

    if gb >= 1:
        return f"{gb:.2f} GB"
    elif mb >= 1:
        return f"{mb:.2f} MB"
    else:
        return f"{tamanho_bytes} Bytes"