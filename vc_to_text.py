from pathlib import Path
from faster_whisper import WhisperModel
answer  = input('you want small or medium:').lower().strip()

if answer not in ['small','medium']:
    raise ValueError('Only small and medium is accepted')


audio = next(Path(".").glob("*.mp3"))


print(f"Downloading/loading the {answer} model...", flush=True)


model = WhisperModel(
    answer,
    device="cpu",
    compute_type="int8",
)

print("Model loaded. Starting transcription...", flush=True)


segments, info = model.transcribe(
    str(audio),
    language="fa",
    task="transcribe",
    beam_size=5,
    vad_filter=True,
)

with open("transcript_fa.txt", "w", encoding="utf-8") as file:
    for segment in segments:
        text = segment.text.strip()
        print(text, flush=True)
        file.write(text + "\n")
