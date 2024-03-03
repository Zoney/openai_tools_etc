from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import (
    OpenAIWhisperParser,
)
import concurrent.futures
import os

def download_and_transcribe_youtube(url):
    # Two Karpathy lecture videos
    urls = ["https://www.youtube.com/watch?v=2IK3DFHRFfw", "https://www.youtube.com/watch?v=2eWuYf-aZE4"]

    # Directory to save audio files
    save_dir = "./storage"

    # Transcribe the videos to text
    loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
    docs = loader.load()
    print(docs)
    # Initialize the YouTube audio loader
    # loader = YouTubeAudio()

    # Load and transcribe the audio from the YouTube URL
    # transcription = loader.load(url)

    # # Extract the video ID from the URL to use as a filename
    # video_id = url.split('=')[-1]

    # # Define the path to save the transcription text file
    # save_path = os.path.join('storage', f'{video_id}.txt')

    # # Save the transcription to a text file
    # with open(save_path, 'w') as file:
    #     file.write(transcription)

    # print(f"Transcription for {url} saved to {save_path}")

# def download_transcriptions_in_parallel(urls):
#     # Use ThreadPoolExecutor to download and transcribe in parallel
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(download_and_transcribe_youtube, urls)

# if __name__ == "__main__":
#     # Example YouTube URLs
#     youtube_urls = [
#         "https://www.youtube.com/watch?v=example1",
#         "https://www.youtube.com/watch?v=example2"
#     ]

#     download_transcriptions_in_parallel(youtube_urls)
