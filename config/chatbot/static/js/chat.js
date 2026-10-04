// ===============================
// Chatbot JavaScript
// ===============================

console.log("chat.js loaded");


// ===============================
// Conversation History
// ===============================

let conversationHistory = [];


// ===============================
// Get CSRF token from cookie
// ===============================

function getCookie(name) {

    let cookieValue = null;

    if (
        document.cookie &&
        document.cookie !== ""
    ) {

        const cookies =
            document.cookie.split(";");

        for (
            let cookie of cookies
        ) {

            cookie = cookie.trim();

            if (
                cookie.startsWith(
                    name + "="
                )
            ) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(
                            name.length + 1
                        )
                    );

                break;
            }
        }
    }

    return cookieValue;
}


// ===============================
// Send Message
// ===============================

async function sendMessage() {

    console.log(
        "sendMessage called"
    );

    const promptBox =
        document.getElementById(
            "prompt"
        );

    if (!promptBox) {

        console.error(
            "Textarea with id='prompt' not found."
        );

        return;
    }

    const prompt =
        promptBox.value.trim();

    if (prompt === "") return;


    // ===============================
    // Show user message
    // ===============================

    addMessage(
        prompt,
        "user"
    );


    // ===============================
    // Add user message to history
    // ===============================

    conversationHistory.push({

        role: "user",

        content: prompt

    });


    // Keep recent history
    conversationHistory =
        conversationHistory.slice(-8);


    // Clear input
    promptBox.value = "";

    promptBox.focus();


    // Show typing indicator
    showTyping();


    const csrftoken =
        getCookie("csrftoken");


    try {

        const response =
            await fetch(
                "/chat/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "X-CSRFToken":
                            csrftoken
                    },

                    body: JSON.stringify({

                        prompt: prompt,

                        history:
                            conversationHistory
                    })
                }
            );


        hideTyping();


        if (!response.ok) {

            addMessage(
                "Server Error: " +
                response.status,
                "bot"
            );

            // Remove failed user message
            conversationHistory.pop();

            return;
        }


        const data =
            await response.json();


        // ===============================
        // Show AI response
        // ===============================

        addMessage(
            data.answer,
            "bot"
        );


        // ===============================
        // Save AI response
        // ===============================

        conversationHistory.push({

            role: "assistant",

            content: data.answer

        });


        // Keep recent history
        conversationHistory =
            conversationHistory.slice(-8);


    } catch (error) {

        hideTyping();

        console.error(error);

        addMessage(
            "Unable to connect to the server.",
            "bot"
        );

        // Remove failed user message
        conversationHistory.pop();
    }
}


// ===============================
// Add Message
// ===============================

function addMessage(
    text,
    type
) {

    const chat =
        document.getElementById(
            "chat-box"
        );

    if (!chat) {

        console.error(
            "chat-box not found."
        );

        return;
    }


    // Remove Markdown bold markers
    text =
        text.replace(
            /\*\*(.*?)\*\*/g,
            "$1"
        );


    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message " + type;


    const bubble =
        document.createElement(
            "div"
        );

    bubble.className =
        "bubble";

    bubble.style.whiteSpace =
        "pre-wrap";


    // ===============================
    // Detect URLs
    // ===============================

    const urlRegex =
        /(https?:\/\/[^\s]+)/g;

    let lastIndex = 0;

    let match;


    while (
        (match =
            urlRegex.exec(text)) !== null
    ) {

        // Text before URL
        bubble.appendChild(
            document.createTextNode(
                text.substring(
                    lastIndex,
                    match.index
                )
            )
        );


        // Remove punctuation
        // from the end of URL
        const cleanUrl =
            match[0].replace(
                /[.,!?;:)]+$/,
                ""
            );


        // Create clickable link
        const link =
            document.createElement(
                "a"
            );

        link.href =
            cleanUrl;

        link.textContent =
            cleanUrl;

        link.target =
            "_blank";

        link.rel =
            "noopener noreferrer";


        bubble.appendChild(
            link
        );


        // Add punctuation separately
        const punctuation =
            match[0].substring(
                cleanUrl.length
            );


        if (punctuation) {

            bubble.appendChild(
                document.createTextNode(
                    punctuation
                )
            );
        }


        lastIndex =
            urlRegex.lastIndex;
    }


    // Remaining text
    bubble.appendChild(
        document.createTextNode(
            text.substring(
                lastIndex
            )
        )
    );


    message.appendChild(
        bubble
    );

    chat.appendChild(
        message
    );


    // Scroll to bottom
    chat.scrollTop =
        chat.scrollHeight;
}


// ===============================
// Typing Indicator
// ===============================

function showTyping() {

    const chat =
        document.getElementById(
            "chat-box"
        );

    if (!chat) return;


    if (
        document.getElementById(
            "typing-indicator"
        )
    ) {
        return;
    }


    const div =
        document.createElement(
            "div"
        );

    div.className =
        "message bot";

    div.id =
        "typing-indicator";


    div.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;


    chat.appendChild(
        div
    );


    chat.scrollTop =
        chat.scrollHeight;
}


// ===============================
// Hide Typing Indicator
// ===============================

function hideTyping() {

    const typing =
        document.getElementById(
            "typing-indicator"
        );

    if (typing) {

        typing.remove();
    }
}


// ===============================
// Initialize Events
// ===============================

window.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "DOM Loaded"
        );


        const prompt =
            document.getElementById(
                "prompt"
            );

        const sendBtn =
            document.getElementById(
                "send-btn"
            );


        console.log(
            "Prompt:",
            prompt
        );

        console.log(
            "Send Button:",
            sendBtn
        );


        if (!prompt) {

            console.error(
                "Element with id='prompt' not found."
            );

            return;
        }


        if (!sendBtn) {

            console.error(
                "Element with id='send-btn' not found."
            );

            return;
        }


        // ===============================
        // Welcome Message
        // ===============================

        addMessage(
            `🎓 Welcome to Academia International College!

Hello! I'm the AI Assistant of Academia International College.

I can help you with:

1) Admissions & Enrollment
2) Courses & Programs
3) Eligibility Criteria
4) Scholarships & Financial Aid
5) Fees & Payment Information
6) College Facilities
7) Academic Calendar
8) Contact Information

How can I assist you today? 😊`,
            "bot"
        );


        // ===============================
        // Send Button
        // ===============================

        sendBtn.addEventListener(
            "click",
            sendMessage
        );


        // ===============================
        // Enter Key
        // ===============================

        prompt.addEventListener(
            "keydown",
            function (e) {

                if (
                    e.key === "Enter" &&
                    !e.shiftKey
                ) {

                    e.preventDefault();

                    sendMessage();
                }
            }
        );
    }
);