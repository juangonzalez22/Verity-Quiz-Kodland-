import os
import json
import discord
from services.giphy import get_gif

LETTERS = ["A", "B", "C", "D"]
SCORES_FILE = "scores.json"
POINTS_PER_CORRECT = 10
ANSWER_TIMEOUT = 20

RESULTS = {
    "correct": {"title": "✅ Correct!", "color": discord.Color.green()},
    "wrong": {"title": "❌ Wrong!", "color": discord.Color.red()},
    "timeout": {"title": "⏰ Time's up!", "color": discord.Color.orange()},
}

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, encoding="utf-8") as file:
        return json.load(file)

def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=2, ensure_ascii=False)

def record_answer(user, is_correct):
    scores = load_scores()
    entry = scores.setdefault(
        str(user.id),
        {"name": user.display_name, "points": 0, "correct": 0, "answered": 0},
    )
    entry["name"] = user.display_name
    entry["answered"] += 1
    if is_correct:
        entry["correct"] += 1
        entry["points"] += POINTS_PER_CORRECT
    save_scores(scores)
    return entry

def build_question_embed(question):
    embed = discord.Embed(
        title="🧠 Quiz!",
        description=f"**{question['question']}**",
        color=discord.Color.blurple(),
    )
    options_text = "\n".join(
        f"**{letter}.** {option}"
        for letter, option in zip(LETTERS, question["options"])
    )
    embed.add_field(name="Options", value=options_text, inline=False)

    footer = f"Topic: {question['topic']} • You have {ANSWER_TIMEOUT} seconds"

    if question.get("image"):
        embed.set_image(url=question["image"])
    else:
        gif_url = get_gif("thinking")
        if gif_url:
            embed.set_image(url=gif_url)
            footer += " • GIF: GIPHY"

    embed.set_footer(text=footer)
    return embed

def build_result_embed(question, status, entry=None):
    info = RESULTS[status]
    correct_text = question["options"][LETTERS.index(question["correct"])]

    embed = discord.Embed(
        title=info["title"],
        description=f"**{question['question']}**",
        color=info["color"],
    )
    embed.add_field(
        name="Correct answer",
        value=f"**{question['correct']}.** {correct_text}",
        inline=False,
    )

    footer_parts = []
    if entry:
        if status == "correct":
            footer_parts.append(
                f"+{POINTS_PER_CORRECT} points • Total: {entry['points']}"
            )
        else:
            footer_parts.append(f"No points this time • Total: {entry['points']}")

    gif_url = get_gif(status)
    if gif_url:
        embed.set_image(url=gif_url)
        footer_parts.append("GIF: GIPHY")

    if footer_parts:
        embed.set_footer(text=" • ".join(footer_parts))
    return embed