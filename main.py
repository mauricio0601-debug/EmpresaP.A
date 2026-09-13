import os
from colorama import Fore, Style, init

init()

ARQUIVO = "Produto.txt"

def produto_ja_existe(nome_produto):
    if not os.path.exists(ARQUIVO):
        return False

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(";")

            produto_atual = dados[0].replace("nome do produto: ", "").strip()

            if produto_atual.lower() == nome_produto.lower():
                return True

    return False

def titulo(texto):
    print(Fore.BLUE + "\n" + "=" * 70)
    print(texto.center(70))
    print("=" * 70 + Style.RESET_ALL)

def cadastrar_produto():
    titulo("CADASTRAR PRODUTO")

    while True:
        produto = input(Fore.LIGHTBLACK_EX + "Digite o nome do produto: \n" + Style.RESET_ALL)
        if produto =="":
            print(Fore.YELLOW + "não pode espaços vazios\n" + Style.RESET_ALL)
        elif produto_ja_existe(produto):
            print(Fore.YELLOW + "não produtos de mesmo nome, se deseja alterar alguma informação use a seção de alterar produto\n" + Style.RESET_ALL)
        elif produto.replace(" ", "").isalpha():
            break
        else:
            print(Fore.YELLOW + "Digite apens letras\n" + Style.RESET_ALL)
    while True:
        try:
            preco = float(input(Fore.LIGHTBLACK_EX + "Digite o preço do produto: \n" + Style.RESET_ALL).replace(",", "."))

            if preco > 0:
                break
            else:
                print(Fore.YELLOW + "Digite números acima de 0 \n" + Style.RESET_ALL)
        except ValueError:
            print(Fore.YELLOW + "Digite apenas números\n" + Style.RESET_ALL)

    while True:
            try:
                quantidade = int(input(Fore.LIGHTBLACK_EX + "Digite a quantidade do produto: \n" + Style.RESET_ALL))
    
                if quantidade > 0:
                    break
                else:
                    print(Fore.YELLOW + "Digite números acima de 0\n" + Style.RESET_ALL)
            except ValueError:
                print(Fore.YELLOW + "Digite apenas números (ou) números inteiros\n" + Style.RESET_ALL)

    

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                produto_existente = linha.strip().split(";")[0]

                if produto_existente.lower() == produto.lower():
                    print(Fore.RED + "produto já cadastrado\n" + Style.RESET_ALL)
                    return

    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"nome do produto: {produto}; preço R$:{preco}; quantidade:{quantidade}\n")

    print(Fore.GREEN + f"Produto cadastrado com sucesso | Nome: {produto} | Preço: R$ {preco} | Quantidade: {quantidade}" + Style.RESET_ALL)


def listar():
    titulo("PRODUTOS CADASTRADOS")

    print(Fore.BLUE + "=" * 75 + Style.RESET_ALL)
    print(f"{'PRODUTO':<35}{'PREÇO':>10}{'QUANTIDADE':>20}")
    print(Fore.BLUE + "-" * 70 + Style.RESET_ALL)

    if not os.path.exists(ARQUIVO):
        print(Fore.RED + "Arquivo de cadastro inexistente!\n" + Style.RESET_ALL)
        return

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        produtos = arquivo.readlines()

    if len(produtos) == 0:
        print(Fore.YELLOW + "Nenhum produto cadastrado.\n" + Style.RESET_ALL)
        return

    for linha in produtos:
        dados = linha.strip().split(";")

        produto = dados[0].replace("nome do produto: ", "")
        preco = float(dados[1].replace(" preço R$:", ""))
        quantidade = int(dados[2].replace(" quantidade:", ""))  
        print(f"{produto:<35}R$ {preco:>10.2f}{quantidade:>14}")

    print(Fore.BLUE + "=" * 70 + Style.RESET_ALL)

def alterar_produto():
    titulo("ALTERAR PRODUTO")

    if not os.path.exists(ARQUIVO):
        print(Fore.RED + "Arquivo de cadastro inexistente!\n" + Style.RESET_ALL)
        return

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        produtos = arquivo.readlines()

    if len(produtos) == 0:
        print(Fore.YELLOW + "Nenhum produto cadastrado.\n" + Style.RESET_ALL)
        return

    nome_busca = input(Fore.BLUE + "Digite o nome do produto que deseja alterar: \n" + Style.RESET_ALL).strip()

    encontrado = False
    nova_lista = []

    for linha in produtos:
        dados = linha.strip().split(";")

        produto_atual = dados[0].replace("nome do produto: ", "")

        if produto_atual.lower() == nome_busca.lower():
            encontrado = True

            while True:
                novo_nome = input(Fore.LIGHTBLACK_EX + "DIGITE O NOVO NOME DO PRODUTO:\n" + Style.RESET_ALL)

                if novo_nome.strip() == "":
                    print(Fore.YELLOW + "NÃO PODE CONTER ESPAÇOS VAZIOS\n" + Style.RESET_ALL)
                elif novo_nome.lower() != produto_atual.lower() and produto_ja_existe(novo_nome):
                    print(Fore.YELLOW + "Esse produto já está cadastrado\n" + Style.RESET_ALL)
                elif novo_nome.replace(" ", "").isalpha():
                    break
                else:
                    print(Fore.YELLOW + "DIGITE APENAS LETRAS\n" + Style.RESET_ALL)

            while True:
                entrada_preco = input(Fore.LIGHTBLACK_EX + "DIGITE O NOVO PREÇO DO PRODUTO:\n" + Style.RESET_ALL).strip()

                try:
                    novo_preco = float(entrada_preco.replace(",", "."))

                    if novo_preco > 0:
                        break
                    else:
                        print(Fore.YELLOW + "DIGITE NÚMEROS ACIMA DE 0\n" + Style.RESET_ALL)

                except ValueError:
                    print(Fore.YELLOW + "DIGITE APENAS NÚMEROS\n" + Style.RESET_ALL)

            while True:
                entrada_qtd = input(Fore.LIGHTBLACK_EX + "DIGITE A NOVA QUANTIDADE DO PRODUTO:\n" + Style.RESET_ALL).strip()

                try:
                    nova_quantidade = int(entrada_qtd)

                    if nova_quantidade > 0:
                        break
                    else:
                        print(Fore.YELLOW + "DIGITE NÚMEROS ACIMA DE 0\n" + Style.RESET_ALL)

                except ValueError:
                    print(Fore.YELLOW + "DIGITE APENAS NÚMEROS INTEIROS\n" + Style.RESET_ALL)

            nova_lista.append(
                f"nome do produto: {novo_nome}; preço R$:{novo_preco}; quantidade:{nova_quantidade}\n"
            )

        else:
            nova_lista.append(linha)

    if not encontrado:
        print(Fore.RED + "Produto não encontrado!\n" + Style.RESET_ALL)
        return

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(nova_lista)

    print(Fore.GREEN + f"Produto alterado com sucesso | Nome: {novo_nome} | Preço: R$ {novo_preco} | Quantidade: {nova_quantidade}" + Style.RESET_ALL)


def excluir_produto():
    titulo("EXCLUIR PRODUTO")

    if not os.path.exists(ARQUIVO):
        print(Fore.RED + "Arquivo de cadastro inexistente!\n" + Style.RESET_ALL)
        return

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        produtos = arquivo.readlines()

    if len(produtos) == 0:
        print(Fore.YELLOW + "Nenhum produto cadastrado.\n" + Style.RESET_ALL)
        return

    produto_busca = input(Fore.BLUE + "Digite o nome do produto que deseja excluir: \n" + Style.RESET_ALL).strip()

    encontrado = False
    nova_lista = []

    for linha in produtos:
        dados = linha.strip().split(";")
        produto_atual = dados[0].replace("nome do produto: ", "")

        if produto_atual.lower() == produto_busca.lower():
            encontrado = True
        else:
            nova_lista.append(linha)

    if not encontrado:
        print(Fore.RED + "Produto não encontrado!\n" + Style.RESET_ALL)
        return

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(nova_lista)

    print(Fore.GREEN + "Produto excluído com sucesso!\n" + Style.RESET_ALL)


cadastrar_produto()
alterar_produto()