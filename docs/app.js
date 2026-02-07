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

function appendChatMessage(container, role, message) {
  const item = document.createElement("div");
  item.className = `chat-line chat-line--${role}`;
  item.innerHTML = `<span class="chat-role">${role}</span><span class="chat-message">${message}</span>`;
  container.appendChild(item);
  container.scrollTop = container.scrollHeight;
}

function buildAssistantReply(input, latest) {
  const summary = latest
    ? `Latest mutation "${latest.mutation}" with fitness ${formatNumber(latest.fitness)}.`
    : "No metrics yet. Trigger an evolution cycle to generate data.";
  return `${summary} ${input ? `You asked: "${input}".` : ""}`;
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

    const chatLog = document.getElementById("chat-log");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    if (chatLog && chatInput && chatSend) {
      appendChatMessage(chatLog, "system", "Console online. Ask about the latest evolution cycle.");
      chatSend.addEventListener("click", () => {
        const text = chatInput.value.trim();
        if (!text) return;
        appendChatMessage(chatLog, "operator", text);
        const reply = buildAssistantReply(text, latest);
        appendChatMessage(chatLog, "aams", reply);
        chatInput.value = "";
      });
    }
  } catch (error) {
    updateText("timestamp", "No metrics yet.");
    const chatLog = document.getElementById("chat-log");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    if (chatLog && chatInput && chatSend) {
      appendChatMessage(chatLog, "system", "Console online. Metrics not available yet.");
      chatSend.addEventListener("click", () => {
        const text = chatInput.value.trim();
        if (!text) return;
        appendChatMessage(chatLog, "operator", text);
        appendChatMessage(
          chatLog,
          "aams",
          buildAssistantReply(text, null)
        );
        chatInput.value = "";
      });
    }
  }
}

render();
