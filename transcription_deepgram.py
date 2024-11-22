import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def transcribe_video_with_timestamps(video_path, output_file):
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        with open(video_path, "rb") as audio_file:
            audio_data = audio_file.read()

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

        # Extract word-level timestamps
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

# File paths
video_file = "elon-tucker.mp4"
output_file = "transcription_deepgram.txt"

# Run transcription
asyncio.run(transcribe_video_with_timestamps(video_file, output_file))
