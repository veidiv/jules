# Guess the Animal AI Game

Welcome to "Guess the Animal," a fun and interactive game where you try to guess an animal that the AI is thinking of!

## How to Play

1.  The AI will secretly choose an animal.
2.  You can ask the AI yes/no questions to figure out what the animal is (e.g., "Is it a mammal?", "Can it fly?").
3.  The AI will answer your questions with "yes" or "no."
4.  When you think you know the animal, type `guess` to make your guess.
5.  Try to guess the animal in as few questions as possible!
6.  Type `quit` at any time to end the game.

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    The game requires Python and the `deepseek` library (though it currently uses a simulation mode if the API key is not provided).
    ```bash
    pip install -r requirements.txt
    ```

## Running the Game

1.  **Set the API Key (Optional for Full AI Mode):**
    To use the actual DeepSeek AI for responses, you need to set the `DEEPSEEK_API_KEY` environment variable.
    ```bash
    export DEEPSEEK_API_KEY="your_actual_api_key_here"
    ```
    If this key is not set, the game will run in a simulation mode with pre-defined responses for some common questions.

2.  **Run the game:**
    ```bash
    python game.py
    ```

Enjoy playing!
