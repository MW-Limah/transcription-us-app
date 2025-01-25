import eventlet
eventlet.monkey_patch()

from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
from services.speech_to_text import transcribe_audio
from services.translator import translate_text
from routes.main import main
import os
import warnings
import subprocess

# Função para converter o áudio para um formato compatível
def convert_to_wav(input_file, output_file):
    try:
        command = [
            "ffmpeg", "-i", input_file, "-ar", "16000", "-ac", "1", "-y", output_file
        ]
        print(f"Executando comando: {' '.join(command)}")
        subprocess.run(command, check=True)
        print(f"Arquivo convertido para {output_file}")
    except Exception as e:
        raise RuntimeError(f"Erro ao converter arquivo: {e}")

# Diretório para arquivos temporários
TEMP_DIR = os.path.join(os.getcwd(), 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)  # Cria o diretório se não existir

# Suprime avisos de FutureWarning e FP16
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU")

app = Flask(__name__, static_folder="templates", static_url_path="/")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Endpoint para servir arquivos estáticos (Frontend)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# Endpoint WebSocket para transcrição e tradução em tempo real
@socketio.on('stream_audio')
def handle_stream(data):
    try:
        audio_data = data.get('audio')
        if not audio_data:
            raise ValueError("Nenhum dado de áudio foi recebido.")

        # Caminhos dos arquivos no diretório temporário
        temp_file = os.path.join(TEMP_DIR, 'temp_stream.wav')
        converted_file = os.path.join(TEMP_DIR, 'converted_stream.wav')

        # Salva os dados como arquivo temporário
        with open(temp_file, 'wb') as f:
            f.write(audio_data)

        # Converte o arquivo para um formato compatível
        convert_to_wav(temp_file, converted_file)

        # Transcreve o áudio
        transcription = transcribe_audio(converted_file)

        # Tradução para português
        translation = translate_text(transcription)

        # Envia a transcrição e a tradução de volta ao cliente
        emit('transcription', {'transcription': transcription, 'translation': translation})
    except Exception as e:
        print(f"Erro ao processar o áudio: {e}")
        emit('error', {'error': str(e)})
    finally:
        # Remove arquivos temporários
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(converted_file):
            os.remove(converted_file)

# Inicialização do servidor
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
