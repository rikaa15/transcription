import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def transcribe_audio_with_timestamps(audio_path):
    audio_name = os.path.splitext(os.path.basename(audio_path))[0]
    
    output_file = f"transcription_deepgram_{audio_name}.txt"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # Send audio data to Deepgram for transcription
        response = await session.post(
            "https://api.deepgram.com/v1/listen",
            data=audio_data,
            params={
                "punctuate": "true",
                "language": "en-US",
                "utterances": "true",
                "words": "true"
            },
        )

        result = await response.json()

        # Extract word-level timestamps from the result
        words_data = []
        if "results" in result and "channels" in result["results"]:
            words = result["results"]["channels"][0].get("alternatives", [{}])[0].get("words", [])
            for word_info in words:
                word = word_info.get("word", "")
                start_time = word_info.get("start", 0)  # Start time in seconds
                end_time = word_info.get("end", 0)      # End time in seconds
                words_data.append(f"{start_time:.3f}-{end_time:.3f}: {word}")

        # Save transcription with timestamps to file
        with open(output_file, "w") as f:
            f.write("\n".join(words_data))

audio_file = "townhall_audio.mp3"  # Audio file path

# Run transcription
asyncio.run(transcribe_audio_with_timestamps(audio_file))
