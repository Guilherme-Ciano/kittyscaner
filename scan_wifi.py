from tabulate import tabulate
import subprocess

# Utils
from utils import Cores, showMessage

def obter_redes_wifi():
    try:
        # Executa o comando nmcli para listar redes Wi-Fi
        resultado_nmcli = subprocess.run(['nmcli', '-f', 'SSID,CHAN,SECURITY', 'device', 'wifi', 'list'], capture_output=True, text=True)
        saida_nmcli = resultado_nmcli.stdout

        # Extrai os dados das redes Wi-Fi encontradas
        redes_wifi = []
        linhas = saida_nmcli.strip().split('\n')[1:]  # Ignora o cabeçalho
        for linha in linhas:
            partes = linha.split()
            ssid = partes[0]
            canal = partes[1]
            seguranca = partes[2] if len(partes) > 2 else "Sem segurança"
            redes_wifi.append({
                "SSID": ssid,
                "Canal": canal,
                "Segurança": seguranca
            })

        return redes_wifi

    except Exception as e:
        print(f"=-= [!] Ocorreu um erro: {e}")
        return []


def obter_redes_wifi_windows():
    try:
        # Executa o comando netsh para listar redes Wi-Fi
        resultado_netsh = subprocess.run(['netsh', 'wlan', 'show', 'network'], capture_output=True, text=True)
        saida_netsh = resultado_netsh.stdout

        # Extrai os dados das redes Wi-Fi encontradas
        redes_wifi = []
        linhas = saida_netsh.strip().split('\n')
        for i in range(len(linhas)):
            if "SSID" in linhas[i]:
                ssid = linhas[i+1].strip().split(": ")[1]
                canal = "Não disponível"
                seguranca = linhas[i+3].strip().split(": ")[1]
                redes_wifi.append({
                    "SSID": ssid,
                    "Canal": canal,
                    "Segurança": seguranca
                })

        return redes_wifi

    except Exception as e:
        print(f"=-= [!] Ocorreu um erro: {e}")
        return []


def obter_dispositivos_wifi():
    try:
        # Executa o comando nmap para encontrar dispositivos na rede local
        resultado_nmap = subprocess.run(['nmap', '-sn', '192.168.1.0/24'], capture_output=True, text=True)
        saida_nmap = resultado_nmap.stdout

        # Extrai os dados dos dispositivos encontrados
        dispositivos = []
        for linha in saida_nmap.split('\n'):
            if 'Nmap scan report' in linha:
                partes = linha.split()
                ip = partes[4]
                mac = partes[-1]
                dispositivos.append({
                    "Nome do Dispositivo": "Desconhecido",
                    "IP": ip,
                    "Endereço MAC": mac
                })

        return dispositivos

    except Exception as e:
        showMessage(f"=-= [!] Ocorreu um erro: {e}", Cores.VERMELHO)
        return []

def scan_dispositivos_wifi():
    dispositivos_wifi = obter_dispositivos_wifi()
    if dispositivos_wifi:
        # Converte a lista de dicionários em uma tabela formatada
        tabela_formatada = tabulate(dispositivos_wifi, headers="keys", tablefmt="fancy_grid")
        showMessage("=-= [@] Dispositivos WiFi na rede:", Cores.CIANO)
        showMessage(tabela_formatada, Cores.CIANO)
    else:
        showMessage("=-= [!] Nenhum dispositivo WiFi encontrado.", Cores.VERMELHO)

def scan_redes_wifi():
    redes_encontradas_windows = obter_redes_wifi_windows()
    print(redes_encontradas_windows)
    if redes_encontradas_windows:
        # Converte a lista de dicionários em uma tabela formatada
        tabela_formatada = tabulate(redes_encontradas_windows, headers="keys", tablefmt="fancy_grid")
        showMessage("=-= [@] Dispositivos WiFi na rede:", Cores.CIANO)
        showMessage(tabela_formatada, Cores.CIANO)
    else:
        showMessage("=-= [!] Nenhuma rede WiFi encontrada.", Cores.VERMELHO)

def scan_wifi_completo():
    scan_redes_wifi()
    scan_dispositivos_wifi()

if __name__ == "__main__":
    scan_wifi_completo()