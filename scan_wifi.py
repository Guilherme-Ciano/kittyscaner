from tabulate import tabulate
import subprocess

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
        print(f"Ocorreu um erro: {e}")
        return []

def scan_dispositivos_wifi():
    dispositivos_wifi = obter_dispositivos_wifi()
    if dispositivos_wifi:
        # Converte a lista de dicionários em uma tabela formatada
        tabela_formatada = tabulate(dispositivos_wifi, headers="keys", tablefmt="fancy_grid")
        print("Dispositivos WiFi na rede:")
        print(tabela_formatada)
    else:
        print("Nenhum dispositivo WiFi encontrado.")

if __name__ == "__main__":
    scan_dispositivos_wifi()