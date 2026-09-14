from datetime import datetime
from colorama import Fore, Style, init
import cliente
import Cadastro_de_Produtos as produto

init()

ARQUIVO_LOG = "Log_Atividades.txt"


def registrar_log(acao):
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        arquivo.write(f"{agora} - {acao}\n")


def exibir_menu():
    print(Fore.BLUE + "=" * 40)
    print("        EMPRESA+ - MENU PRINCIPAL")
    print("=" * 40 + Style.RESET_ALL)
    print("1 - Cadastrar Cliente")
    print("2 - Cadastrar Produto")
    print("3 - Listar Produtos")
    print("4 - Alterar Produto")
    print("5 - Excluir Produto")
    print("6 - Sair")
    print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            registrar_log("Opção selecionada: Cadastrar Cliente")
            cliente.main()
        elif opcao == "2":
            registrar_log("Opção selecionada: Cadastrar Produto")
            produto.cadastrar_produto()
        elif opcao == "3":
            registrar_log("Opção selecionada: Listar Produtos")
            produto.listar()
        elif opcao == "4":
            registrar_log("Opção selecionada: Alterar Produto")
            produto.alterar_produto()
        elif opcao == "5":
            registrar_log("Opção selecionada: Excluir Produto")
            produto.excluir_produto()
        elif opcao == "6":
            registrar_log("Programa encerrado pelo usuário")
            print(Fore.CYAN + "Encerrando o programa..." + Style.RESET_ALL)
            break
        else:
            print(Fore.YELLOW + "Opção inválida! Digite um número de 1 a 6.\n" + Style.RESET_ALL)


if __name__ == "__main__":
    main()