def text_separator(decorator="-", n_chars=81):
    """
        A função text_separator é utilizada para imprimir uma linha de separação no console. A linha é composta por um caractere repetido, que pode ser personalizado pelo usuário. O padrão é um hífen (-).
    Parâmetros

        decorator (str): Um caractere que será utilizado para criar a linha de separação. O valor padrão é '-'.
        n_chars (int): O número de caracteres que a linha de separação deve conter. O valor padrão é 81.

    Retorno
    A função retorna a linha de separação como uma string
    """
    return(decorator * n_chars)
