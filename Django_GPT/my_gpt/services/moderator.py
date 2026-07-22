from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device

MODEL_ID = "unitary/toxic-bert"


@lru_cache(maxsize=1)
def get_moderator():
    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        top_k=None,               
        device=get_pipeline_device(),
    )


def moderate_text(text):
    moderator = get_moderator()
    outputs = moderator(text)[0]        

    scores = sorted(outputs, key=lambda x: x["score"], reverse=True)
    top = scores[0]

    return {
        "highest_label": top["label"],
        "highest_score": round(top["score"] * 100, 2),
        "all_scores": [
            {"label": s["label"], "score": round(s["score"] * 100, 2)}
            for s in scores
        ],
    }