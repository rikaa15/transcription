from google.cloud import speech
from jiwer import wer

client = speech.SpeechClient()

audio = speech.RecognitionAudio(uri="gs://transcription-test-elon/elon-tucker_audio.flac")
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=48000,
    language_code="en-US",
    enable_word_time_offsets=True,
    audio_channel_count=2,
    model="latest_long"
)

operation = client.long_running_recognize(config=config, audio=audio)
print("Waiting for operation to complete...")
response = operation.result(timeout=None)

with open("transcription_timestamps.txt", "w") as file:
    file.write("Transcription Results:\n\n")
    
    for result in response.results:
        alternative = result.alternatives[0]
        file.write("Transcript: " + alternative.transcript + "\n")
        
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
            file.write(f"Word: {word}, start: {start_time}, end: {end_time}\n")

transcription_sentences = []
with open("transcription_sentences.txt", "w") as file:
    for result in response.results:
        alternative = result.alternatives[0]
        transcription_sentences.append(alternative.transcript)
        file.write(alternative.transcript + "\n")

generated_transcription = " ".join(transcription_sentences)
with open("ground_truth.txt", "r") as gt_file:
    ground_truth_transcription = gt_file.read().strip()

error_rate = wer(ground_truth_transcription, generated_transcription)
print(f"Word Error Rate (WER): {error_rate:.2%}")