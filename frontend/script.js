function analyzeMood() {
  const input = document.getElementById("userInput").value.trim();
  const resultDiv = document.getElementById("result");

  if (!input) {
    alert("Please type how you're feeling.");
    return;
  }

  // Show user message
  resultDiv.innerHTML += `
    <div class="chat user">🧍‍♀️ You: ${input}</div>
  `;
  resultDiv.scrollTop = resultDiv.scrollHeight;

  // Show typing indicator
  const typingDiv = document.createElement("div");
  typingDiv.className = "chat bot typing";
  typingDiv.textContent = "MindGuard is typing...";
  resultDiv.appendChild(typingDiv);
  resultDiv.scrollTop = resultDiv.scrollHeight;

  // Send to backend
  fetch("http://localhost:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: input }),
  })
    .then((res) => res.json())
    .then((data) => {
      // Remove typing indicator
      resultDiv.removeChild(typingDiv);

      const botMessage = document.createElement("div");
      botMessage.className = "chat bot";

      let i = 0;
      const text = `🤖 MindGuard: ${data.reply}`;
      const typeWriter = () => {
        if (i < text.length) {
          botMessage.textContent += text.charAt(i);
          i++;
          resultDiv.scrollTop = resultDiv.scrollHeight;
          setTimeout(typeWriter, 15); // typing speed
        }
      };

      resultDiv.appendChild(botMessage);
      typeWriter();
      document.getElementById("userInput").value = "";
    })
    .catch((err) => {
      resultDiv.removeChild(typingDiv);
      resultDiv.innerHTML += `
        <div class="chat bot">❌ Error: ${err.message}</div>
      `;
    });
}

// Load chat history on page load
window.onload = () => {
  const resultDiv = document.getElementById("result");

  fetch("http://localhost:5000/history")
    .then((res) => res.json())
    .then((chats) => {
      chats.reverse().forEach((chat) => {
        resultDiv.innerHTML += `
          <div class="chat user">🧍‍♀️ You: ${chat.user}</div>
          <div class="chat bot">🤖 MindGuard: ${chat.bot}</div>
        `;
      });
      resultDiv.scrollTop = resultDiv.scrollHeight;
    });

  // Handle dark mode preference
  const toggle = document.getElementById("darkModeToggle");
  if (localStorage.getItem("darkMode") === "enabled") {
    document.body.classList.add("dark");
    toggle.checked = true;
  }

  toggle.addEventListener("change", () => {
    if (toggle.checked) {
      document.body.classList.add("dark");
      localStorage.setItem("darkMode", "enabled");
    } else {
      document.body.classList.remove("dark");
      localStorage.setItem("darkMode", "disabled");
    }
  });
};
