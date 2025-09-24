import wikipedia
import re
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>⚡ Smart Aesthetic Chatbot</title>
    <style>
        :root {
            --bg: #f2f4fc;
            --bubble-user: #2f67e6;
            --bubble-bot: #fff;
            --bubble-user-text: #fff;
            --bubble-bot-text: #343a40;
            --accent: #ff7b54;
        }
        body {
            background: var(--bg);
            font-family: 'Segoe UI','Inter',Arial,sans-serif;
            margin:0; padding:0;
            display:flex; flex-direction:column;
            min-height:100vh;
        }
        header { text-align:center; color:var(--accent); margin:25px 0 8px; }
        .chatbox {
            flex:1; display:flex; flex-direction:column;
            background:#fff;
            box-shadow:0 6px 24px rgba(0,0,0,.15);
            border-radius:20px; max-width:500px;
            width:95%; margin:0 auto 20px;
            padding:20px;
        }
        .conversation { flex:1; overflow-y:auto; margin-bottom:15px; }
        .user-msg,.bot-msg { margin:10px 0; display:flex; }
        .bubble {
            padding:12px 16px; border-radius:20px;
            font-size:1.05rem; max-width:80%;
            word-wrap:break-word; white-space:pre-wrap;
            line-height:1.5;
        }
        .user-msg { justify-content:flex-end; }
        .user-msg .bubble {
            background:var(--bubble-user); color:var(--bubble-user-text);
            border-bottom-right-radius:6px;
        }
        .bot-msg { justify-content:flex-start; }
        .bot-msg .bubble {
            background:var(--bubble-bot); color:var(--bubble-bot-text);
            border-bottom-left-radius:6px;
        }
        form { display:flex; gap:10px; }
        input[type="text"] {
            flex:1; padding:12px 15px; border-radius:18px;
            border:2px solid var(--accent); background:var(--bg);
            font-size:1rem; color:#222;
        }
        input[type="submit"] {
            border:none; background:var(--accent);
            color:#222; border-radius:17px; font-weight:600;
            padding:0 18px; cursor:pointer;
        }
        input[type="submit"]:hover { opacity:0.9; }
        footer {
            text-align:center; font-size:0.95rem;
            color:var(--accent); padding:12px;
        }
    </style>
</head>
<body>
    <header><h2>⚡ Smart Aesthetic Chatbot</h2></header>
    <div class="chatbox">
        <div class="conversation">
            {% for msg, sender in history %}
                {% if sender == 'user' %}
                    <div class="user-msg"><span class="bubble">{{ msg }}</span></div>
                {% else %}
                    <div class="bot-msg"><span class="bubble">{{ msg }}</span></div>
                {% endif %}
            {% endfor %}
            {% if not history %}
                <div class="bot-msg"><span class="bubble">👋 Hi! I’m your chatbot. Ask me anything — I’ll try to find an answer.</span></div>
            {% endif %}
        </div>
        <form method="POST" autocomplete="off">
            <input type="text" name="message" placeholder="Ask me..." required autofocus/>
            <input type="submit" value="Send"/>
        </form>
    </div>
    <footer>© 2025 Shrey Shah — All Rights Reserved</footer>
</body>
</html>
"""

# ---------- Predefined Q&A ----------
basic_qa = {
    "what is a chatbot": "A chatbot is a program that simulates human conversation using AI or rule-based logic.",
    "what is ai": "AI (Artificial Intelligence) enables machines to perform tasks that typically require human intelligence.",
    "what is machine learning": "Machine Learning is a type of AI that allows systems to learn and improve from data automatically.",
    "what is python": "🐍 Python is a high-level, beginner-friendly programming language used in web, AI, and data science.",
    "what is java": "☕ Java is a popular programming language widely used for applications and enterprise systems.",
    "who made this": "This chatbot was proudly created by Shrey Shah ✨",
    "what is flask": "Flask is a lightweight Python web framework used to build web apps.",
    "what is wikipedia": "Wikipedia is a free online encyclopedia that anyone can edit.",
    "what is data science": "Data science involves analyzing and interpreting complex data to extract useful insights.",
    "what is cloud computing": "Cloud computing is delivering computing services (servers, storage, databases) over the internet."
    # 👉 You can expand this with up to 100 Q&A entries.
}

# ---------- Cleaning helper ----------
def clean_wikipedia(text):
    text = re.sub(r'\([^)]pronunciation[^)]\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------- Chatbot logic ----------
def chatbot_response(text):
    user_text = text.lower().strip()

    # Check basic Q&A first
    if user_text in basic_qa:
        return basic_qa[user_text]

    # Simple greetings
    if user_text in ["hi", "hello", "hey"]:
        return "Hello! 👋 How can I help you?"
    elif "your name" in user_text:
        return "I'm the Smart Aesthetic Chatbot 🤖"
    elif "bye" in user_text or "exit" in user_text:
        return "Goodbye! 👋 Have a great day."

    # Otherwise → Wikipedia fallback
    try:
        summary = wikipedia.summary(user_text, sentences=2, auto_suggest=True, redirect=True)
        return clean_wikipedia(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That could mean: {', '.join(e.options[:4])}."
    except wikipedia.exceptions.PageError:
        return "❌ Couldn't find info on that."
    except Exception:
        return "⚠ Something went wrong. Try again."

# ---------- Flask Route ----------
@app.route("/", methods=["GET", "POST"])
def home():
    history = []
    if request.method == "POST":
        user_message = request.form["message"]
        bot_response = chatbot_response(user_message)
        history.append((user_message, "user"))
        history.append((bot_response, "bot"))
    return render_template_string(HTML_PAGE, history=history)

if __name__ == "__main__":
    app.run(debug=True)
