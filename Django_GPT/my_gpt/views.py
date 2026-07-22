import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .services.sentiment import analyze_sentiment, MODEL_ID as SENTIMENT_MODEL

from .decorators import model_login_required
from .models import InferenceHistory
from .services.summarizer import summarize_text, MODEL_ID as SUMMARIZE_MODEL

from .services.moderator import moderate_text, MODEL_ID as MODERATE_MODEL

from .services.combo import run_combo

logger = logging.getLogger(__name__)


def sentiment(request):
    return render(request, "my_gpt/sentiment.html", {
        "active_tab": "sentiment",
        "model_id": SENTIMENT_MODEL,
    })


@require_POST
def sentiment_run(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 요청이 아닙니다."}, status=400)

    text = str(body.get("text") or "").strip()

    # 서버 입력 검증 (감정 분석: 1~1000자)
    if not text:
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)
    if len(text) > 1000:
        return JsonResponse({"error": "문장은 1,000자 이하로 입력해주세요."}, status=400)

    # 오류 처리 (사용자에겐 traceback 노출 금지)
    try:
        result = analyze_sentiment(text)
    except Exception:
        logger.exception("Sentiment inference failed.")
        return JsonResponse({"error": "모델 실행에 실패했습니다."}, status=502)

    return JsonResponse({
        "label": result["label"],
        "score": round(result["score"] * 100, 2),
        "all_scores": result["all_scores"],
    })

def _recent_histories(user, task):
    """로그인 사용자의 해당 기능 최근 5개"""
    return list(
        InferenceHistory.objects
        .filter(user=user, task=task)
        .values("input_text", "output_text", "created_at")[:5]
    )


@model_login_required
def summarize(request):
    histories = _recent_histories(request.user, InferenceHistory.Task.SUMMARIZE)
    return render(request, "my_gpt/summarize.html", {
        "active_tab": "summarize",
        "model_id": SUMMARIZE_MODEL,
        "histories": histories,
    })


@require_POST
@model_login_required
def summarize_run(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 요청이 아닙니다."}, status=400)

    text = str(body.get("text") or "").strip()

    # 요약: 100~5000자
    if not text:
        return JsonResponse({"error": "요약할 문서를 입력해주세요."}, status=400)
    if len(text) < 100:
        return JsonResponse({"error": "요약할 문서는 100자 이상 입력해주세요."}, status=400)
    if len(text) > 5000:
        return JsonResponse({"error": "문서는 5,000자 이하로 입력해주세요."}, status=400)

    try:
        result = summarize_text(text)
    except Exception:
        logger.exception("Summarize inference failed.")
        return JsonResponse({"error": "모델 실행에 실패했습니다."}, status=502)

    # 로그인 사용자 → DB에 기록 저장
    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=text,
        output_text=result["summary"],
        result_data={"ratio": result["ratio"]},
    )

    return JsonResponse(result)

@model_login_required
def moderate(request):
    histories = _recent_histories(request.user, InferenceHistory.Task.MODERATE)
    return render(request, "my_gpt/moderate.html", {
        "active_tab": "moderate",
        "model_id": MODERATE_MODEL,
        "histories": histories,
    })


@require_POST
@model_login_required
def moderate_run(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 요청이 아닙니다."}, status=400)

    text = str(body.get("text") or "").strip()

    if not text:
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)
    if len(text) > 1000:
        return JsonResponse({"error": "문장은 1,000자 이하로 입력해주세요."}, status=400)

    try:
        result = moderate_text(text)
    except Exception:
        logger.exception("Moderate inference failed.")
        return JsonResponse({"error": "모델 실행에 실패했습니다."}, status=502)

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=text,
        output_text=f"{result['highest_label']} ({result['highest_score']}%)",
        result_data={"all_scores": result["all_scores"]},
    )

    return JsonResponse(result)

@model_login_required
def combo(request):
    histories = _recent_histories(request.user, InferenceHistory.Task.COMBO)
    return render(request, "my_gpt/combo.html", {
        "active_tab": "combo",
        "histories": histories,
    })


@require_POST
@model_login_required
def combo_run(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 요청이 아닙니다."}, status=400)

    text = str(body.get("text") or "").strip()

    # 복합: 200~5000자
    if not text:
        return JsonResponse({"error": "분석할 내용을 입력해주세요."}, status=400)
    if len(text) < 200:
        return JsonResponse({"error": "200자 이상 입력해주세요."}, status=400)
    if len(text) > 5000:
        return JsonResponse({"error": "5,000자 이하로 입력해주세요."}, status=400)

    try:
        result = run_combo(text)
    except Exception:
        logger.exception("Combo inference failed.")
        return JsonResponse({"error": "모델 실행에 실패했습니다."}, status=502)

    # 복합 기록 저장
    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.COMBO,
        input_text=text,
        output_text=result["summary"],
        result_data={
            "sentiment": result["sentiment"],
            "toxicity": {
                "highest_label": result["toxicity"]["highest_label"],
                "highest_score": result["toxicity"]["highest_score"],
            },
        },
    )

    return JsonResponse(result)