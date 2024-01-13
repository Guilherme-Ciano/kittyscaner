from tabulate import tabulate
import subprocess

# Utils
from utils import showMessage, Cores

def obter_dispositivos_bluetooth():
    try:
        # Executa o comando hcitool para encontrar dispositivos Bluetooth
        resultado_hcitool = subprocess.run(['hcitool', 'scan'], capture_output=True, text=True)
        saida_hcitool = resultado_hcitool.stdout

        # Extrai os dados dos dispositivos Bluetooth encontrados
        dispositivos = []
        for linha in saida_hcitool.split('\n'):
            partes = linha.split()
            if len(partes) == 2:
                mac = partes[0]
                nome_dispositivo = partes[1]
                dispositivos.append({
                    "Nome do Dispositivo": nome_dispositivo,
                    "Endereço MAC": mac
                })

        return dispositivos

    except Exception as e:
        showMessage(f"=-= [!] Ocorreu um erro: {e}", Cores.VERMELHO)
        return []

def scan_dispositivos_bluetooth():
    dispositivos_bluetooth = obter_dispositivos_bluetooth()
    if dispositivos_bluetooth:
        # Converte a lista de dicionários em uma tabela formatada
        tabela_formatada = tabulate(dispositivos_bluetooth, headers="keys", tablefmt="fancy_grid")
        showMessage("=-= [@] Dispositivos Bluetooth encontrados:", Cores.CIANO)
        showMessage(tabela_formatada, Cores.CIANO)
    else:
        showMessage("=-= [!] Nenhum dispositivo Bluetooth encontrado.", Cores.VERMELHO)

if __name__ == "__main__":
    scan_dispositivos_bluetooth()
