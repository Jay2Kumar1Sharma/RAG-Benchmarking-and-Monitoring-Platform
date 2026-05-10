const sample = [
  { retriever: "hybrid", reranker: "cross_encoder", quality_score: 0.86, p95_latency_ms: 248 },
  { retriever: "dense", reranker: "identity", quality_score: 0.66, p95_latency_ms: 210 },
  { retriever: "bm25", reranker: "identity", quality_score: 0.62, p95_latency_ms: 146 },
];

function render() {
  document.querySelector("#latency").textContent = "248 ms";
  document.querySelector("#hallucination").textContent = "8.4%";
  document.querySelector("#retrieval").textContent = "0.86";
  document.querySelector("#tokens").textContent = "12.8k";
  document.querySelector("#leaderboard").innerHTML = sample
    .map(
      (row) =>
        `<tr><td>${row.retriever}</td><td>${row.reranker}</td><td>${row.quality_score}</td><td>${row.p95_latency_ms} ms</td></tr>`,
    )
    .join("");
}

document.querySelector("#refresh").addEventListener("click", render);
render();

