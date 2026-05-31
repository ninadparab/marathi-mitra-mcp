# ═══════════════════════════════════════════════════════════
# server.py — Marathi Mitra MCP Server
# ═══════════════════════════════════════════════════════════

import random
import sys
from mcp.server.fastmcp import FastMCP
from gradio_client import Client

# ── MCP Server ────────────────────────────────────────────
mcp = FastMCP(
    name="Marathi Mitra",
    instructions="""
    You are connected to Marathi Mitra — a Marathi vocabulary
    learning tool powered by a fine-tuned Phi-3 Mini model.
    Use teach_word() when user wants to learn a Marathi word.
    Use word_of_the_day() for daily vocabulary practice.
    Use quiz_me() to test the user's Marathi knowledge.
    Use get_vocabulary_list() to browse available words.
    Always be encouraging and kid-friendly.
    """
)

SPACES_URL = "ninadp/marathi-mitra"

# ── Vocabulary ────────────────────────────────────────────
VOCABULARY = [
    "butterfly", "sun", "moon", "rain", "flower",
    "tree", "river", "sky", "water", "mountain",
    "cat", "dog", "bird", "fish", "elephant",
    "cow", "monkey", "parrot", "lion", "tiger",
    "mother", "father", "sister", "brother",
    "grandmother", "grandfather", "friend",
    "school", "book", "pencil", "food", "house",
    "red", "blue", "green", "yellow", "white",
    "one", "two", "three", "four", "five",
    "happy", "love", "music", "dance", "game",
    "mango", "apple", "banana", "milk", "rice",
    "morning", "evening", "night", "today", "tomorrow",
    "big", "small", "hot", "cold", "good",
    "thank you", "hello", "yes", "no", "please",
]


# ── Helper — call HF Spaces ───────────────────────────────
def call_spaces(word: str) -> str:
    """Call HF Spaces Gradio API and return lesson text."""
    try:
        client = Client(SPACES_URL)
        result = client.predict(
            word, 0, 0, [],
            api_name="/predict",
        )
        lesson = result[0]
        if not lesson or lesson == "Please enter a word! 😊":
            return f"Sorry, couldn't find Marathi word for '{word}'"
        return lesson
    except Exception as e:
        return f"Error connecting to Marathi Mitra: {e}"


# ── Tool 1 — teach_word ───────────────────────────────────
@mcp.tool()
def teach_word(word: str) -> str:
    """
    Teach the Marathi word for any English word.
    Returns full lesson with Devanagari script,
    pronunciation, example sentence and fun fact.

    Args:
        word: English word to teach in Marathi
    """
    return call_spaces(word.strip().lower())


# ── Tool 2 — word_of_the_day ──────────────────────────────
@mcp.tool()
def word_of_the_day() -> str:
    """
    Get a random Marathi word of the day with full lesson.
    Great for daily vocabulary practice.
    """
    word   = random.choice(VOCABULARY)
    lesson = call_spaces(word)
    return f"🌟 TODAY'S MARATHI WORD 🌟\n\nWord: {word}\n\n{lesson}"


# ── Tool 3 — quiz_me ──────────────────────────────────────
@mcp.tool()
def quiz_me(word: str) -> str:
    """
    Quiz the user on a Marathi word.
    Shows English word, hides Marathi translation.

    Args:
        word: English word to quiz the user on
    """
    import re
    lesson = call_spaces(word.strip().lower())

    marathi_match = re.search(r"is \*\*([^*]+)\*\*", lesson)
    pronun_match  = re.search(r"How to say it:\*?\*?\s*(.+)", lesson)

    marathi_word  = marathi_match.group(1).strip() if marathi_match else "?"
    pronunciation = pronun_match.group(1).strip()  if pronun_match  else "?"

    return f"""🎯 MARATHI QUIZ TIME! 🎯

What is the Marathi word for: {word.upper()}?

Think about it... 🤔
Say "show answer" when ready!

💡 Hint: {len(marathi_word)} characters in Devanagari

[ANSWER: {marathi_word} / {pronunciation}]"""


# ── Tool 4 — get_vocabulary_list ──────────────────────────
@mcp.tool()
def get_vocabulary_list(category: str = "all") -> str:
    """
    Get list of available Marathi vocabulary words.

    Args:
        category: nature, animals, family, daily,
                  colors, numbers, or all
    """
    categories = {
        "nature":  ["sun", "moon", "rain", "flower", "tree",
                    "river", "sky", "water", "mountain", "cloud",
                    "star", "ocean", "forest", "rainbow"],
        "animals": ["cat", "dog", "bird", "fish", "elephant",
                    "cow", "monkey", "parrot", "lion", "tiger",
                    "horse", "rabbit", "peacock", "butterfly"],
        "family":  ["mother", "father", "sister", "brother",
                    "grandmother", "grandfather", "friend",
                    "uncle", "aunt", "child"],
        "daily":   ["school", "book", "pencil", "food", "house",
                    "door", "chair", "clock", "road", "market"],
        "colors":  ["red", "blue", "green", "yellow", "white",
                    "black", "orange", "pink"],
        "numbers": ["one", "two", "three", "four", "five", "ten"],
    }

    if category == "all":
        result = "📚 AVAILABLE VOCABULARY\n\n"
        for cat, words in categories.items():
            result += f"{cat.upper()}: {', '.join(words)}\n\n"
        result += f"Total: {sum(len(w) for w in categories.values())} words"
        return result

    category = category.lower()
    if category in categories:
        words = categories[category]
        return (
            f"📚 {category.upper()} ({len(words)} words):\n"
            f"{', '.join(words)}\n\n"
            f"Use teach_word() to learn any of these!"
        )
    return f"Category '{category}' not found. Try: {', '.join(categories.keys())}"


# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    # Use stderr for any debug messages — stdout is for MCP
    print("Marathi Mitra MCP Server starting...", file=sys.stderr)
    mcp.run(transport="stdio")