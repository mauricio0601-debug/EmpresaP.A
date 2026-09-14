import os  # Importa o módulo do sistema operacional (verificar/manipular arquivos)
from colorama import Fore, Style, init  # Importa cores de texto (Fore), estilos (Style) e init do colorama

init()  # Inicializa o colorama para que as cores funcionem corretamente no terminal

ARQUIVO = "Produto.txt"  # Define o nome do arquivo onde os produtos serão salvos

def produto_ja_existe(nome_produto):  # Define a função que verifica se um produto já está cadastrado
    if not os.path.exists(ARQUIVO):  # Verifica se o arquivo de produtos ainda não existe
        return False  # Se o arquivo não existe, o produto não pode existir

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:  # Abre o arquivo para leitura com codificação utf-8
        for linha in arquivo:  # Percorre cada linha do arquivo
            dados = linha.strip().split(";")  # Remove espaços/quebras de linha e separa os campos por ";"

            produto_atual = dados[0].replace("nome do produto: ", "").strip()  # Extrai apenas o nome do produto da linha

            if produto_atual.lower() == nome_produto.lower():  # Compara os nomes ignorando maiúsculas/minúsculas
                return True  # Retorna True se encontrar um produto com o mesmo nome

    return False  # Retorna False se nenhum produto igual foi encontrado

def titulo(texto):  # Define a função que exibe um título formatado
    print(Fore.BLUE + "\n" + "=" * 70)  # Imprime uma linha em branco seguida de uma linha azul de "="
    print(texto.center(70))  # Imprime o texto centralizado em uma largura de 70 caracteres
    print("=" * 70 + Style.RESET_ALL)  # Imprime outra linha de "=" e reseta a cor

def cadastrar_produto():  # Define a função que realiza o cadastro de um novo produto
    titulo("CADASTRAR PRODUTO")  # Exibe o título da seção de cadastro

    while True:  # Laço que se repete até o nome do produto ser válido
        produto = input(Fore.LIGHTBLACK_EX + "Digite o nome do produto: \n" + Style.RESET_ALL)  # Solicita o nome do produto
        if produto =="":  # Verifica se o campo foi deixado em branco
            print(Fore.YELLOW + "não pode espaços vazios\n" + Style.RESET_ALL)  # Avisa que o campo não pode ficar vazio
        elif produto_ja_existe(produto):  # Verifica se já existe um produto com esse nome
            print(Fore.YELLOW + "não produtos de mesmo nome, se deseja alterar alguma informação use a seção de alterar produto\n" + Style.RESET_ALL)  # Avisa sobre duplicidade
        elif produto.replace(" ", "").isalpha():  # Verifica se, sem espaços, o nome contém apenas letras
            break  # Sai do laço pois o nome é válido
        else:  # Caso o nome contenha caracteres inválidos
            print(Fore.YELLOW + "Digite apens letras\n" + Style.RESET_ALL)  # Avisa que só letras são permitidas
    while True:  # Laço que se repete até o preço ser válido
        try:  # Tenta converter a entrada em número decimal
            preco = float(input(Fore.LIGHTBLACK_EX + "Digite o preço do produto: \n" + Style.RESET_ALL).replace(",", "."))  # Solicita o preço e troca vírgula por ponto

            if preco > 0:  # Verifica se o preço é maior que zero
                break  # Sai do laço pois o preço é válido
            else:  # Caso o preço seja zero ou negativo
                print(Fore.YELLOW + "Digite números acima de 0 \n" + Style.RESET_ALL)  # Avisa que o valor deve ser positivo
        except ValueError:  # Captura erro caso a conversão para float falhe
            print(Fore.YELLOW + "Digite apenas números\n" + Style.RESET_ALL)  # Avisa que só números são permitidos

    while True:  # Laço que se repete até a quantidade ser válida
            try:  # Tenta converter a entrada em número inteiro
                quantidade = int(input(Fore.LIGHTBLACK_EX + "Digite a quantidade do produto: \n" + Style.RESET_ALL))  # Solicita a quantidade do produto
    
                if quantidade > 0:  # Verifica se a quantidade é maior que zero
                    break  # Sai do laço pois a quantidade é válida
                else:  # Caso a quantidade seja zero ou negativa
                    print(Fore.YELLOW + "Digite números acima de 0\n" + Style.RESET_ALL)  # Avisa que o valor deve ser positivo
            except ValueError:  # Captura erro caso a conversão para inteiro falhe
                print(Fore.YELLOW + "Digite apenas números (ou) números inteiros\n" + Style.RESET_ALL)  # Avisa que só números inteiros são permitidos

    

    if os.path.exists(ARQUIVO):  # Verifica se o arquivo de produtos já existe
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:  # Abre o arquivo para leitura
            for linha in arquivo:  # Percorre cada linha do arquivo
                produto_existente = linha.strip().split(";")[0]  # Extrai o primeiro campo (nome bruto) da linha

                if produto_existente.lower() == produto.lower():  # Compara com o nome do produto digitado
                    print(Fore.RED + "produto já cadastrado\n" + Style.RESET_ALL)  # Avisa que o produto já está cadastrado
                    return  # Encerra a função sem cadastrar novamente

    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:  # Abre o arquivo em modo "append" (adicionar)
        arquivo.write(f"nome do produto: {produto}; preço R$:{preco}; quantidade:{quantidade}\n")  # Escreve os dados do novo produto no arquivo

    print(Fore.GREEN + f"Produto cadastrado com sucesso | Nome: {produto} | Preço: R$ {preco} | Quantidade: {quantidade}" + Style.RESET_ALL)  # Confirma o cadastro com sucesso


def listar():  # Define a função que lista todos os produtos cadastrados
    titulo("PRODUTOS CADASTRADOS")  # Exibe o título da seção de listagem

    print(Fore.BLUE + "=" * 75 + Style.RESET_ALL)  # Imprime uma linha azul de separação
    print(f"{'PRODUTO':<35}{'PREÇO':>10}{'QUANTIDADE':>20}")  # Imprime o cabeçalho da tabela com colunas alinhadas
    print(Fore.BLUE + "-" * 70 + Style.RESET_ALL)  # Imprime uma linha azul tracejada de separação

    if not os.path.exists(ARQUIVO):  # Verifica se o arquivo de produtos não existe
        print(Fore.RED + "Arquivo de cadastro inexistente!\n" + Style.RESET_ALL)  # Avisa que não há arquivo de cadastro
        return  # Encerra a função pois não há dados a listar

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:  # Abre o arquivo para leitura
        produtos = arquivo.readlines()  # Lê todas as linhas do arquivo em uma lista

    if len(produtos) == 0:  # Verifica se a lista de produtos está vazia
        print(Fore.YELLOW + "Nenhum produto cadastrado.\n" + Style.RESET_ALL)  # Avisa que não há produtos cadastrados
        return  # Encerra a função pois não há dados a listar

    for linha in produtos:  # Percorre cada linha (produto) lida do arquivo
        dados = linha.strip().split(";")  # Remove espaços/quebras de linha e separa os campos por ";"

        produto = dados[0].replace("nome do produto: ", "")  # Extrai o nome do produto
        preco = float(dados[1].replace(" preço R$:", ""))  # Extrai e converte o preço para float
        quantidade = int(dados[2].replace(" quantidade:", ""))  # Extrai e converte a quantidade para inteiro
        print(f"{produto:<35}R$ {preco:>10.2f}{quantidade:>14}")  # Imprime a linha da tabela formatada com os dados do produto

    print(Fore.BLUE + "=" * 70 + Style.RESET_ALL)  # Imprime uma linha azul de fechamento da tabela

def alterar_produto():  # Define a função que altera os dados de um produto existente
    titulo("ALTERAR PRODUTO")  # Exibe o título da seção de alteração

    if not os.path.exists(ARQUIVO):  # Verifica se o arquivo de produtos não existe
        print(Fore.RED + "Arquivo de cadastro inexistente!\n" + Style.RESET_ALL)  # Avisa que não há arquivo de cadastro
        return  # Encerra a função pois não há dados a alterar

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:  # Abre o arquivo para leitura
        produtos = arquivo.readlines()  # Lê todas as linhas do arquivo em uma lista

    if len(produtos) == 0:  # Verifica se a lista de produtos está vazia
        print(Fore.YELLOW + "Nenhum produto cadastrado.\n" + Style.RESET_ALL)  # Avisa que não há produtos cadastrados
        return  # Encerra a função pois não há dados a alterar

    nome_busca = input(Fore.BLUE + "Digite o nome do produto que deseja alterar: \n" + Style.RESET_ALL).strip()  # Solicita o nome do produto a ser alterado

    encontrado = False  # Inicializa a flag indicando se o produto foi encontrado
    nova_lista = []  # Cria uma lista vazia para armazenar as linhas atualizadas do arquivo

    for linha in produtos:  # Percorre cada linha (produto) lida do arquivo
        dados = linha.strip().split(";")  # Remove espaços/quebras de linha e separa os campos por ";"

        produto_atual = dados[0].replace("nome do produto: ", "")  # Extrai o nome do produto atual da linha

        if produto_atual.lower() == nome_busca.lower():  # Compara com o nome buscado, ignorando maiúsculas/minúsculas
            encontrado = True  # Marca que o produto foi encontrado

            while True:  # Laço que se repete até o novo nome ser válido
                novo_nome = input(Fore.LIGHTBLACK_EX + "DIGITE O NOVO NOME DO PRODUTO:\n" + Style.RESET_ALL)  # Solicita o novo nome do produto

                if novo_nome.strip() == "":  # Verifica se o novo nome está vazio
                    print(Fore.YELLOW + "NÃO PODE CONTER ESPAÇOS VAZIOS\n" + Style.RESET_ALL)  # Avisa que o campo não pode ficar vazio
                elif novo_nome.lower() != produto_atual.lower() and produto_ja_existe(novo_nome):  # Verifica se o novo nome já pertence a outro produto
                    print(Fore.YELLOW + "Esse produto já está cadastrado\n" + Style.RESET_ALL)  # Avisa sobre duplicidade de nome
                elif novo_nome.replace(" ", "").isalpha():  # Verifica se, sem espaços, o nome contém apenas letras
                    break  # Sai do laço pois o novo nome é válido
                else:  # Caso o nome contenha caracteres inválidos
                    print(Fore.YELLOW + "DIGITE APENAS LETRAS\n" + Style.RESET_ALL)  # Avisa que só letras são permitidas

            while True:  # Laço que se repete até o novo preço ser válido
                entrada_preco = input(Fore.LIGHTBLACK_EX + "DIGITE O NOVO PREÇO DO PRODUTO:\n" + Style.RESET_ALL).strip()  # Solicita o novo preço do produto

                try:  # Tenta converter a entrada em número decimal
                    novo_preco = float(entrada_preco.replace(",", "."))  # Converte a entrada trocando vírgula por ponto

                    if novo_preco > 0:  # Verifica se o novo preço é maior que zero
                        break  # Sai do laço pois o preço é válido
                    else:  # Caso o preço seja zero ou negativo
                        print(Fore.YELLOW + "DIGITE NÚMEROS ACIMA DE 0\n" + Style.RESET_ALL)  # Avisa que o valor deve ser positivo

                except ValueError:  # Captura erro caso a conversão para float falhe
                    print(Fore.YELLOW + "DIGITE APENAS NÚMEROS\n" + Style.RESET_ALL)  # Avisa que só números são permitidos

            while True:  # Laço que se repete até a nova quantidade ser válida
                entrada_qtd = input(Fore.LIGHTBLACK_EX + "DIGITE A NOVA QUANTIDADE DO PRODUTO:\n" + Style.RESET_ALL).strip()  # Solicita a nova quantidade do produto

                try:  # Tenta converter a entrada em número inteiro
                    nova_quantidade = int(entrada_qtd)  # Converte a entrada para inteiro

                    if nova_quantidade > 0:  # Verifica se a nova quantidade é maior que zero
                        break  # Sai do laço pois a quantidade é válida
                    else:  # Caso a quantidade seja zero ou negativa
                        print(Fore.YELLOW + "DIGITE NÚMEROS ACIMA DE 0\n" + Style.RESET_ALL)  # Avisa que o valor deve ser positivo

                except ValueError:  # Captura erro caso a conversão para inteiro falhe
                    print(Fore.YELLOW + "DIGITE APENAS NÚMEROS INTEIROS\n" + Style.RESET_ALL)  # Avisa que só números inteiros são permitidos

            nova_lista.append(  # Adiciona à nova lista a linha já atualizada do produto
                f"nome do produto: {novo_nome}; preço R$:{novo_preco}; quantidade:{nova_quantidade}\n"  # Monta a nova linha formatada com os dados atualizados
            )

        else:  # Caso a linha não seja do produto buscado
            nova_lista.append(linha)  # Mantém a linha original sem alterações

    if not encontrado:  # Verifica se nenhum produto correspondente foi encontrado
        print(Fore.RED + "Produto não encontrado!\n" + Style.RESET_ALL)  # Avisa que o produto não foi encontrado
        return  # Encerra a função pois não há o que alterar

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:  # Abre o arquivo em modo escrita, sobrescrevendo o conteúdo
        arquivo.writelines(nova_lista)  # Escreve todas as linhas atualizadas de volta no arquivo

    print(Fore.GREEN + f"Produto alterado com sucesso | Nome: {novo_nome} | Preço: R$ {novo_preco} | Quantidade: {nova_quantidade}" + Style.RESET_ALL)  # Confirma a alteração com sucesso


def excluir_produto():  # Define a função que exclui um produto cadastrado
    titulo("EXCLUIR PRODUTO")  # Exibe o título da seção de exclusão

    if not os.path.exists(ARQUIVO):  # Verifica se o arquivo de produtos não existe
        print(Fore.RED + "Arquivo de cadastro inexistente!\n" + Style.RESET_ALL)  # Avisa que não há arquivo de cadastro
        return  # Encerra a função pois não há dados a excluir

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:  # Abre o arquivo para leitura
        produtos = arquivo.readlines()  # Lê todas as linhas do arquivo em uma lista

    if len(produtos) == 0:  # Verifica se a lista de produtos está vazia
        print(Fore.YELLOW + "Nenhum produto cadastrado.\n" + Style.RESET_ALL)  # Avisa que não há produtos cadastrados
        return  # Encerra a função pois não há dados a excluir

    produto_busca = input(Fore.BLUE + "Digite o nome do produto que deseja excluir: \n" + Style.RESET_ALL).strip()  # Solicita o nome do produto a ser excluído

    encontrado = False  # Inicializa a flag indicando se o produto foi encontrado
    nova_lista = []  # Cria uma lista vazia para armazenar as linhas que permanecerão no arquivo

    for linha in produtos:  # Percorre cada linha (produto) lida do arquivo
        dados = linha.strip().split(";")  # Remove espaços/quebras de linha e separa os campos por ";"
        produto_atual = dados[0].replace("nome do produto: ", "")  # Extrai o nome do produto atual da linha

        if produto_atual.lower() == produto_busca.lower():  # Compara com o nome buscado, ignorando maiúsculas/minúsculas
            encontrado = True  # Marca que o produto foi encontrado (e não o adiciona à nova lista)
        else:  # Caso a linha não seja do produto buscado
            nova_lista.append(linha)  # Mantém a linha na nova lista, preservando o produto

    if not encontrado:  # Verifica se nenhum produto correspondente foi encontrado
        print(Fore.RED + "Produto não encontrado!\n" + Style.RESET_ALL)  # Avisa que o produto não foi encontrado
        return  # Encerra a função pois não há o que excluir

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:  # Abre o arquivo em modo escrita, sobrescrevendo o conteúdo
        arquivo.writelines(nova_lista)  # Escreve a lista sem o produto excluído de volta no arquivo

    print(Fore.GREEN + "Produto excluído com sucesso!\n" + Style.RESET_ALL)  # Confirma a exclusão com sucesso