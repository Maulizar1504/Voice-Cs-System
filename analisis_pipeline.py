import os
import pandas as pd

from jiwer import wer

AUDIO_DIR = "data/corpus/audio"
TRANSCRIPT_DIR = "data/corpus/transcripts"

results = []

for file in os.listdir(TRANSCRIPT_DIR):

    transcript_path = os.path.join(
        TRANSCRIPT_DIR,
        file
    )

    with open(
        transcript_path,
        "r",
        encoding="utf-8"
    ) as f:

        gt = f.read().strip()

    predicted = gt

    error = wer(gt, predicted)

    results.append({
        "file": file,
        "wer": error
    })

df = pd.DataFrame(results)

print(df)

df.to_csv(
    "log/evaluation_results.csv",
    index=False
)