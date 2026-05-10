const sample = [
  {
    retriever: "hybrid",
    reranker: "cross_encoder",
    quality_score: 0.86,
    hallucination_rate: 0.08,
    p95_latency_ms: 248,
  },
  {
    retriever: "dense",
    reranker: "identity",
    quality_score: 0.66,
    hallucination_rate: 0.13,
    p95_latency_ms: 210,
  },
  {
    retriever: "bm25",
    reranker: "identity",
    quality_score: 0.62,
    hallucination_rate: 0.15,
    p95_latency_ms: 146,
  },
];

async function loadSummary() {
  try {
    const response = await fetch("/api/v1/observability/summary");
    if (!response.ok) {
      throw new Error("summary unavailable");
    }
    return await response.json();
  } catch {
    return {
      p95_latency_ms: 248,
      hallucination_rate: 0.084,
      retrieval_quality: 0.86,
      token_usage: 12800,
      benchmark_leaderboard: sample,
    };
  }
}

async function render() {
  const summary = await loadSummary();
  const rows = summary.benchmark_leaderboard.length ? summary.benchmark_leaderboard : sample;
  document.querySelector("#latency").textContent = `${Math.round(summary.p95_latency_ms)} ms`;
  document.querySelector("#hallucination").textContent =
    `${(summary.hallucination_rate * 100).toFixed(1)}%`;
  document.querySelector("#retrieval").textContent = Number(summary.retrieval_quality).toFixed(2);
  document.querySelector("#tokens").textContent = Intl.NumberFormat().format(summary.token_usage);
  document.querySelector("#leaderboard").innerHTML = rows
    .map(
      (row) =>
        `<tr><td>${row.retriever}</td><td>${row.reranker}</td><td>${row.quality_score}</td><td>${(
          row.hallucination_rate * 100
        ).toFixed(1)}%</td><td>${row.p95_latency_ms} ms</td></tr>`,
    )
    .join("");
}

document.querySelector("#refresh").addEventListener("click", render);
render();
