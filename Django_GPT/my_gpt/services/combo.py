from .summarizer import summarize_text
from .sentiment import analyze_sentiment
from .moderator import moderate_text


def run_combo(text):
    # ① 요약 (원문 입력)
    summary_result = summarize_text(text, sample=True)
    summary = summary_result["summary"]

    # ② 감정 분석 (요약문 입력 — 원문 아님!)
    sentiment_result = analyze_sentiment(summary)

    # ③ 유해 표현 분석 (요약문 입력)
    toxicity_result = moderate_text(summary)

    # 종합 판정 (LLM 없이 조건문으로 생성)
    if sentiment_result["label"] == "negative":
        sentiment_desc = "부정적인 평가를 포함합니다."
    else:
        sentiment_desc = "강한 부정적 평가는 확인되지 않았습니다."

    if toxicity_result["highest_score"] >= 50:
        toxicity_desc = "유해 표현 가능성이 높습니다."
    else:
        toxicity_desc = "심각한 유해 표현 가능성은 낮습니다."

    verdict = f"이 피드백은 {sentiment_desc} 또한 {toxicity_desc}"

    return {
        "original_text": text,
        "summary": summary,
        "sentiment": {
            "label": sentiment_result["label"],
            "score": round(sentiment_result["score"] * 100, 2),
        },
        "toxicity": {
            "highest_label": toxicity_result["highest_label"],
            "highest_score": toxicity_result["highest_score"],
            "all_scores": toxicity_result["all_scores"],
        },
        "verdict": verdict,
    }