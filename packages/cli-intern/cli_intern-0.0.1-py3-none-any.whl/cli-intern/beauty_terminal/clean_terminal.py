def clean_terminal():
    """
    A função clean_terminal é projetada para limpar a tela do terminal, proporcionando um ambiente mais organizado para a visualização de saídas subsequentes. Ela detecta automaticamente o sistema operacional em uso e executa o comando apropriado para limpar a tela.
    """
    import os

    os.system("cls" if os.name == "nt" else "clear")
