import random
import os
# Hypothetically import the DeepSeek client.
# from deepseek import DeepSeekClient

CLIENT = None # Explicitly set CLIENT to None to use fallback logic.

ANIMALS = [
    "Lion", "Elephant", "Tiger", "Giraffe", "Zebra", "Monkey", "Kangaroo", "Penguin", "Dolphin", "Bear",
    "Wolf", "Fox", "Rabbit", "Squirrel", "Horse", "Cow", "Pig", "Sheep", "Goat", "Chicken",
    "Duck", "Owl", "Eagle", "Parrot", "Snake", "Crocodile", "Turtle", "Frog", "Fish", "Shark"
]

# Basic categorization for hints (can be expanded)
ANIMAL_CATEGORIES = {
    "Lion": "mammal", "Elephant": "mammal", "Tiger": "mammal", "Giraffe": "mammal",
    "Zebra": "mammal", "Monkey": "mammal", "Kangaroo": "mammal", "Penguin": "bird",
    "Dolphin": "mammal", "Bear": "mammal", "Wolf": "mammal", "Fox": "mammal",
    "Rabbit": "mammal", "Squirrel": "mammal", "Horse": "mammal", "Cow": "mammal",
    "Pig": "mammal", "Sheep": "mammal", "Goat": "mammal", "Chicken": "bird",
    "Duck": "bird", "Owl": "bird", "Eagle": "bird", "Parrot": "bird",
    "Snake": "reptile", "Crocodile": "reptile", "Turtle": "reptile",
    "Frog": "amphibian", "Fish": "fish", "Shark": "fish"
}

ANIMAL_HINTS = {
    "Lion": "It's known as the king of the jungle.",
    "Elephant": "It's the largest land animal and has a trunk.",
    "Tiger": "It's a big cat with stripes.",
    "Giraffe": "It has a very long neck.",
    "Zebra": "It's a horse-like animal with black and white stripes.",
    "Monkey": "It's a primate that likes to climb trees.",
    "Kangaroo": "It's a marsupial from Australia that hops.",
    "Penguin": "It's a bird that cannot fly and lives in cold places.",
    "Dolphin": "It's an intelligent marine mammal.",
    "Bear": "It's a large mammal, some species hibernate.",
    # Add more specific hints if desired
}


def choose_animal():
    """Selects a random animal from the ANIMALS list."""
    return random.choice(ANIMALS)

def get_ai_answer(animal, question):
    """
    Gets a 'yes' or 'no' answer from the AI (DeepSeek) based on the animal and the question.
    """
    if CLIENT:
        try:
            prompt_messages = [
                {"role": "system", "content": "You are an assistant for a 'Guess the Animal' game. The player will ask a yes/no question about a specific animal. You must answer only with 'yes' or 'no'. Do not provide any explanations or additional text."},
                {"role": "user", "content": f"The animal is {animal}. The question is: {question}"}
            ]
            # response = CLIENT.chat.completions.create(model="deepseek-chat", messages=prompt_messages, max_tokens=5, temperature=0.0)
            # ai_response_text = response.choices[0].message.content.strip().lower()
            ai_response_text = _simulate_ai_response(animal, question, response_type="answer")

            if "yes" in ai_response_text:
                return "yes"
            elif "no" in ai_response_text:
                return "no"
            else:
                print(f"[AI Helper] Unexpected response from AI for answer: {ai_response_text}. Falling back to simulation.")
                return _simulate_ai_response(animal, question, response_type="answer")
        except Exception as e:
            print(f"[AI Helper] Error calling DeepSeek API for answer: {e}. Falling back to simulation.")
            return _simulate_ai_response(animal, question, response_type="answer")
    else:
        return _simulate_ai_response(animal, question, response_type="answer")

def get_ai_hint(animal):
    """
    Provides a hint for the given animal, using AI or simulated logic.
    """
    if CLIENT:
        try:
            prompt_messages = [
                {"role": "system", "content": "You are an assistant for a 'Guess the Animal' game. Provide a helpful, short, one-sentence hint for the animal. Do not reveal the animal's name."},
                {"role": "user", "content": f"Give me a hint for the animal: {animal}."}
            ]
            # response = CLIENT.chat.completions.create(model="deepseek-chat", messages=prompt_messages, max_tokens=50, temperature=0.7)
            # hint_text = response.choices[0].message.content.strip()
            hint_text = _simulate_ai_response(animal, "", response_type="hint")

            if hint_text:
                return hint_text
            else:
                print(f"[AI Helper] AI returned an empty hint. Falling back to simulation.")
                return _simulate_ai_response(animal, "", response_type="hint")
        except Exception as e:
            print(f"[AI Helper] Error calling DeepSeek API for hint: {e}. Falling back to simulation.")
            return _simulate_ai_response(animal, "", response_type="hint")
    else:
        return _simulate_ai_response(animal, "", response_type="hint")

def _simulate_ai_response(animal, question, response_type="answer"):
    """
    Internal placeholder logic for AI responses (answers or hints) if the API is not available.
    """
    animal_lower = animal.lower()

    if response_type == "hint":
        # Try specific hint first
        if animal in ANIMAL_HINTS:
            return ANIMAL_HINTS[animal]
        # Fallback to category hint
        if animal in ANIMAL_CATEGORIES:
            return f"Hint: This animal is a type of {ANIMAL_CATEGORIES[animal]}."
        return "Hint: I'm thinking of a common animal." # Generic fallback hint

    # Logic for response_type == "answer"
    question_lower = question.lower()
    if "mammal" in question_lower:
        return "yes" if ANIMAL_CATEGORIES.get(animal) == "mammal" else "no"
    elif "bird" in question_lower:
        return "yes" if ANIMAL_CATEGORIES.get(animal) == "bird" else "no"
    elif "reptile" in question_lower:
        return "yes" if ANIMAL_CATEGORIES.get(animal) == "reptile" else "no"
    elif "fish" in question_lower:
        return "yes" if ANIMAL_CATEGORIES.get(animal) == "fish" else "no"
    elif "fly" in question_lower:
        # Simplified: some birds fly, some don't.
        if animal_lower in ["penguin", "chicken", "ostrich"]: return "no"
        if ANIMAL_CATEGORIES.get(animal) == "bird" and animal_lower not in ["penguin", "chicken"]: return "yes" # most other birds
        if animal_lower == "bat": return "yes" # a flying mammal
        return "no"
    elif "water" in question_lower or "swim" in question_lower:
        if animal_lower in ["penguin", "dolphin", "crocodile", "turtle", "frog", "fish", "shark", "duck", "whale", "seal"]: return "yes"
        return "no"
    elif "legs" in question_lower:
        if "4" in question or "four" in question_lower:
            if animal_lower in ["lion", "elephant", "tiger", "giraffe", "zebra", "bear", "wolf", "fox", "horse", "cow", "pig", "sheep", "goat", "crocodile", "turtle", "lizard"]: return "yes"
            return "no"
        elif "2" in question or "two" in question_lower:
            if animal_lower in ["monkey", "kangaroo", "penguin", "chicken", "duck", "owl", "eagle", "parrot", "human", "bird", "ostrich"]: return "yes" # bird is generic
            return "no"
        elif "no legs" in question_lower or "0 legs" in question_lower:
            if animal_lower in ["snake", "fish", "shark", "dolphin", "whale", "worm"]: return "yes"
            return "no"

    return random.choice(["yes", "no"]) # Fallback for unhandled questions

if __name__ == '__main__':
    print("--- Testing AI Helper ---")
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Info: DEEPSEEK_API_KEY not set. AI responses will be simulated.")
        print("-" * 30)

    selected_animal = choose_animal()
    print(f"The AI is thinking of: {selected_animal}\n")

    # Test hint
    hint = get_ai_hint(selected_animal)
    print(f"Hint for {selected_animal}: {hint}\n")

    test_questions = [
        "Is it a mammal?", "Is it a bird?", "Can it fly?",
        "Does it live in water?", "Does it have 4 legs?", "Does it have 2 legs?", "Does it have no legs?",
        "Is it a predator?", "Is it bigger than a cat?", "Does it have fur?"
    ]

    for q in test_questions:
        answer = get_ai_answer(selected_animal, q)
        print(f"Q: {q}\nA: {answer}\n")

    print("--- End of AI Helper Test ---")
