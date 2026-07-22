from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "sshleifer/distilbart-cnn-6-6"


@lru_cache(maxsize=1)
def get_summarizer():
    return pipeline(
        task="summarization",
        model=MODEL_ID,
        device=get_pipeline_device(),
    )


def summarize_text(text):
    summarizer = get_summarizer()
    output = summarizer(text, max_length=180, min_length=40)[0]
    summary = output["summary_text"].strip()

    ratio = round(len(summary) / len(text) * 100, 2)
    return {
        "summary": summary,
        "original_length": len(text),
        "summary_length": len(summary),
        "ratio": ratio,
    }