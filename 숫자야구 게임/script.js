const MAX_ATTEMPTS = 9;
let attempts = MAX_ATTEMPTS;
let answer = [];
let isGameOver = false;

const inputs = [
  document.getElementById("number1"),
  document.getElementById("number2"),
  document.getElementById("number3"),
];
const attemptsSpan = document.getElementById("attempts");
const resultsDiv = document.getElementById("results");
const resultImg = document.getElementById("game-result-img");
const submitButton = document.querySelector(".submit-button");

function initGame() {
  attempts = MAX_ATTEMPTS;
  isGameOver = false;
  answer = makeRandomNumbers();

  inputs.forEach((input) => (input.value = ""));
  resultsDiv.innerHTML = "";
  resultImg.src = "";
  attemptsSpan.textContent = attempts;
  submitButton.disabled = false;
}

function makeRandomNumbers() {
  const numbers = [];
  while (numbers.length < 3) {
    const rand = Math.floor(Math.random() * 10);
    if (!numbers.includes(rand)) {
      numbers.push(rand);
    }
  }
  return numbers;
}

function check_numbers() {
  if (isGameOver) return;

  const guess = inputs.map((input) => input.value.trim());

  const hasEmpty = guess.some((value) => value === "");
  if (hasEmpty) {
    inputs.forEach((input) => (input.value = ""));
    return;
  }

  const guessNumbers = guess.map((value) => Number(value));

  let strike = 0;
  let ball = 0;
  for (let i = 0; i < 3; i++) {
    if (guessNumbers[i] === answer[i]) {
      strike++;
    } else if (answer.includes(guessNumbers[i])) {
      ball++;
    }
  }

  attempts--;
  attemptsSpan.textContent = attempts;

  appendResult(guessNumbers, strike, ball);

  inputs.forEach((input) => (input.value = ""));

  if (strike === 3) {
    endGame(true);
  } else if (attempts === 0) {
    endGame(false);
  }
}

function appendResult(guessNumbers, strike, ball) {
  const row = document.createElement("div");
  row.className = "check-result";

  const left = document.createElement("div");
  left.className = "left";
  left.textContent = guessNumbers.join(" ");

  const colon = document.createElement("div");
  colon.textContent = ":";

  const right = document.createElement("div");
  right.className = "right";

  if (strike === 0 && ball === 0) {
    const out = document.createElement("span");
    out.className = "num-result out";
    out.textContent = "O";
    right.appendChild(out);
  } else {
    const strikeSpan = document.createElement("span");
    strikeSpan.textContent = strike + " ";

    const strikeCircle = document.createElement("span");
    strikeCircle.className = "num-result strike";
    strikeCircle.textContent = "S";

    const ballSpan = document.createElement("span");
    ballSpan.textContent = " " + ball + " ";

    const ballCircle = document.createElement("span");
    ballCircle.className = "num-result ball";
    ballCircle.textContent = "B";

    right.appendChild(strikeSpan);
    right.appendChild(strikeCircle);
    right.appendChild(ballSpan);
    right.appendChild(ballCircle);
  }

  row.appendChild(left);
  row.appendChild(colon);
  row.appendChild(right);
  resultsDiv.appendChild(row);
}

function endGame(isWin) {
  isGameOver = true;
  resultImg.src = isWin ? "success.png" : "fail.png";
  submitButton.disabled = true;
}

initGame();