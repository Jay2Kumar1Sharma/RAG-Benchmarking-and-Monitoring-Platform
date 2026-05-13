const state = {
  lastQuestion: "",
  lastAnswer: "",
  lastSources: [],
  summaryRetryTimer: null,
};

const $ = (selector) => document.querySelector(selector);
const config = window.RAG_PLATFORM_CONFIG || {};
const defaultApiBaseUrl = config.apiBaseUrl || "http://localhost:8000";
const apiReconnectMs = Number(config.apiReconnectMs || 5000);

function apiBase() {
  return defaultApiBaseUrl.replace(/\/$/, "");
}

async function request(path, options = {}) {
  const { timeoutMs = 15000, ...fetchOptions } = options;
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`${apiBase()}${path}`, {
      ...fetchOptions,
      signal: controller.signal,
    });
    const text = await response.text();
    const payload = text ? JSON.parse(text) : {};
    if (!response.ok) {
      throw new Error(payload.detail || `HTTP ${response.status}`);
    }
    return payload;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("Request timed out");
    }
    throw error;
  } finally {
    window.clearTimeout(timeout);
  }
}

function scheduleSummaryRetry() {
  window.clearTimeout(state.summaryRetryTimer);
  state.summaryRetryTimer = window.setTimeout(renderSummary, apiReconnectMs);
}

function clearSummaryRetry() {
  window.clearTimeout(state.summaryRetryTimer);
  state.summaryRetryTimer = null;
}

function setStatus(selector, text, tone = "neutral") {
  const node = $(selector);
  node.textContent = text;
  node.dataset.tone = tone;
}

function setMetricsPending() {
  $("#latency").textContent = "--";
  $("#hallucination").textContent = "--";
  $("#retrieval").textContent = "--";
  $("#tokens").textContent = "--";
  renderLeaderboard([]);
}

async function loadSummary() {
  setStatus("#api-status", "connecting", "loading");
  setMetricsPending();
  try {
    const [health, summary] = await Promise.all([
      request("/api/v1/health", { timeoutMs: 8000 }),
      request("/api/v1/observability/summary", { timeoutMs: 12000 }),
    ]);
    clearSummaryRetry();
    setStatus("#api-status", health.status, "good");
    return summary;
  } catch {
    setStatus("#api-status", "connecting", "loading");
    scheduleSummaryRetry();
    return null;
  }
}

async function renderSummary() {
  const summary = await loadSummary();
  if (!summary) {
    return;
  }
  const rows = summary.benchmark_leaderboard || [];
  $("#latency").textContent = `${Math.round(summary.p95_latency_ms)} ms`;
  $("#hallucination").textContent = `${(summary.hallucination_rate * 100).toFixed(1)}%`;
  $("#retrieval").textContent = Number(summary.retrieval_quality).toFixed(2);
  $("#tokens").textContent = Intl.NumberFormat().format(summary.token_usage);
  renderLeaderboard(rows);
}

function renderLeaderboard(rows) {
  if (!rows.length) {
    $("#leaderboard").innerHTML = `<tr><td colspan="5">--</td></tr>`;
    return;
  }
  $("#leaderboard").innerHTML = rows
    .map(
      (row) => `<tr>
        <td>${escapeHtml(row.retriever)}</td>
        <td>${escapeHtml(row.reranker)}</td>
        <td>${Number(row.quality_score || 0).toFixed(2)}</td>
        <td>${(Number(row.hallucination_rate || 0) * 100).toFixed(1)}%</td>
        <td>${Math.round(Number(row.p95_latency_ms || 0))} ms</td>
      </tr>`,
    )
    .join("");
}

async function uploadDocuments(event) {
  event.preventDefault();
  const files = $("#document-files").files;
  if (!files.length) {
    setStatus("#upload-status", "Choose at least one file", "bad");
    return;
  }
  const form = new FormData();
  for (const file of files) {
    form.append("files", file);
  }
  setStatus("#upload-status", "Uploading", "neutral");
  try {
    const result = await request("/api/v1/upload-documents", { method: "POST", body: form });
    setStatus("#upload-status", `${result.total_chunks} chunks`, "good");
    $("#upload-results").innerHTML = result.documents
      .map(
        (doc) => `<div class="result-row">
          <strong>${escapeHtml(doc.filename)}</strong>
          <span>${doc.duplicate ? "duplicate" : `${doc.chunks_created} chunks`}</span>
        </div>`,
      )
      .join("");
  } catch (error) {
    setStatus("#upload-status", error.message, "bad");
  }
}

async function runQuery(event) {
  event.preventDefault();
  const payload = {
    question: $("#question").value.trim(),
    retriever: $("#retriever").value,
    reranker: $("#reranker").value,
    top_k: Number($("#top-k").value),
    rerank_top_k: Number($("#rerank-top-k").value),
  };
  if (!payload.question) {
    setStatus("#query-status", "Question required", "bad");
    return;
  }
  setStatus("#query-status", "Running", "neutral");
  try {
    const result = await request("/api/v1/query", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
    state.lastQuestion = payload.question;
    state.lastAnswer = result.answer;
    state.lastSources = result.sources || [];
    setStatus("#query-status", `${Math.round(result.latency_ms)} ms`, "good");
    $("#answer").textContent = result.answer;
    renderSources(state.lastSources);
    await renderSummary();
  } catch (error) {
    setStatus("#query-status", error.message, "bad");
  }
}

function renderSources(sources) {
  $("#sources").innerHTML = sources
    .map(
      (source, index) => `<details class="source-item">
        <summary>[${index + 1}] score ${Number(source.score || 0).toFixed(3)}</summary>
        <p>${escapeHtml(source.text)}</p>
      </details>`,
    )
    .join("");
}

async function evaluateAnswer(event) {
  event.preventDefault();
  if (!state.lastAnswer) {
    setStatus("#eval-status", "Run a query first", "bad");
    return;
  }
  const payload = {
    persist: $("#persist-eval").checked,
    examples: [
      {
        question: state.lastQuestion,
        answer: state.lastAnswer,
        ground_truth: $("#ground-truth").value.trim() || null,
        contexts: state.lastSources,
        relevant_chunk_ids: state.lastSources.map((source) => source.chunk_id),
      },
    ],
  };
  setStatus("#eval-status", "Evaluating", "neutral");
  try {
    const result = await request("/api/v1/evaluate", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
    setStatus("#eval-status", "Complete", "good");
    $("#evaluation-results").innerHTML = Object.entries(result.metrics)
      .map(
        ([key, value]) => `<div class="result-row">
          <strong>${escapeHtml(key)}</strong>
          <span>${Number(value).toFixed(3)}</span>
        </div>`,
      )
      .join("");
    await renderSummary();
  } catch (error) {
    setStatus("#eval-status", error.message, "bad");
  }
}

async function runBenchmark(event) {
  event.preventDefault();
  const questions = $("#benchmark-questions").value.split("\n").map((item) => item.trim()).filter(Boolean);
  const payload = {
    name: $("#benchmark-name").value.trim() || "frontend-comparison",
    questions,
    variants: [
      { retriever: "hybrid", reranker: "keyword_overlap", chunk_size: 900 },
      { retriever: "dense", reranker: "identity", chunk_size: 900 },
      { retriever: "multi_query", reranker: "keyword_overlap", chunk_size: 900 },
    ],
  };
  setStatus("#benchmark-status", "Running", "neutral");
  try {
    const result = await request("/api/v1/benchmark", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
    setStatus("#benchmark-status", `${result.summary.variants} variants`, "good");
    renderLeaderboard(result.leaderboard);
    await renderSummary();
  } catch (error) {
    setStatus("#benchmark-status", error.message, "bad");
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

$("#refresh").addEventListener("click", renderSummary);
$("#upload-form").addEventListener("submit", uploadDocuments);
$("#query-form").addEventListener("submit", runQuery);
$("#evaluate-form").addEventListener("submit", evaluateAnswer);
$("#benchmark-form").addEventListener("submit", runBenchmark);
renderSummary();
