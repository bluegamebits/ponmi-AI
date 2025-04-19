document.getElementById("send").onclick = async () => { const prompt = 
  document.getElementById("prompt").value; const resElem = 
  document.getElementById("response"); resElem.textContent = "⋯ thinking ⋯"; const 
  resp = await fetch("/chat", {
    method: "POST", headers: {"Content-Type": "application/json"}, body: 
    JSON.stringify({prompt})
  });
  const data = await resp.json(); resElem.textContent = data.reply || data.error;
};
