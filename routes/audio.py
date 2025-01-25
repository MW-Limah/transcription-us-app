from flask import Blueprint, request, jsonify
from services.speech_to_text import transcribe_audio
from services.translator import translate_text
import os

# Criação do blueprint
audio_bp = Blueprint('audio', __name__)

# Rota para transcrever áudio
@audio_bp.route('/transcribe', methods=['POST'])
def transcribe():
    # Verifica se o arquivo foi enviado
    if 'audio' not in request.files:
        return jsonify({"error": "Nenhum arquivo de áudio foi enviado."}), 400

    audio_file = request.files['audio']

    # Salva o arquivo de áudio temporariamente
    temp_path = 'temp_audio.wav'
    audio_file.save(temp_path)

    try:
        # Realiza a transcrição
        transcription = transcribe_audio(temp_path)

        # Tradução para o português
        translation = translate_text(transcription)

        # Retorna a resposta
        return jsonify({
            "transcription": transcription,
            "translation": translation
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Remove o arquivo temporário
        if os.path.exists(temp_path):
            os.remove(temp_path)
