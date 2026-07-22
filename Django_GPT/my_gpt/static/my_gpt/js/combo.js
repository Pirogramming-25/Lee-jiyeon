const input = document.getElementById("input");
const runBtn = document.getElementById("run");
const regenBtn = document.getElementById("regenerate");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");

let sending = false;
let lastText = null;   // 재생성용: 마지막으로 분석한 원문

function setSending(on) {
    sending = on;
    runBtn.disabled = on;
    regenBtn.disabled = on;
    statusEl.hidden = !on;
}

function renderResult(data) {
    resultEl.innerHTML =
        `<h3>[요약]</h3><div>${data.summary}</div>` +
        `<h3 style="margin-top:12px">[감정 분석]</h3>` +
        `<div>${data.sentiment.label} (${data.sentiment.score}%)</div>` +
        `<h3 style="margin-top:12px">[유해 표현 분석]</h3>` +
        `<div>Highest: ${data.toxicity.highest_label} (${data.toxicity.highest_score}%)</div>` +
        `<div>` +
        data.toxicity.all_scores.map((s) => `${s.label}: ${s.score}%`).join("<br>") +
        `</div>` +
        `<h3 style="margin-top:12px">[종합 판정]</h3><div>${data.verdict}</div>`;
}

async function analyze(text) {
    if (sending) return;
    errorEl.hidden = true;

    setSending(true);
    try {
        const res = await fetch("/combo/run/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ text }),
        });
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            errorEl.textContent = data.error || `요청 실패 (${res.status})`;
            errorEl.hidden = false;
            return;
        }

        renderResult(data);
        lastText = text;          // 재생성용으로 저장
        regenBtn.hidden = false;  // 재생성 버튼 노출
    } catch (e) {
        errorEl.textContent = "서버와 연결하지 못했습니다.";
        errorEl.hidden = false;
    } finally {
        setSending(false);
    }
}

runBtn.addEventListener("click", () => {
    const text = input.value.trim();
    if (!text) {
        errorEl.textContent = "분석할 내용을 입력해주세요.";
        errorEl.hidden = false;
        return;
    }
    analyze(text);
});

// 재생성: 입력창을 다시 안 받고 마지막 원문으로 재실행
regenBtn.addEventListener("click", () => {
    if (lastText) analyze(lastText);
});