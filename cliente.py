import re
import unicodedata
import os
from colorama import Fore, Style, init

init()

ARQUIVO = "Cliente.txt"


# =========================================================
# FUNÇÕES GERAIS
# =========================================================

def limpar_tela():
    """
    Limpa o terminal para impedir que as tentativas anteriores
    fiquem acumuladas na tela.
    """
    os.system("cls" if os.name == "nt" else "clear")


def remover_acentos(texto):
    """
    Remove acentos apenas para facilitar algumas validações.
    Exemplo: João -> Joao
    """
    texto_normalizado = unicodedata.normalize("NFD", texto)

    return "".join(
        caractere
        for caractere in texto_normalizado
        if unicodedata.category(caractere) != "Mn"
    )


def encerrar_programa():
    """
    Permite encerrar o programa de maneira amigável
    quando o usuário pressiona Ctrl+C ou envia EOF.
    """
    print(Fore.CYAN + "\nPrograma encerrado pelo usuário." + Style.RESET_ALL)
    raise SystemExit


def ler_entrada(mensagem):
    try:
        return input(Fore.LIGHTBLACK_EX + mensagem + Style.RESET_ALL).strip()
    except (KeyboardInterrupt, EOFError):
        encerrar_programa()


def cabecalho():
    print(Fore.BLUE + "=" * 40)
    print("        CADASTRO DE CLIENTES")
    print("=" * 40 + Style.RESET_ALL)
    print()


# =========================================================
# NOME
# =========================================================

def validar_nome(nome):
    if not nome:
        return None, "Nome inválido! O campo não pode ficar vazio."

    # Substitui vários espaços por apenas um
    nome = " ".join(nome.split())

    # Remove acentos apenas para validação
    nome_sem_acentos = remover_acentos(nome)

    # Permite letras, espaços, hífen e apóstrofo
    if not all(
        caractere.isalpha()
        or caractere.isspace()
        or caractere in ("-", "'")
        for caractere in nome_sem_acentos
    ):
        return (
            None,
            "Nome inválido! Use somente letras, espaços, "
            "hífen ou apóstrofo."
        )

    # Considera somente letras para validar o tamanho
    quantidade_letras = sum(
        caractere.isalpha()
        for caractere in nome_sem_acentos
    )

    if quantidade_letras < 4:
        return None, "Nome inválido! Digite pelo menos 4 letras."

    # Exige pelo menos nome e sobrenome
    partes_nome = (
        nome.replace("-", " ")
        .replace("'", " ")
        .split()
    )

    if len(partes_nome) < 2:
        return (
            None,
            "Digite o nome completo, incluindo pelo menos "
            "um sobrenome."
        )

    # Cada parte deve ter pelo menos 2 letras
    if any(len(parte) < 2 for parte in partes_nome):
        return (
            None,
            "Cada parte do nome deve possuir pelo menos 2 letras."
        )

    return nome, None


def cadastrar_nome():
    erro = None

    while True:
        limpar_tela()
        cabecalho()

        if erro:
            print(Fore.YELLOW + erro + Style.RESET_ALL)
            print()

        nome = ler_entrada("Nome completo: ")

        nome_validado, erro = validar_nome(nome)

        if erro is None:
            return nome_validado


# =========================================================
# E-MAIL
# =========================================================

def validar_email(email):
    email = email.lower()

    if not email:
        return None, "E-mail inválido! O campo não pode ficar vazio."

    # Não permite espaços
    if any(caractere.isspace() for caractere in email):
        return None, "E-mail inválido! Não use espaços."

    # Deve possuir exatamente um @
    if email.count("@") != 1:
        return (
            None,
            "E-mail inválido! Digite apenas um caractere '@'."
        )

    parte_local, dominio = email.split("@")

    # Aceita somente Gmail
    if dominio != "gmail.com":
        return (
            None,
            "E-mail inválido! Use um endereço terminado "
            "em @gmail.com."
        )

    if not parte_local:
        return (
            None,
            "E-mail inválido! Digite algo antes de @gmail.com."
        )

    # Não permite somente números
    if parte_local.isdigit():
        return (
            None,
            "E-mail inválido! A parte antes de @gmail.com "
            "não pode conter somente números."
        )

    # Deve começar e terminar com letra ou número
    if (
        not parte_local[0].isalnum()
        or not parte_local[-1].isalnum()
    ):
        return (
            None,
            "E-mail inválido! Comece e termine o endereço "
            "com uma letra ou número."
        )

    # Não permite dois pontos consecutivos
    if ".." in parte_local:
        return (
            None,
            "E-mail inválido! Não use dois pontos consecutivos."
        )

    # Permite letras, números, ponto, hífen e sublinhado
    if not re.fullmatch(r"[a-z0-9._-]+", parte_local):
        return (
            None,
            "E-mail inválido! Use somente letras, números, "
            "ponto, hífen ou sublinhado."
        )

    # Exige pelo menos uma letra
    if not any(caractere.isalpha() for caractere in parte_local):
        return (
            None,
            "E-mail inválido! O endereço deve possuir "
            "pelo menos uma letra."
        )

    return email, None


def cadastrar_email(nome):
    erro = None

    while True:
        limpar_tela()
        cabecalho()

        print(Fore.GREEN + f"Nome completo: {nome}" + Style.RESET_ALL)
        print()

        if erro:
            print(Fore.YELLOW + erro + Style.RESET_ALL)
            print()

        email = ler_entrada("E-mail Gmail: ")

        email_validado, erro = validar_email(email)

        if erro is None:
            return email_validado


# =========================================================
# TELEFONE
# =========================================================

def validar_telefone(telefone_digitado):
    if not telefone_digitado:
        return (
            None,
            "Telefone inválido! O campo não pode ficar vazio."
        )

    # Aceita somente números, espaços e hífen
    if not re.fullmatch(r"[0-9 -]+", telefone_digitado):
        return (
            None,
            "Telefone inválido! Use somente números, "
            "espaços e hífen."
        )

    # Remove espaços e hífens
    numeros = re.sub(r"[ -]", "", telefone_digitado)

    # Exatamente 11 números
    if len(numeros) != 11:
        return (
            None,
            "Telefone inválido! Digite exatamente 11 números, "
            "incluindo o DDD."
        )

    if not numeros.isdigit():
        return (
            None,
            "Telefone inválido! Digite somente números."
        )

    # Impede número formado por um único dígito repetido
    if len(set(numeros)) == 1:
        return (
            None,
            "Telefone inválido! Digite um número de telefone real."
        )

    ddd = numeros[:2]
    nono_digito = numeros[2]

    # DDD entre 11 e 99
    if not 11 <= int(ddd) <= 99:
        return (
            None,
            "Telefone inválido! Digite um DDD válido."
        )

    # Exige celular começando com 9
    if nono_digito != "9":
        return (
            None,
            "Telefone inválido! Para este cadastro, informe um "
            "celular com 9 dígitos após o DDD."
        )

    # Formata telefone
    telefone_formatado = (
        f"{numeros[:2]} {numeros[2:7]}-{numeros[7:]}"
    )

    return telefone_formatado, None


def cadastrar_telefone(nome, email):
    erro = None

    while True:
        limpar_tela()
        cabecalho()

        print(Fore.GREEN + f"Nome completo: {nome}" + Style.RESET_ALL)
        print(Fore.GREEN + f"E-mail: {email}" + Style.RESET_ALL)
        print()

        if erro:
            print(Fore.YELLOW + erro + Style.RESET_ALL)
            print()

        telefone = ler_entrada(
            "Telefone (exemplo: 11 93942-9439): "
        )

        telefone_validado, erro = validar_telefone(telefone)

        if erro is None:
            return telefone_validado


# =========================================================
# CONTINUAR
# =========================================================

def perguntar_continuar(nome, email, telefone):
    erro = None

    while True:
        limpar_tela()
        cabecalho()

        print(Fore.GREEN + f"Nome completo: {nome}" + Style.RESET_ALL)
        print(Fore.GREEN + f"E-mail: {email}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Telefone: {telefone}" + Style.RESET_ALL)
        print()

        print(Fore.BLUE + "-" * 40)
        print("Cliente cadastrado com sucesso!")
        print("-" * 40 + Style.RESET_ALL)
        print()

        if erro:
            print(Fore.YELLOW + erro + Style.RESET_ALL)
            print()

        resposta = ler_entrada(
            "Deseja cadastrar outro cliente? (s/n): "
        ).lower()

        if resposta in ("s", "sim"):
            return True

        if resposta in ("n", "nao", "não"):
            return False

        erro = "Resposta inválida! Digite 's' para sim ou 'n' para não."


# =========================================================
# PERSISTÊNCIA EM ARQUIVO
# =========================================================

def salvar_cliente_em_arquivo(cliente):
    with open(ARQUIVO, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"Nome: {cliente['nome']}; "
            f"E-mail: {cliente['email']}; "
            f"Telefone: {cliente['telefone']}\n"
        )


# =========================================================
# EXIBIÇÃO
# =========================================================

def exibir_cliente(cliente, numero=None):
    if numero is not None:
        print(Fore.CYAN + f"CLIENTE {numero}" + Style.RESET_ALL)

    print(f"Nome: {cliente['nome']}")
    print(f"E-mail: {cliente['email']}")
    print(f"Telefone: {cliente['telefone']}")


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

def main():
    clientes = []

    limpar_tela()
    cabecalho()

    while True:

        # -------------------------
        # CADASTRAR NOME
        # -------------------------

        nome = cadastrar_nome()

        # -------------------------
        # CADASTRAR E-MAIL
        # -------------------------

        email = cadastrar_email(nome)

        # -------------------------
        # CADASTRAR TELEFONE
        # -------------------------

        telefone = cadastrar_telefone(nome, email)

        # -------------------------
        # SALVAR CLIENTE
        # -------------------------

        cliente = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
        }

        clientes.append(cliente)
        salvar_cliente_em_arquivo(cliente)

        # -------------------------
        # PERGUNTAR SE CONTINUA
        # -------------------------

        continuar = perguntar_continuar(
            nome,
            email,
            telefone
        )

        if not continuar:
            break

    # =====================================================
    # FINAL
    # =====================================================

    limpar_tela()

    print(Fore.BLUE + "=" * 40)
    print("CADASTRO ENCERRADO")
    print("=" * 40 + Style.RESET_ALL)
    print(f"Total de clientes cadastrados: {len(clientes)}")
    print()

    for indice, cliente in enumerate(clientes, start=1):
        exibir_cliente(cliente, indice)
        print()


if __name__ == "__main__":
    main()