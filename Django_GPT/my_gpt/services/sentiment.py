from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        top_k=None,               
        device=get_pipeline_device(),
    )


def analyze_sentiment(text):
    classifier = get_sentiment_pipeline()
    outputs = classifier(text)[0]     

    scores = sorted(outputs, key=lambda x: x["score"], reverse=True)
    top = scores[0]

    return {
        "label": top["label"],          
        "score": top["score"],
        "all_scores": [
            {"label": s["label"], "score": round(s["score"] * 100, 2)}
            for s in scores
        ],
    }