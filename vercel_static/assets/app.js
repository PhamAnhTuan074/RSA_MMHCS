const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

const state = {
  mode: "number",
  keys: null,
};

const presets = {
  easy: { p: 3n, q: 11n, e: 3n, mode: "number", message: "4" },
  medium: { p: 109n, q: 137n, e: 19n, mode: "number", message: "123" },
  text: { p: 61n, q: 53n, e: 17n, mode: "text", message: "HELLO RSA" },
};

function toBigInt(value, fallback = 0n) {
  const clean = String(value ?? "").trim();
  if (!/^-?\d+$/.test(clean)) return fallback;
  return BigInt(clean);
}

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) {
    [a, b] = [b, a % b];
  }
  return a;
}

function isPrime(number) {
  if (number < 2n) return false;
  if (number === 2n || number === 3n) return true;
  if (number % 2n === 0n) return false;
  for (let divisor = 3n; divisor * divisor <= number; divisor += 2n) {
    if (number % divisor === 0n) return false;
  }
  return true;
}

function modPow(base, exponent, modulus) {
  if (modulus <= 1n) return 0n;
  let result = 1n;
  let currentBase = ((base % modulus) + modulus) % modulus;
  let currentExponent = exponent;
  const steps = [];
  let round = 1;

  while (currentExponent > 0n) {
    const odd = currentExponent % 2n === 1n;
    if (odd) result = (result * currentBase) % modulus;
    steps.push({
      round,
      exponent: currentExponent,
      odd,
      result,
      base: currentBase,
    });
    currentBase = (currentBase * currentBase) % modulus;
    currentExponent = currentExponent / 2n;
    round += 1;
  }

  if (steps.length === 0) {
    steps.push({ round: 1, exponent: 0n, odd: false, result: 1n % modulus, base: currentBase });
  }
  return { value: result, steps };
}

function extendedGcdTable(a, b) {
  let oldR = a;
  let r = b;
  let oldS = 1n;
  let s = 0n;
  let oldT = 0n;
  let t = 1n;
  const rows = [
    { step: 0, q: "-", r: oldR, s: oldS, t: oldT, expr: `${oldR} = ${oldS}.${a} + ${oldT}.${b}` },
    { step: 1, q: "-", r, s, t, expr: `${r} = ${s}.${a} + ${t}.${b}` },
  ];

  let step = 2;
  while (r !== 0n) {
    const quotient = oldR / r;
    const nextR = oldR - quotient * r;
    const nextS = oldS - quotient * s;
    const nextT = oldT - quotient * t;
    rows.push({
      step,
      q: String(quotient),
      r: nextR,
      s: nextS,
      t: nextT,
      expr: nextR === 0n ? "Dừng vì số dư bằng 0" : `${nextR} = ${nextS}.${a} + ${nextT}.${b}`,
    });
    [oldR, r] = [r, nextR];
    [oldS, s] = [s, nextS];
    [oldT, t] = [t, nextT];
    step += 1;
  }
  return rows;
}

function modInverse(e, phi) {
  const table = extendedGcdTable(phi, e);
  const row = table.find((item) => item.r === 1n);
  if (!row) throw new Error("Không tồn tại nghịch đảo modulo.");
  return ((row.t % phi) + phi) % phi;
}

function suggestE(phi) {
  for (const candidate of [65537n, 257n, 17n, 5n, 3n]) {
    if (candidate > 1n && candidate < phi && gcd(candidate, phi) === 1n) return candidate;
  }
  for (let candidate = 3n; candidate < phi; candidate += 2n) {
    if (gcd(candidate, phi) === 1n) return candidate;
  }
  return 3n;
}

function parseCipher(text) {
  const matches = String(text).match(/-?\d+/g) ?? [];
  return matches.map((value) => BigInt(value)).filter((value) => value >= 0n);
}

function utf8Bytes(text) {
  return Array.from(new TextEncoder().encode(text), (byte) => BigInt(byte));
}

function bytesToText(bytes) {
  const raw = Uint8Array.from(bytes.map((byte) => Number(byte)));
  return new TextDecoder("utf-8", { fatal: true }).decode(raw);
}

function renderRows(tbody, rows, cells) {
  tbody.innerHTML = rows
    .map((row) => `<tr>${cells.map((cell) => `<td>${cell(row)}</td>`).join("")}</tr>`)
    .join("");
}

function setStatus(element, message, error = false) {
  element.classList.toggle("error", error);
  element.innerHTML = message;
}

function validateKeys() {
  const p = toBigInt($("#p-input").value);
  const q = toBigInt($("#q-input").value);
  const e = toBigInt($("#e-input").value);
  const status = $("#key-status");

  state.keys = null;
  $("#n-value").textContent = "-";
  $("#phi-value").textContent = "-";
  $("#public-key").textContent = "-";
  $("#private-key").textContent = "-";
  $("#euclid-table").innerHTML = "";

  if (!isPrime(p) || !isPrime(q)) {
    setStatus(status, "p và q phải là hai số nguyên tố.", true);
    updateSimulations();
    return;
  }
  if (p === q) {
    setStatus(status, "p và q phải khác nhau.", true);
    updateSimulations();
    return;
  }

  const n = p * q;
  const phi = (p - 1n) * (q - 1n);
  if (!(e > 1n && e < phi)) {
    setStatus(status, `e phải thỏa 1 < e < phi(n) = ${phi}.`, true);
    updateSimulations();
    return;
  }
  const common = gcd(e, phi);
  if (common !== 1n) {
    setStatus(status, `e chưa hợp lệ vì gcd(${e}, ${phi}) = ${common}.`, true);
    updateSimulations();
    return;
  }

  const d = modInverse(e, phi);
  const table = extendedGcdTable(phi, e);
  state.keys = { p, q, e, d, n, phi };

  $("#n-value").textContent = String(n);
  $("#phi-value").textContent = String(phi);
  $("#public-key").textContent = `(${e}, ${n})`;
  $("#private-key").textContent = `(${d}, ${n})`;
  setStatus(
    status,
    `Khóa hợp lệ. d = ${d}, kiểm tra e.d mod phi(n) = ${(e * d) % phi}.` +
      (n <= 255n ? " Với văn bản UTF-8 nên chọn n > 255." : "")
  );
  renderRows($("#euclid-table"), table, [
    (row) => row.step,
    (row) => row.q,
    (row) => row.r,
    (row) => row.s,
    (row) => row.t,
    (row) => row.expr,
  ]);
  updateSimulations();
}

function updateNumberSimulation() {
  const target = $("#number-result");
  const table = $("#power-table");
  if (!state.keys) {
    setStatus(target, "Hãy nhập bộ khóa hợp lệ trước.", true);
    table.innerHTML = "";
    return;
  }

  const m = toBigInt($("#message-number").value);
  const { e, d, n } = state.keys;
  if (m < 0n || m >= n) {
    setStatus(target, `m phải thỏa 0 <= m < n = ${n}.`, true);
    table.innerHTML = "";
    return;
  }

  const encrypted = modPow(m, e, n);
  const decrypted = modPow(encrypted.value, d, n);
  setStatus(
    target,
    `<strong>Chu trình hoàn tất:</strong> m = ${m} -> c = ${encrypted.value} -> m' = ${decrypted.value}.`
  );
  renderRows(table, encrypted.steps, [
    (row) => row.round,
    (row) => row.exponent,
    (row) => (row.odd ? "Có" : "Không"),
    (row) => row.result,
    (row) => row.base,
  ]);
}

function updateTextSimulation() {
  const target = $("#text-result");
  const table = $("#power-table");
  if (!state.keys) {
    setStatus(target, "Hãy nhập bộ khóa hợp lệ trước.", true);
    table.innerHTML = "";
    return;
  }

  const text = $("#message-text").value;
  const bytes = utf8Bytes(text);
  const { e, d, n } = state.keys;
  if (!text) {
    setStatus(target, "Vui lòng nhập văn bản.", true);
    table.innerHTML = "";
    return;
  }
  if (bytes.some((byte) => byte >= n)) {
    setStatus(target, `n = ${n} chưa đủ lớn cho mọi byte UTF-8. Hãy dùng p=61, q=53 hoặc lớn hơn.`, true);
    table.innerHTML = "";
    return;
  }

  const cipher = bytes.map((byte) => modPow(byte, e, n).value);
  const recoveredBytes = cipher.map((item) => modPow(item, d, n).value);
  let recovered = "";
  try {
    recovered = bytesToText(recoveredBytes);
  } catch {
    recovered = "(UTF-8 không hợp lệ)";
  }
  setStatus(
    target,
    `<strong>${bytes.length} byte:</strong> [${bytes.join(", ")}]<br>` +
      `<strong>Bản mã:</strong> [${cipher.join(", ")}]<br>` +
      `<strong>Khôi phục:</strong> ${escapeHtml(recovered)}`
  );

  const sample = bytes[0] ?? 0n;
  renderRows(table, modPow(sample, e, n).steps, [
    (row) => row.round,
    (row) => row.exponent,
    (row) => (row.odd ? "Có" : "Không"),
    (row) => row.result,
    (row) => row.base,
  ]);
}

function updateSimulations() {
  if (state.mode === "number") {
    updateNumberSimulation();
  } else {
    updateTextSimulation();
  }
}

function encryptQuick() {
  if (!state.keys) {
    $("#quick-cipher").textContent = "Hãy nhập bộ khóa hợp lệ ở phần mô phỏng.";
    return;
  }
  const text = $("#quick-plain").value;
  const bytes = utf8Bytes(text);
  const { e, n } = state.keys;
  if (bytes.some((byte) => byte >= n)) {
    $("#quick-cipher").textContent = `n = ${n} chưa đủ lớn cho văn bản UTF-8.`;
    return;
  }
  const cipher = bytes.map((byte) => modPow(byte, e, n).value);
  $("#quick-cipher").textContent = cipher.join(", ");
  $("#quick-cipher-input").value = cipher.join(", ");
}

function decryptQuick() {
  if (!state.keys) {
    $("#quick-plain-output").textContent = "Hãy nhập bộ khóa hợp lệ ở phần mô phỏng.";
    return;
  }
  const cipher = parseCipher($("#quick-cipher-input").value);
  const { d, n } = state.keys;
  if (!cipher.length) {
    $("#quick-plain-output").textContent = "Không tìm thấy số bản mã.";
    return;
  }
  try {
    const bytes = cipher.map((item) => modPow(item, d, n).value);
    $("#quick-plain-output").textContent = bytesToText(bytes);
  } catch {
    $("#quick-plain-output").textContent = "Dữ liệu giải mã không tạo thành UTF-8 hợp lệ.";
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
    return map[char];
  });
}

function switchView(viewName) {
  $$(".nav-tab").forEach((button) => button.classList.toggle("is-active", button.dataset.view === viewName));
  $$(".view").forEach((view) => view.classList.toggle("is-active", view.id === `${viewName}-view`));
}

function setMode(mode) {
  state.mode = mode;
  $("#mode-number").classList.toggle("is-active", mode === "number");
  $("#mode-text").classList.toggle("is-active", mode === "text");
  $("#number-sim").classList.toggle("is-hidden", mode !== "number");
  $("#text-sim").classList.toggle("is-hidden", mode !== "text");
  updateSimulations();
}

function applyPreset(name) {
  const preset = presets[name];
  $("#p-input").value = String(preset.p);
  $("#q-input").value = String(preset.q);
  $("#e-input").value = String(preset.e);
  if (preset.mode === "number") {
    $("#message-number").value = preset.message;
  } else {
    $("#message-text").value = preset.message;
  }
  setMode(preset.mode);
  validateKeys();
}

$$(".nav-tab").forEach((button) => button.addEventListener("click", () => switchView(button.dataset.view)));
$$(".preset-btn").forEach((button) => button.addEventListener("click", () => applyPreset(button.dataset.preset)));
["#p-input", "#q-input", "#e-input", "#message-number", "#message-text"].forEach((selector) => {
  $(selector).addEventListener("input", validateKeys);
});
$("#suggest-e").addEventListener("click", () => {
  const p = toBigInt($("#p-input").value);
  const q = toBigInt($("#q-input").value);
  if (isPrime(p) && isPrime(q) && p !== q) {
    $("#e-input").value = String(suggestE((p - 1n) * (q - 1n)));
    validateKeys();
  }
});
$("#mode-number").addEventListener("click", () => setMode("number"));
$("#mode-text").addEventListener("click", () => setMode("text"));
$("#encrypt-btn").addEventListener("click", encryptQuick);
$("#decrypt-btn").addEventListener("click", decryptQuick);

validateKeys();
encryptQuick();
