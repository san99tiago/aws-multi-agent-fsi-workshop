// // TODO: add auth (uncommented by san99tiago)
// import { Amplify, Auth } from "aws-amplify";
// import awsconfig from "./aws-exports";

// Amplify.configure(awsconfig);

// Constants
const loginBtn = document.getElementById("login-btn");
const logoutBtn = document.getElementById("logout-btn");
const loginContainer = document.getElementById("login-container");
const applicationContainer = document.getElementById("application-container");

// Sign in and out
function signIn() {
  // Auth.federatedSignIn();
  // Hide the login container and show application container
  loginContainer.classList.add("hidden");
  applicationContainer.classList.remove("hidden");
  logoutBtn.style.display = "block";
  return true;
}
function signOut() {
  logoutBtn.style.display = "none";
  console.log("User is not authenticated.");
  applicationContainer.classList.add("hidden");
  loginContainer.classList.remove("hidden");
  logoutBtn.style.display = "none";
  return false;

  // REMOVED BY SANTI:
  // Auth.signOut();
}

loginBtn.addEventListener("click", signIn);
logoutBtn.addEventListener("click", signOut);

// // TODO: UNCOMMENT AND ADD AUTH (WHEN COGNITO ENABLED)
// // Start
// async function getUserSession() {
//   try {
//     const session = await Auth.currentSession();
//     const idToken = session.getIdToken().getJwtToken(); // Get the ID token
//     if (idToken) {
//       // User is authenticated, send a message
//       console.log("User is authenticated.");

//       // Hide the login container and show application container
//       loginContainer.classList.add("hidden");
//       applicationContainer.classList.remove("hidden");
//       logoutBtn.style.display = "block";
//       return true;
//     } else {
//       console.log("User is not authenticated.");
//       applicationContainer.classList.add("hidden");
//       loginContainer.classList.remove("hidden");
//       logoutBtn.style.display = "none";
//       return false;
//     }
//   } catch (error) {
//     console.log("Error getting user session:", error);
//     applicationContainer.classList.add("hidden");
//     loginContainer.classList.remove("hidden");
//     logoutBtn.style.display = "none";
//     return false;
//   }
// }
// getUserSession();

const messageContainer = document.getElementById("messageContainer");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

// Render the initial bot message
const initialBotMessage = document.createElement("div");
initialBotMessage.classList.add(
  "bg-green-200",
  "px-3",
  "py-2",
  "rounded-2xl",
  "self-start",
  "mb-4",
  "cursor-pointer",
  "w-3/4"
);
initialBotMessage.textContent = "Prueba el chatbot Multi-Agente!";
messageContainer.appendChild(initialBotMessage);

// Function to scroll to the bottom of the message container
function scrollToBottom() {
  messageContainer.scrollTop = messageContainer.scrollHeight;
}

// Handle Enter key press
messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});

// Send message function
async function sendMessage() {
  const message = messageInput.value.trim();
  if (message) {
    // Render the user's message
    const userMessage = document.createElement("div");
    userMessage.classList.add(
      "bg-emerald-900",
      "px-3",
      "py-2",
      "rounded-2xl",
      "self-end",
      "mb-4",
      "text-emerald-50"
    );
    userMessage.textContent = message;
    messageContainer.appendChild(userMessage);
    messageInput.value = "";
    scrollToBottom(); // Scroll to the bottom after rendering the user's message

    // Send the message to the API gateway
    try {
      // TODO: Replace this to the JSON API request...
      const data = {
        results: {
          output: {
            message: {
              content: [
                {
                  text: `Echo.. ${message}`,
                },
              ],
            },
          },
        },
      };
      // const response = await fetch(`REPLACE_API_URL/invokemodel?input=${encodeURIComponent(message)}`, {
      //   method: 'GET',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      // });
      // const data = await response.json();
      const botMessage = document.createElement("div");
      botMessage.classList.add(
        "bg-green-200",
        "px-3",
        "py-2",
        "rounded-2xl",
        "self-start",
        "mb-4",
        "cursor-pointer",
        "w-3/4",
        "highlighted"
      );

      // Check if the content is a BASE64-encoded image
      const content = data.results.output.message.content[0].text;
      botMessage.textContent = content;

      // Remove the highlight from the previous bot message
      const previousHighlightedDiv = document.querySelector(".highlighted");
      if (previousHighlightedDiv) {
        previousHighlightedDiv.classList.remove("highlighted");
      }

      messageContainer.appendChild(botMessage);
      scrollToBottom(); // Scroll to the bottom after rendering the bot's message
    } catch (error) {
      console.error("Error:", error);
    }
  }
}

// Handle send button click
sendButton.addEventListener("click", sendMessage);
