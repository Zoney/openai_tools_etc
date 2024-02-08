import argparse
from transcriber import transcribe_audio_file
from summarizer import summarize_text  # Import the summarize function from your new module

def transcribe_audio(args):
    transcription = transcribe_audio_file(args.audio_file)
    print(f"Transcription Done. File saved as {transcription}.")

def summarize_audio(args):
    summarize_text(args.text_file)  # Assumes the function prints the summary

def main():
    parser = argparse.ArgumentParser(description="Zoney AI Tools - A collection of CLI tools for various tasks.")
    subparsers = parser.add_subparsers(help='Available Commands')

    # Transcribe command
    transcribe_parser = subparsers.add_parser('transcribe', help='Transcribe an audio file using OpenAI Whisper API')
    transcribe_parser.add_argument('audio_file', type=str, help='Path to the audio file to be transcribed')
    transcribe_parser.set_defaults(func=transcribe_audio)

    # Summarize command
    summarize_parser = subparsers.add_parser('summarize', help='Summarize text from a .txt file')
    summarize_parser.add_argument('text_file', type=str, help='Path to the .txt file to summarize')
    summarize_parser.set_defaults(func=summarize_audio)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
