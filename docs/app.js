async function loadMetrics() {
  const response = await fetch("metrics.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Metrics not found");
  }
  return response.json();
}

function updateText(id, value) {
  const node = document.getElementById(id);
  if (node) {
    node.textContent = value;
  }
}

function formatNumber(value) {
  if (typeof value !== "number") return value;
  return value.toLocaleString(undefined, { maximumFractionDigits: 3 });
}

async function render() {
  try {
    const payload = await loadMetrics();
    const latest = payload.latest;

    updateText("timestamp", latest.timestamp ?? "-");
    updateText("mutation", latest.mutation ?? "-");
    updateText("accepted", latest.accepted ? "Yes" : "No");
    updateText("fitness", formatNumber(latest.fitness));

    updateText("loss", formatNumber(latest.metrics?.loss));
    updateText("latency", formatNumber(latest.metrics?.latency));
    updateText("params", formatNumber(latest.metrics?.params));
    updateText("seed", formatNumber(latest.metrics?.seed));

    const specNode = document.getElementById("spec");
    if (specNode) {
      specNode.textContent = JSON.stringify(latest.spec, null, 2);
    }
  } catch (error) {
    updateText("timestamp", "No metrics yet.");
  }
}

render();
