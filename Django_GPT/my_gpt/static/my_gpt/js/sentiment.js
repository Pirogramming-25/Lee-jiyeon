const input = document.getElementById("input");
const runBtn = document.getElementById("run");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");
const historyEl = document.getElementById("history");

let sending = false;
const localHistory = [];   // 비로그인 기록: 새로고침하면 사라짐

function setSending(on) {
    sending = on;
    runBtn.disabled = on;
    input.disabled = on;
    statusEl.hidden = !on;
}

function renderHistory() {
    historyEl.innerHTML = "";
    localHistory.slice(0, 5).forEach((item) => {
        const div = document.createElement("div");
        div.className = "history-item";
        div.textContent = `${item.label} (${item.score}%) — ${item.text}`;
        historyEl.appendChild(div);
    });
}

async function run() {
    if (sending) return;

    const text = input.value.trim();
    errorEl.hidden = true;
    resultEl.innerHTML = "";

    if (!text) {
        errorEl.textContent = "분석할 문장을 입력해주세요.";
        errorEl.hidden = false;
        return;
    }

    setSending(true);
    try {
        const res = await fetch("/sentiment/run/", {
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

        // 결과 출력: 대표 레이블 + 전체 점수
        const lines = data.all_scores
            .map((s) => `${s.label}: ${s.score}%`)
            .join("<br>");
        resultEl.innerHTML =
            `<strong>감정: ${data.label} (${data.score}%)</strong><br>${lines}`;

        // 비로그인 기록에 추가 (앞쪽에 넣고 5개 유지)
        localHistory.unshift({ label: data.label, score: data.score, text });
        if (localHistory.length > 5) localHistory.pop();
        renderHistory();
    } catch (e) {
        errorEl.textContent = "서버와 연결하지 못했습니다.";
        errorEl.hidden = false;
    } finally {
        setSending(false);
    }
}

runBtn.addEventListener("click", run);