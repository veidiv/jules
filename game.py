import ai_helper

def play_game():
    """Main function to play the Guess the Animal game."""
    chosen_animal = ai_helper.choose_animal()
    # print(f"[Game Debug] AI has chosen: {chosen_animal}")

    print("Welcome to Guess the Animal!")
    print("I'm thinking of an animal. Try to guess it by asking yes/no questions.")
    print("Type 'guess' to make a guess, 'hint' for a hint, or 'quit' to end the game.")

    questions_asked = 0
    guessed_correctly = False
    hint_taken_this_turn = False # To prevent multiple hints without a question

    while not guessed_correctly:
        if hint_taken_this_turn:
            prompt_message = f"\nQuestion {questions_asked + 1}: What is your question? (or type 'guess'/'quit'): "
        else:
            prompt_message = f"\nQuestion {questions_asked + 1}: What is your question? (or type 'guess'/'quit'/'hint'): "

        user_input = input(prompt_message).strip().lower()
        hint_taken_this_turn = False # Reset for next input

        if not user_input:
            print("Please type a question, 'guess', 'quit', or 'hint'.")
            continue

        if user_input == "quit":
            print(f"Thanks for playing! The animal was {chosen_animal}.")
            break
        elif user_input == "guess":
            guess = input("What is your animal guess? ").strip()
            if not guess:
                print("You didn't type a guess! Please try again.")
                continue

            questions_asked += 1
            if guess.lower() == chosen_animal.lower():
                print(f"\nCongratulations! You guessed it! The animal was {chosen_animal}.")
                print(f"It took you {questions_asked} questions.")
                guessed_correctly = True
            else:
                print(f"Sorry, '{guess}' is not the animal I was thinking of.")
        elif user_input == "hint":
            questions_asked += 1
            hint = ai_helper.get_ai_hint(chosen_animal)
            print(f"Hint: {hint}")
            hint_taken_this_turn = True # Player just took a hint
        else:
            # It's a question
            questions_asked += 1
            ai_response = ai_helper.get_ai_answer(chosen_animal, user_input)
            print(f"AI says: {ai_response}")

    if not guessed_correctly and user_input != "quit":
        print(f"\nGame over. The animal was {chosen_animal}.")

if __name__ == "__main__":
    play_game()
