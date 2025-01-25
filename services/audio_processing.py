from pydub import AudioSegment

def convert_to_wav(file_path, output_path):
    audio = AudioSegment.from_file(file_path)
    audio.export(output_path, format="wav")
