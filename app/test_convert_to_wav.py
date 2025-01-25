import os
from app import convert_to_wav  # Importa a função do arquivo app.py

# Função principal para testar a conversão
if __name__ == "__main__":
    # Arquivo de entrada (substitua por um arquivo de áudio existente)
    input_file = "temp_stream.wav"
    # Arquivo de saída
    output_file = "converted_stream.wav"

    # Cria um arquivo de teste (caso não exista)
    if not os.path.exists(input_file):
        print(f"Criando um arquivo de teste: {input_file}")
        with open(input_file, "wb") as f:
            f.write("Teste de áudio")  # Adiciona dados fictícios no arquivo

    # Tenta converter o arquivo
    try:
        print(f"Convertendo {input_file} para {output_file}")
        convert_to_wav(input_file, output_file)
        print(f"Arquivo convertido: {output_file}")
    except Exception as e:
        print(f"Erro durante a conversão: {e}")

    # Limpeza (opcional)
    if os.path.exists(output_file):
        print(f"Arquivo gerado: {output_file}")
