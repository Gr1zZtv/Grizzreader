// Connect to server
const socket = new WebSocket("ws://localhost:8000/ws");

// When a message is received from the server, add it to the chat box
socket.addEventListener("message", (event) => {
  const chatBox = document.getElementById("chat-container");
  const messageData = JSON.parse(event.data);
  const username = messageData["username"];
  const message = messageData["message"];
  const chatMessage = document.createElement("div");
  const userNickname = document.createElement("span");
  userNickname.classList.add("user-nickname", getRandomColor());
  userNickname.innerText = username;
  chatMessage.appendChild(userNickname);
  chatMessage.innerHTML += ": " + message;
  chatMessage.classList.add("chat-message");
  chatBox.appendChild(chatMessage);
});

// Generate a random color for the username
function getRandomColor() {
  const colors = ["red", "green", "blue"];
  return colors[Math.floor(Math.random() * colors.length)];
}
