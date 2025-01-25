import whisper

# Função para transcrever áudio usando Whisper
def transcribe_audio(file_path):
    """
    Transcreve o áudio de um arquivo usando o modelo Whisper da OpenAI.

    Args:
        file_path (str): Caminho para o arquivo de áudio.

    Returns:
        str: Texto transcrito do áudio.
    """
    try:
        # Carrega o modelo Whisper
        model = whisper.load_model("base")  # Pode trocar "base" por "tiny", "small", etc., conforme necessário.

        # Realiza a transcrição
        result = model.transcribe(file_path)

        # Retorna o texto transcrito
        return result.get('text', '')
    except Exception as e:
        raise RuntimeError(f"Erro ao transcrever o áudio: {e}")
