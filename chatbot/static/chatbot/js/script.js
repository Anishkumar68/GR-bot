window.addEventListener("load", function () {
	const textInput = document.getElementById("user-input");
	const messageContainer = document.querySelector(".chatbot-messages");
	const sendButton = document.getElementById("send-message");

	// Sending the message
	async function sendMessage(event) {
		if (event) event.preventDefault();

		const userMessage = textInput.value.trim();
		if (!userMessage) return;

		// Display user message in the chat
		addMessage(userMessage, "user-message");
		textInput.value = ""; // Clear the input field

		// Show typing indicator
		showTypingIndicator();

		// Send user message to the backend
		const response = await fetch("/chatbot-response/", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify({message: userMessage}),
		});
		const data = await response.json();

		// Hide typing indicator and display AI response
		hideTypingIndicator();
		const aiResponse = data.message;
		addMessage(aiResponse, "ai-response");
	}

	// Function to add a message to the chat UI
	function addMessage(htmlContent, type) {
		const messageWrapper = document.createElement("div");
		messageWrapper.classList.add("message", type, "bubble-animation");

		const icon = document.createElement("span");
		icon.classList.add("icon");
		icon.innerHTML = type === "user-message" ? "&#128100;" : "&#129302;";

		const messageText = document.createElement("p");
		messageText.innerHTML = htmlContent;

		messageWrapper.appendChild(icon);
		messageWrapper.appendChild(messageText);
		messageContainer.appendChild(messageWrapper);
		messageContainer.scrollTop = messageContainer.scrollHeight;
	}

	// Typing indicator functions
	function showTypingIndicator() {
		const typingIndicator = document.createElement("div");
		typingIndicator.classList.add("typing-indicator", "bubble-animation");
		typingIndicator.innerHTML = `<span class="icon">🤖</span><span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
		typingIndicator.id = "typing-indicator";
		messageContainer.appendChild(typingIndicator);
		messageContainer.scrollTop = messageContainer.scrollHeight;
	}

	function hideTypingIndicator() {
		const typingIndicator = document.getElementById("typing-indicator");
		if (typingIndicator) {
			messageContainer.removeChild(typingIndicator);
		}
	}

	// Event listeners for form submission and Enter key
	textInput.addEventListener("keypress", function (e) {
		if (e.key === "Enter") sendMessage(e);
	});
	sendButton.addEventListener("click", sendMessage);
});
