window.addEventListener("load", function () {
  // Function to handle sending user input
  function sendMessage() {
    // Get the user's input text
    const userInput = document.getElementById("user-input").value.trim();

    // Check if input is not empty
    if (userInput) {
      // Add user message to chat
      addMessage(userInput, "user-message");

      // Clear the input field
      document.getElementById("user-input").value = "";

      // Simulate AI response after a short delay
      setTimeout(() => {
        const aiResponse = getAIResponse(userInput);
        addMessage(aiResponse, "ai-response");
      }, 500); // Adjust delay as needed
    }
  }

  // Function to add a message to the chat area
  function addMessage(text, type) {
    const messagesContainer = document.querySelector(".chatbot-messages");

    // Create message wrapper div
    const messageWrapper = document.createElement("div");
    messageWrapper.classList.add("message", type);

    // Create icon for AI or user
    const icon = document.createElement("span");
    icon.classList.add("icon");
    icon.innerHTML = type === "user-message" ? "&#128100;" : "&#129302;"; // Emoji icons for user and AI

    // Create message text element
    const messageText = document.createElement("p");
    messageText.textContent = text;

    // Append icon and text to message wrapper
    messageWrapper.appendChild(icon);
    messageWrapper.appendChild(messageText);

    // Append message to messages container
    messagesContainer.appendChild(messageWrapper);

    // Scroll to the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Function to simulate AI response (for demonstration purposes)
  function getAIResponse(userInput) {
    // Simple response logic, can be replaced with API or GPT model integration
    if (userInput.toLowerCase().includes("gift")) {
      return "I can help you find the perfect gift! Tell me more about the person's interests.";
    } else {
      return "Let me think... That sounds interesting!";
    }
  }

  // Add event listener for Enter key to send message
  document
    .getElementById("user-input")
    .addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });

  // Add event listener for the send button
  document.querySelector(".btn-send").addEventListener("click", sendMessage);
});
