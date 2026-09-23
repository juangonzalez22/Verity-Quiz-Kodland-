import os
import json
import random
import aiohttp

LETTERS = ["A", "B", "C", "D"]

async def fetch_api_question():
    url = "https://the-trivia-api.com/v2/questions?limit=1&difficulties=easy"
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Trivia API status code: {response.status}")
                    return None
                data = await response.json()
                if not data or not isinstance(data, list):
                    return None

                raw = data[0]
                q_text = raw["question"]["text"]
                correct_ans = raw["correctAnswer"]
                options = raw["incorrectAnswers"] + [correct_ans]

                random.shuffle(options)
                correct_letter = LETTERS[options.index(correct_ans)]

                return {
                    "question": q_text,
                    "options": options,
                    "correct": correct_letter,
                    "topic": raw["category"].title(),
                    "image": None
                }
    except Exception as e:
        print(f"Error connecting to Trivia API: {e}")
        return None

def load_local_questions():
    if not os.path.exists("questions.json"):
        return []
    with open("questions.json", encoding="utf-8") as file:
        return json.load(file)

async def get_question():
    question = await fetch_api_question()
    if not question:
        local_questions = load_local_questions()
        if local_questions:
            question = random.choice(local_questions)
    return question