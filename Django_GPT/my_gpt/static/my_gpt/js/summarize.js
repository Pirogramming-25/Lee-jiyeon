const input = document.getElementById("input");
const runBtn = document.getElementById("run");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");

let sending = false;

function setSending(on) {
    sending = on;
    runBtn.disabled = on;
    input.disabled = on;
    statusEl.hidden = !on;
}

async function run() {
    if (sending) return;

    const text = input.value.trim();
    errorEl.hidden = true;
    resultEl.innerHTML = "";

    if (!text) {
        errorEl.textContent = "요약할 문서를 입력해주세요.";
        errorEl.hidden = false;
        return;
    }

    setSending(true);
    try {
        const res = await fetch("/summarize/run/", {
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

        resultEl.innerHTML =
            `<div>원문 길이: ${data.original_length}자</div>` +
            `<div>요약문 길이: ${data.summary_length}자</div>` +
            `<div>요약 비율: ${data.ratio}%</div>` +
            `<div style="margin-top:8px"><strong>요약 결과:</strong><br>${data.summary}</div>`;
    } catch (e) {
        errorEl.textContent = "서버와 연결하지 못했습니다.";
        errorEl.hidden = false;
    } finally {
        setSending(false);
    }
}

runBtn.addEventListener("click", run);