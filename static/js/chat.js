const historyEl = document.getElementById("chat-history");
const promptEl  = document.getElementById("prompt");
const sendBtn   = document.getElementById("send");

// helper to append a message bubble
function appendMessage(text, cls) {
  const msg = document.createElement("div");
  msg.className = `message ${cls}`;
  msg.textContent = text;
  historyEl.appendChild(msg);
  historyEl.scrollTop = historyEl.scrollHeight;
}

sendBtn.onclick = async () => {
  const text = promptEl.value.trim();
  if (!text) return;
  
  // disable while waiting
  sendBtn.disabled = true;
  promptEl.disabled = true;

  // user bubble
  appendMessage(text, "user");
  promptEl.value = "";

  // placeholder assistant bubble
  const thinking = document.createElement("div");
  thinking.className = "message assistant";
  thinking.textContent = "⋯ thinking ⋯";
  historyEl.appendChild(thinking);
  historyEl.scrollTop = historyEl.scrollHeight;

  // call backend
  try {
    const resp = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({prompt: text})
    });
    const data = await resp.json();

    // replace placeholder
    thinking.textContent = data.reply || data.error;
  } catch (err) {
    thinking.textContent = "🚨 Network error";
  }

  // re-enable input
  sendBtn.disabled = false;
  promptEl.disabled = false;
  promptEl.focus();
};