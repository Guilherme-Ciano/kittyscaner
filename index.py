# Utils
from utils import showMessage, Cores

# Scanners
from scan_usb import scan_dispositivos_usb_e_armazenamento
from scan_wifi import scan_wifi_completo
from scan_bluetooth import scan_dispositivos_bluetooth

applicationBanner = ('''
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
   /\_/\    M E O W T D O W N   =-=
  ( o.o )   author: @gui_ciano  =-=
   > ^ <    only for education  =-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=''')

opcoes = {
    1: "Search for Wi-Fi Devices",
    2: "Search for Bluetooth Devices",
    3: "Search for USB Devices",
    99: "Sair"
}

def menu_interativo():
    showMessage(applicationBanner, Cores.CIANO)

    while True:
        for chave, valor in opcoes.items():
            showMessage(f"=-= [{chave}] {valor}", Cores.CIANO)

        showMessage("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", Cores.CIANO)

        # Define códigos de escape ANSI para cores
        COR_CYAN = '\033[96m'
        RESET_COR = '\033[0m'

        # Solicita a entrada do usuário com a cor ciano
        escolha = input(f"{COR_CYAN}=-= > {RESET_COR}")

        try:
            escolha = int(escolha)
            if escolha in opcoes:
                if escolha == 4:
                    print("Saindo do menu.")
                    break
                else:
                    executa_funcao(escolha)
                    break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Digite um número válido.")

def executa_funcao(opcao):
    if opcao == 1:
        scan_wifi_completo()
    elif opcao == 2:
        scan_dispositivos_bluetooth()
    elif opcao == 3:
        scan_dispositivos_usb_e_armazenamento()

if __name__ == "__main__":
    menu_interativo()
