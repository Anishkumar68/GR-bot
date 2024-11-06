window.addEventListener("load", function () {
  const chatForm = document.getElementById("chatForm");
  const textInput = document.getElementById("user-input");
  const messageContainer = document.querySelector(".chatbot-messages");

  // Function to handle sending the message
  async function sendMessage(event) {
    if (event) event.preventDefault(); // Prevent form from refreshing the page if called from an event

    const userMessage = textInput.value.trim();
    if (!userMessage) return; // Exit if message is empty

    // Display user message in the chat
    addMessage(userMessage, "user-message");
    textInput.value = ""; // Clear the input field

    // Send the user message to the backend via a POST request
    const response = await fetch("/chatbot-response/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({message: userMessage}),
    });

    // Parse the JSON response from the backend
    const data = await response.json();

    // Display the AI response in the chat
    const aiResponse = data.message;
    addMessage(aiResponse, "ai-response");
  }

  // Function to add a message to the chat UI
  function addMessage(text, type) {
    const messageWrapper = document.createElement("div");
    messageWrapper.classList.add("message", type);

    // Add icon based on the message type
    const icon = document.createElement("span");
    icon.classList.add("icon");
    icon.innerHTML = type === "user-message" ? "&#128100;" : "&#129302;"; // User and AI icons

    const messageText = document.createElement("p");
    messageText.textContent = text;

    messageWrapper.appendChild(icon);
    messageWrapper.appendChild(messageText);
    messageContainer.appendChild(messageWrapper);

    // Auto-scroll to the latest message
    messageContainer.scrollTop = messageContainer.scrollHeight;
  }

  // Event listeners for form submission and Enter key
  textInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage(e); // Pass the event to sendMessage
  });
  document.querySelector(".btn-send").addEventListener("click", sendMessage); // No event needed here
});
