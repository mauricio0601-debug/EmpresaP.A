import re  # Importa o módulo de expressões regulares, usado para validar e-mail/telefone
import unicodedata  # Importa o módulo para manipulação de caracteres Unicode (remover acentos)
import os  # Importa o módulo do sistema operacional (limpar tela, etc.)
from colorama import Fore, Style, init  # Importa cores de texto (Fore), estilos (Style) e init do colorama

init()  # Inicializa o colorama para que as cores funcionem corretamente no terminal

ARQUIVO = "Cliente.txt"  # Define o nome do arquivo onde os clientes serão salvos


# =========================================================
# FUNÇÕES GERAIS
# =========================================================

def limpar_tela():  # Define a função que limpa o terminal
    """
    Limpa o terminal para impedir que as tentativas anteriores
    fiquem acumuladas na tela.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Executa 'cls' no Windows ou 'clear' em outros sistemas


def remover_acentos(texto):  # Define a função que remove acentos de um texto
    """
    Remove acentos apenas para facilitar algumas validações.
    Exemplo: João -> Joao
    """
    texto_normalizado = unicodedata.normalize("NFD", texto)  # Normaliza o texto separando letras e acentos

    return "".join(  # Junta os caracteres restantes em uma única string
        caractere
        for caractere in texto_normalizado  # Percorre cada caractere do texto normalizado
        if unicodedata.category(caractere) != "Mn"  # Mantém apenas os que não são marcas de acento (Mn)
    )


def encerrar_programa():  # Define a função que encerra o programa de forma amigável
    """
    Permite encerrar o programa de maneira amigável
    quando o usuário pressiona Ctrl+C ou envia EOF.
    """
    print(Fore.CYAN + "\nPrograma encerrado pelo usuário." + Style.RESET_ALL)  # Exibe mensagem de encerramento em ciano
    raise SystemExit  # Lança exceção para finalizar o programa imediatamente


def ler_entrada(mensagem):  # Define função para ler entradas do usuário com tratamento de interrupção
    try:  # Tenta capturar a entrada do usuário
        return input(Fore.LIGHTBLACK_EX + mensagem + Style.RESET_ALL).strip()  # Exibe mensagem colorida e remove espaços extras da resposta
    except (KeyboardInterrupt, EOFError):  # Captura Ctrl+C (KeyboardInterrupt) ou fim de entrada (EOFError)
        encerrar_programa()  # Chama a função que encerra o programa educadamente


def cabecalho():  # Define a função que exibe o cabeçalho do programa
    print(Fore.BLUE + "=" * 40)  # Imprime uma linha azul de 40 sinais de igual
    print("        CADASTRO DE CLIENTES")  # Imprime o título do programa
    print("=" * 40 + Style.RESET_ALL)  # Imprime outra linha de igual e reseta a cor
    print()  # Imprime uma linha em branco para espaçamento


# =========================================================
# NOME
# =========================================================

def validar_nome(nome):  # Define a função que valida o nome digitado
    if not nome:  # Verifica se o nome está vazio
        return None, "Nome inválido! O campo não pode ficar vazio."  # Retorna erro se estiver vazio

    # Substitui vários espaços por apenas um
    nome = " ".join(nome.split())  # Remove espaços duplicados dividindo e reunindo as palavras

    # Remove acentos apenas para validação
    nome_sem_acentos = remover_acentos(nome)  # Gera uma versão sem acentos apenas para checagens

    # Permite letras, espaços, hífen e apóstrofo
    if not all(  # Verifica se todos os caracteres são válidos
        caractere.isalpha()  # Permite letras
        or caractere.isspace()  # Permite espaços
        or caractere in ("-", "'")  # Permite hífen e apóstrofo
        for caractere in nome_sem_acentos  # Percorre cada caractere do nome sem acentos
    ):
        return (  # Retorna erro se algum caractere for inválido
            None,
            "Nome inválido! Use somente letras, espaços, "
            "hífen ou apóstrofo."
        )

    # Considera somente letras para validar o tamanho
    quantidade_letras = sum(  # Soma a quantidade de caracteres que são letras
        caractere.isalpha()  # Verifica se o caractere é uma letra
        for caractere in nome_sem_acentos  # Percorre o nome sem acentos
    )

    if quantidade_letras < 4:  # Verifica se há menos de 4 letras
        return None, "Nome inválido! Digite pelo menos 4 letras."  # Retorna erro se o nome for muito curto

    # Exige pelo menos nome e sobrenome
    partes_nome = (  # Divide o nome em partes (palavras)
        nome.replace("-", " ")  # Substitui hífen por espaço para separar corretamente
        .replace("'", " ")  # Substitui apóstrofo por espaço para separar corretamente
        .split()  # Divide a string em uma lista de palavras
    )

    if len(partes_nome) < 2:  # Verifica se há menos de duas partes (nome e sobrenome)
        return (  # Retorna erro se não houver sobrenome
            None,
            "Digite o nome completo, incluindo pelo menos "
            "um sobrenome."
        )

    # Cada parte deve ter pelo menos 2 letras
    if any(len(parte) < 2 for parte in partes_nome):  # Verifica se alguma parte tem menos de 2 letras
        return (  # Retorna erro se alguma parte for muito curta
            None,
            "Cada parte do nome deve possuir pelo menos 2 letras."
        )

    return nome, None  # Retorna o nome validado e nenhum erro


def cadastrar_nome():  # Define a função que conduz o cadastro do nome
    erro = None  # Inicializa a variável de erro como None

    while True:  # Laço infinito até que o nome seja validado com sucesso
        limpar_tela()  # Limpa a tela antes de exibir o formulário
        cabecalho()  # Exibe o cabeçalho do programa

        if erro:  # Verifica se há mensagem de erro da tentativa anterior
            print(Fore.YELLOW + erro + Style.RESET_ALL)  # Exibe o erro em amarelo
            print()  # Imprime linha em branco

        nome = ler_entrada("Nome completo: ")  # Solicita ao usuário que digite o nome completo

        nome_validado, erro = validar_nome(nome)  # Valida o nome digitado e captura possível erro

        if erro is None:  # Verifica se não houve erro na validação
            return nome_validado  # Retorna o nome validado


# =========================================================
# E-MAIL
# =========================================================

def validar_email(email):  # Define a função que valida o e-mail digitado
    email = email.lower()  # Converte o e-mail para letras minúsculas

    if not email:  # Verifica se o e-mail está vazio
        return None, "E-mail inválido! O campo não pode ficar vazio."  # Retorna erro se estiver vazio

    # Não permite espaços
    if any(caractere.isspace() for caractere in email):  # Verifica se há algum espaço no e-mail
        return None, "E-mail inválido! Não use espaços."  # Retorna erro se houver espaço

    # Deve possuir exatamente um @
    if email.count("@") != 1:  # Verifica se há exatamente um símbolo @
        return (  # Retorna erro se não houver exatamente um @
            None,
            "E-mail inválido! Digite apenas um caractere '@'."
        )

    parte_local, dominio = email.split("@")  # Separa o e-mail em parte local e domínio

    # Aceita somente Gmail
    if dominio != "gmail.com":  # Verifica se o domínio é gmail.com
        return (  # Retorna erro se o domínio não for gmail.com
            None,
            "E-mail inválido! Use um endereço terminado "
            "em @gmail.com."
        )

    if not parte_local:  # Verifica se a parte antes do @ está vazia
        return (  # Retorna erro se não houver nada antes do @
            None,
            "E-mail inválido! Digite algo antes de @gmail.com."
        )

    # Não permite somente números
    if parte_local.isdigit():  # Verifica se a parte local é composta só de números
        return (  # Retorna erro se for somente números
            None,
            "E-mail inválido! A parte antes de @gmail.com "
            "não pode conter somente números."
        )

    # Deve começar e terminar com letra ou número
    if (  # Verifica o primeiro e o último caractere da parte local
        not parte_local[0].isalnum()  # Verifica se o primeiro caractere não é letra/número
        or not parte_local[-1].isalnum()  # Verifica se o último caractere não é letra/número
    ):
        return (  # Retorna erro se início ou fim forem inválidos
            None,
            "E-mail inválido! Comece e termine o endereço "
            "com uma letra ou número."
        )

    # Não permite dois pontos consecutivos
    if ".." in parte_local:  # Verifica se há dois pontos seguidos
        return (  # Retorna erro se houver pontos consecutivos
            None,
            "E-mail inválido! Não use dois pontos consecutivos."
        )

    # Permite letras, números, ponto, hífen e sublinhado
    if not re.fullmatch(r"[a-z0-9._-]+", parte_local):  # Verifica se só há caracteres permitidos
        return (  # Retorna erro se houver caractere não permitido
            None,
            "E-mail inválido! Use somente letras, números, "
            "ponto, hífen ou sublinhado."
        )

    # Exige pelo menos uma letra
    if not any(caractere.isalpha() for caractere in parte_local):  # Verifica se existe ao menos uma letra
        return (  # Retorna erro se não houver nenhuma letra
            None,
            "E-mail inválido! O endereço deve possuir "
            "pelo menos uma letra."
        )

    return email, None  # Retorna o e-mail validado e nenhum erro


def cadastrar_email(nome):  # Define a função que conduz o cadastro do e-mail
    erro = None  # Inicializa a variável de erro como None

    while True:  # Laço infinito até que o e-mail seja validado com sucesso
        limpar_tela()  # Limpa a tela antes de exibir o formulário
        cabecalho()  # Exibe o cabeçalho do programa

        print(Fore.GREEN + f"Nome completo: {nome}" + Style.RESET_ALL)  # Exibe o nome já cadastrado em verde
        print()  # Imprime linha em branco

        if erro:  # Verifica se há mensagem de erro da tentativa anterior
            print(Fore.YELLOW + erro + Style.RESET_ALL)  # Exibe o erro em amarelo
            print()  # Imprime linha em branco

        email = ler_entrada("E-mail Gmail: ")  # Solicita ao usuário que digite o e-mail

        email_validado, erro = validar_email(email)  # Valida o e-mail digitado e captura possível erro

        if erro is None:  # Verifica se não houve erro na validação
            return email_validado  # Retorna o e-mail validado


# =========================================================
# TELEFONE
# =========================================================

def validar_telefone(telefone_digitado):  # Define a função que valida o telefone digitado
    if not telefone_digitado:  # Verifica se o telefone está vazio
        return (  # Retorna erro se estiver vazio
            None,
            "Telefone inválido! O campo não pode ficar vazio."
        )

    # Aceita somente números, espaços e hífen
    if not re.fullmatch(r"[0-9 -]+", telefone_digitado):  # Verifica se só há números, espaços e hífen
        return (  # Retorna erro se houver caractere inválido
            None,
            "Telefone inválido! Use somente números, "
            "espaços e hífen."
        )

    # Remove espaços e hífens
    numeros = re.sub(r"[ -]", "", telefone_digitado)  # Remove espaços e hífens, deixando só os números

    # Exatamente 11 números
    if len(numeros) != 11:  # Verifica se a quantidade de números é diferente de 11
        return (  # Retorna erro se não tiver exatamente 11 dígitos
            None,
            "Telefone inválido! Digite exatamente 11 números, "
            "incluindo o DDD."
        )

    if not numeros.isdigit():  # Verifica se todos os caracteres restantes são dígitos
        return (  # Retorna erro se houver algo que não seja número
            None,
            "Telefone inválido! Digite somente números."
        )

    # Impede número formado por um único dígito repetido
    if len(set(numeros)) == 1:  # Verifica se todos os dígitos são iguais
        return (  # Retorna erro se o número for tipo 11111111111
            None,
            "Telefone inválido! Digite um número de telefone real."
        )

    ddd = numeros[:2]  # Extrai os dois primeiros dígitos como DDD
    nono_digito = numeros[2]  # Extrai o terceiro dígito (deve ser o "9" do celular)

    # DDD entre 11 e 99
    if not 11 <= int(ddd) <= 99:  # Verifica se o DDD está dentro do intervalo válido
        return (  # Retorna erro se o DDD for inválido
            None,
            "Telefone inválido! Digite um DDD válido."
        )

    # Exige celular começando com 9
    if nono_digito != "9":  # Verifica se o terceiro dígito é "9"
        return (  # Retorna erro se não for um número de celular
            None,
            "Telefone inválido! Para este cadastro, informe um "
            "celular com 9 dígitos após o DDD."
        )

    # Formata telefone
    telefone_formatado = (  # Monta a string final formatada do telefone
        f"{numeros[:2]} {numeros[2:7]}-{numeros[7:]}"  # Formato: DDD 9XXXX-XXXX
    )

    return telefone_formatado, None  # Retorna o telefone formatado e nenhum erro


def cadastrar_telefone(nome, email):  # Define a função que conduz o cadastro do telefone
    erro = None  # Inicializa a variável de erro como None

    while True:  # Laço infinito até que o telefone seja validado com sucesso
        limpar_tela()  # Limpa a tela antes de exibir o formulário
        cabecalho()  # Exibe o cabeçalho do programa

        print(Fore.GREEN + f"Nome completo: {nome}" + Style.RESET_ALL)  # Exibe o nome já cadastrado
        print(Fore.GREEN + f"E-mail: {email}" + Style.RESET_ALL)  # Exibe o e-mail já cadastrado
        print()  # Imprime linha em branco

        if erro:  # Verifica se há mensagem de erro da tentativa anterior
            print(Fore.YELLOW + erro + Style.RESET_ALL)  # Exibe o erro em amarelo
            print()  # Imprime linha em branco

        telefone = ler_entrada(  # Solicita ao usuário que digite o telefone
            "Telefone (exemplo: 11 91234-9123): "
        )

        telefone_validado, erro = validar_telefone(telefone)  # Valida o telefone digitado e captura possível erro

        if erro is None:  # Verifica se não houve erro na validação
            return telefone_validado  # Retorna o telefone validado


# =========================================================
# CONTINUAR
# =========================================================

def perguntar_continuar(nome, email, telefone):  # Define a função que pergunta se o usuário quer continuar
    erro = None  # Inicializa a variável de erro como None

    while True:  # Laço infinito até obter uma resposta válida
        limpar_tela()  # Limpa a tela antes de exibir o resumo
        cabecalho()  # Exibe o cabeçalho do programa

        print(Fore.GREEN + f"Nome completo: {nome}" + Style.RESET_ALL)  # Exibe o nome cadastrado
        print(Fore.GREEN + f"E-mail: {email}" + Style.RESET_ALL)  # Exibe o e-mail cadastrado
        print(Fore.GREEN + f"Telefone: {telefone}" + Style.RESET_ALL)  # Exibe o telefone cadastrado
        print()  # Imprime linha em branco

        print(Fore.BLUE + "-" * 40)  # Imprime uma linha azul de separação
        print("Cliente cadastrado com sucesso!")  # Informa que o cadastro foi concluído
        print("-" * 40 + Style.RESET_ALL)  # Imprime outra linha de separação e reseta a cor
        print()  # Imprime linha em branco

        if erro:  # Verifica se há mensagem de erro da tentativa anterior
            print(Fore.YELLOW + erro + Style.RESET_ALL)  # Exibe o erro em amarelo
            print()  # Imprime linha em branco

        resposta = ler_entrada(  # Solicita ao usuário se deseja cadastrar outro cliente
            "Deseja cadastrar outro cliente? (s/n): "
        ).lower()  # Converte a resposta para minúsculas

        if resposta in ("s", "sim"):  # Verifica se a resposta indica "sim"
            return True  # Retorna True para continuar o cadastro

        if resposta in ("n", "nao", "não"):  # Verifica se a resposta indica "não"
            return False  # Retorna False para encerrar o cadastro

        erro = "Resposta inválida! Digite 's' para sim ou 'n' para não."  # Define erro para resposta inválida


# =========================================================
# PERSISTÊNCIA EM ARQUIVO
# =========================================================

def salvar_cliente_em_arquivo(cliente):  # Define a função que salva um cliente no arquivo de texto
    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:  # Abre o arquivo em modo "append" (adicionar) com codificação utf-8
        arquivo.write(  # Escreve a linha do cliente no arquivo
            f"Nome: {cliente['nome']}; "  # Escreve o nome do cliente
            f"E-mail: {cliente['email']}; "  # Escreve o e-mail do cliente
            f"Telefone: {cliente['telefone']}\n"  # Escreve o telefone do cliente e quebra linha
        )


# =========================================================
# EXIBIÇÃO
# =========================================================

def exibir_cliente(cliente, numero=None):  # Define a função que exibe os dados de um cliente
    if numero is not None:  # Verifica se um número de ordem foi informado
        print(Fore.CYAN + f"CLIENTE {numero}" + Style.RESET_ALL)  # Exibe o número do cliente em ciano

    print(f"Nome: {cliente['nome']}")  # Exibe o nome do cliente
    print(f"E-mail: {cliente['email']}")  # Exibe o e-mail do cliente
    print(f"Telefone: {cliente['telefone']}")  # Exibe o telefone do cliente


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

def main():  # Define a função principal do programa
    clientes = []  # Cria uma lista vazia para armazenar os clientes cadastrados

    limpar_tela()  # Limpa a tela ao iniciar o programa
    cabecalho()  # Exibe o cabeçalho do programa

    while True:  # Laço principal que se repete enquanto o usuário quiser cadastrar clientes

        # -------------------------
        # CADASTRAR NOME
        # -------------------------

        nome = cadastrar_nome()  # Chama a função que cadastra e valida o nome

        # -------------------------
        # CADASTRAR E-MAIL
        # -------------------------

        email = cadastrar_email(nome)  # Chama a função que cadastra e valida o e-mail

        # -------------------------
        # CADASTRAR TELEFONE
        # -------------------------

        telefone = cadastrar_telefone(nome, email)  # Chama a função que cadastra e valida o telefone

        # -------------------------
        # SALVAR CLIENTE
        # -------------------------

        cliente = {  # Cria um dicionário com os dados do cliente
            "nome": nome,  # Armazena o nome no dicionário
            "email": email,  # Armazena o e-mail no dicionário
            "telefone": telefone,  # Armazena o telefone no dicionário
        }

        clientes.append(cliente)  # Adiciona o cliente à lista de clientes
        salvar_cliente_em_arquivo(cliente)  # Salva o cliente no arquivo de texto

        # -------------------------
        # PERGUNTAR SE CONTINUA
        # -------------------------

        continuar = perguntar_continuar(  # Pergunta ao usuário se deseja cadastrar outro cliente
            nome,
            email,
            telefone
        )

        if not continuar:  # Verifica se o usuário não quer continuar
            break  # Sai do laço principal

    # =====================================================
    # FINAL
    # =====================================================

    limpar_tela()  # Limpa a tela antes de exibir o resumo final

    print(Fore.BLUE + "=" * 40)  # Imprime uma linha azul de separação
    print("CADASTRO ENCERRADO")  # Informa que o cadastro foi encerrado
    print("=" * 40 + Style.RESET_ALL)  # Imprime outra linha e reseta a cor
    print(f"Total de clientes cadastrados: {len(clientes)}")  # Exibe o total de clientes cadastrados
    print()  # Imprime linha em branco

    for indice, cliente in enumerate(clientes, start=1):  # Percorre a lista de clientes com índice iniciando em 1
        exibir_cliente(cliente, indice)  # Exibe os dados de cada cliente com seu número
        print()  # Imprime linha em branco entre os clientes


if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    main()  # Chama a função principal para iniciar o programa