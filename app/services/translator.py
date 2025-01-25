from googletrans import Translator

# Função para traduzir texto
def translate_text(text, target_lang='pt'):
    """
    Traduz o texto fornecido para o idioma de destino.

    Args:
        text (str): Texto a ser traduzido.
        target_lang (str): Idioma de destino (ex.: 'pt' para português).

    Returns:
        str: Texto traduzido.
    """
    try:
        # Inicializa o tradutor
        translator = Translator()

        # Realiza a tradução
        translation = translator.translate(text, dest=target_lang)

        # Retorna o texto traduzido
        return translation.text
    except Exception as e:
        raise RuntimeError(f"Erro ao traduzir o texto: {e}")
