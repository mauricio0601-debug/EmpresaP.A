from datetime import datetime  # Importa a classe datetime para registrar data e hora no log
from colorama import Fore, Style, init  # Importa cores de texto (Fore), estilos (Style) e init do colorama
import cliente  # Importa o módulo cliente.py, responsável pelo cadastro de clientes
import Cadastro_de_Produtos as produto  # Importa o módulo Cadastro_de_Produtos.py com o apelido "produto"

init()  # Inicializa o colorama para que as cores funcionem corretamente no terminal

ARQUIVO_LOG = "Log_Atividades.txt"  # Define o nome do arquivo onde os logs de atividades serão salvos


def registrar_log(acao):  # Define a função que registra uma ação no arquivo de log
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:  # Abre o arquivo de log em modo "append" (adicionar)
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Obtém a data e hora atuais formatadas
        arquivo.write(f"{agora} - {acao}\n")  # Escreve a linha do log com data, hora e ação realizada


def exibir_menu():  # Define a função que exibe o menu principal
    print(Fore.BLUE + "=" * 40)  # Imprime uma linha azul de 40 sinais de igual
    print("        EMPRESA+ - MENU PRINCIPAL")  # Imprime o título do menu
    print("=" * 40 + Style.RESET_ALL)  # Imprime outra linha de igual e reseta a cor
    print("1 - Cadastrar Cliente")  # Exibe a opção 1 do menu
    print("2 - Cadastrar Produto")  # Exibe a opção 2 do menu
    print("3 - Listar Produtos")  # Exibe a opção 3 do menu
    print("4 - Alterar Produto")  # Exibe a opção 4 do menu
    print("5 - Excluir Produto")  # Exibe a opção 5 do menu
    print("6 - Sair")  # Exibe a opção 6 do menu (encerrar o programa)
    print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)  # Imprime uma linha azul de fechamento do menu


def main():  # Define a função principal do programa
    while True:  # Laço infinito que mantém o menu ativo até o usuário escolher sair
        exibir_menu()  # Exibe o menu principal
        opcao = input("Escolha uma opção: ").strip()  # Solicita ao usuário que escolha uma opção e remove espaços extras

        if opcao == "1":  # Verifica se a opção escolhida foi "1"
            registrar_log("Opção selecionada: Cadastrar Cliente")  # Registra a ação no log
            cliente.main()  # Chama a função principal do módulo cliente para cadastrar um cliente
        elif opcao == "2":  # Verifica se a opção escolhida foi "2"
            registrar_log("Opção selecionada: Cadastrar Produto")  # Registra a ação no log
            produto.cadastrar_produto()  # Chama a função de cadastro de produto do módulo produto
        elif opcao == "3":  # Verifica se a opção escolhida foi "3"
            registrar_log("Opção selecionada: Listar Produtos")  # Registra a ação no log
            produto.listar()  # Chama a função que lista os produtos cadastrados
        elif opcao == "4":  # Verifica se a opção escolhida foi "4"
            registrar_log("Opção selecionada: Alterar Produto")  # Registra a ação no log
            produto.alterar_produto()  # Chama a função que altera um produto existente
        elif opcao == "5":  # Verifica se a opção escolhida foi "5"
            registrar_log("Opção selecionada: Excluir Produto")  # Registra a ação no log
            produto.excluir_produto()  # Chama a função que exclui um produto existente
        elif opcao == "6":  # Verifica se a opção escolhida foi "6"
            registrar_log("Programa encerrado pelo usuário")  # Registra o encerramento do programa no log
            print(Fore.CYAN + "Encerrando o programa..." + Style.RESET_ALL)  # Exibe mensagem de encerramento em ciano
            break  # Sai do laço principal, encerrando o programa
        else:  # Caso a opção digitada não corresponda a nenhuma válida
            print(Fore.YELLOW + "Opção inválida! Digite um número de 1 a 6.\n" + Style.RESET_ALL)  # Avisa que a opção é inválida


if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    main()  # Chama a função principal para iniciar o programa