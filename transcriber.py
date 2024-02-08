from openai import OpenAI
import os
import subprocess
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def split_audio_with_ffmpeg(file_path, chunk_duration='60', output_format='m4a'):
    """
    Splits an audio file into chunks of a specified duration using FFmpeg.
    
    Args:
    - file_path: Full path to the input audio file.
    - chunk_duration: Duration of each chunk in seconds.
    - output_format: Format of the output files.
    
    Returns a list of paths to the chunk files.
    """
    file_dir, file_name = os.path.split(file_path)
    file_base, _ = os.path.splitext(file_name)
    output_template = os.path.join(file_dir, f"{file_base}_chunk_%03d.{output_format}")
    
    cmd = [
        'ffmpeg',
        '-i', file_path,
        '-f', 'segment',
        '-segment_time', chunk_duration,
        '-c', 'copy',
        output_template
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error splitting audio file: {e}")
        return []

    chunk_files = [os.path.join(file_dir, f) for f in os.listdir(file_dir) if f.startswith(f"{file_base}_chunk_") and f.endswith(f".{output_format}")]
    return sorted(chunk_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))

def transcribe_audio_file(file_path):
    """
    Splits the audio file into manageable chunks, transcribes each chunk using the OpenAI API,
    and saves the combined transcription to a text file in the current working directory.
    
    Args:
    - file_path: Full path to the audio file.
    """
    chunks = split_audio_with_ffmpeg(file_path, chunk_duration='300', output_format='m4a')  # 5 minutes chunks

    transcriptions = [''] * len(chunks) 

    def transcribe_chunk(chunk_path, index):
        try:
            with open(chunk_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            transcriptions[index] = transcript
        except Exception as e:
            print(f"Error transcribing chunk {index}: {e}")
            transcriptions[index] = ""

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(transcribe_chunk, chunk, i) for i, chunk in enumerate(chunks)]
        concurrent.futures.wait(futures)

    combined_transcription = " ".join(transcriptions)
    _, file_name = os.path.split(file_path)
    file_base = os.path.splitext(file_name)[0]
    output_text_file = os.path.join(os.getcwd(), f"storage/{file_base}.txt")
    
    with open(output_text_file, 'w') as f:
        f.write(combined_transcription)
    
    for chunk_path in chunks:
        os.remove(chunk_path)

    return output_text_file
