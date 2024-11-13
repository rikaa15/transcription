from google.cloud import speech

client = speech.SpeechClient()

audio = speech.RecognitionAudio(uri="gs://transcription-test-elon/elon_audio_section.flac")
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=44100,
    language_code="en-US",
    enable_word_time_offsets=True,
    audio_channel_count=2
)

operation = client.long_running_recognize(config=config, audio=audio)
print("Waiting for operation to complete...")
response = operation.result(timeout=90)

for result in response.results:
    alternative = result.alternatives[0]
    print("Transcript:", alternative.transcript)
    for word_info in alternative.words:
        word = word_info.word
        start_time = word_info.start_time
        end_time = word_info.end_time
        print(f"Word: {word}, start: {start_time.total_seconds()}, end: {end_time.total_seconds()}")
