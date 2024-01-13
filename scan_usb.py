import psutil
import platform
# import pywinusb.hid as hid
import subprocess
from tabulate import tabulate

# Utils
from utils import showMessage, formatar_tamanho, Cores

def obter_dispositivos_usb_e_armazenamento():
    dispositivos_usb = []
    informacoes_armazenamento = []

    # Obtém informações sobre dispositivos USB
    if platform.system() == 'Windows':
        dispositivos_usb = obter_dispositivos_usb_windows()
    elif platform.system() == 'Linux':
        dispositivos_usb = obter_dispositivos_usb_linux()

    # Obtém informações sobre espaço de armazenamento
    informacoes_armazenamento = obter_informacoes_armazenamento()

    return dispositivos_usb, informacoes_armazenamento

def obter_dispositivos_usb_linux():
    try:
        # Executa o comando lsusb para listar os dispositivos USB
        resultado_lsusb = subprocess.run(['lsusb'], capture_output=True, text=True)
        saida_lsusb = resultado_lsusb.stdout

        # Extrai os dados dos dispositivos USB encontrados
        dispositivos = []
        for linha in saida_lsusb.split('\n'):
            partes = linha.split()
            if len(partes) >= 6:
                bus = partes[1]
                device = partes[3][:-1]
                descricao = ' '.join(partes[6:])
                dispositivos.append({
                    "Bus": bus,
                    "Device": device,
                    "Descrição": descricao
                })

        return dispositivos

    except Exception as e:
        print(f"Erro ao obter dispositivos USB no Linux: {e}")
        return []

def obter_dispositivos_usb_windows():
    dispositivos = []
    try:
        # Enumera dispositivos USB no Windows usando pywinusb
        filtragem_dispositivos = hid.HidDeviceFilter(vendor_id=0, product_id=0)
        dispositivos = filtragem_dispositivos.get_devices()

        dispositivos_info = []
        for dispositivo in dispositivos:
            dispositivo_info = {
                "Descrição": dispositivo.product_name,
                "VID": hex(dispositivo.vendor_id),
                "PID": hex(dispositivo.product_id)
            }
            dispositivos_info.append(dispositivo_info)

        return dispositivos_info

    except Exception as e:
        print(f"Erro ao obter dispositivos USB no Windows: {e}")
        return []

def obter_informacoes_armazenamento():
    try:
        # Obtém informações sobre o espaço de armazenamento
        particoes = psutil.disk_partitions()

        informacoes_armazenamento = []
        for particao in particoes:
            informacoes = {
                "Dispositivo": particao.device,
                "Ponto de Montagem": particao.mountpoint,
                "Tipo de Sistema": particao.fstype
            }

            try:
                espaco = psutil.disk_usage(particao.mountpoint)
                informacoes["Total"] = formatar_tamanho(espaco.total)
                informacoes["Usado"] = formatar_tamanho(espaco.used)
                informacoes["Disponível"] = formatar_tamanho(espaco.free)
                informacoes["Percentual Usado"] = f"{espaco.percent}%"
            except Exception as e:
                print(f"Erro ao obter informações de espaço de armazenamento: {e}")

            informacoes_armazenamento.append(informacoes)

        return informacoes_armazenamento

    except Exception as e:
        print(f"Erro ao obter informações de espaço de armazenamento: {e}")
        return []
    
def scan_dispositivos_usb_e_armazenamento():
    dispositivos_usb, informacoes_armazenamento = obter_dispositivos_usb_e_armazenamento()

    if dispositivos_usb:
        # Converte a lista de dicionários em uma tabela formatada
        tabela_formatada_dispositivos_usb = tabulate(dispositivos_usb, headers="keys", tablefmt="fancy_grid")
        print("Dispositivos USB conectados:")
        print(tabela_formatada_dispositivos_usb)
    else:
        print("Nenhum dispositivo USB encontrado.")

    if informacoes_armazenamento:
        # Converte a lista de dicionários em uma tabela formatada
        tabela_formatada_armazenamento = tabulate(informacoes_armazenamento, headers="keys", tablefmt="fancy_grid")
        print("\nInformações de armazenamento:")
        print(tabela_formatada_armazenamento)
    else:
        print("Nenhuma informação de armazenamento disponível.")

if __name__ == "__main__":
    scan_dispositivos_usb_e_armazenamento()
