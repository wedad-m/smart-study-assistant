from question_generator import (
    extract_keywords,
    extract_definitions,
    generate_definition_mcq,
    generate_contextual_mcq,
    generate_true_false,
    generate_short_answer
)


def main():
    print("Smart Study Assistant - Exam Question Generator\n")

    text = input("Paste your lecture text:\n\n")
    while True:
        difficulty = input("Choose difficulty (easy / hard): ").lower()
        if difficulty in {"easy", "hard"}:
            break
        print("Please enter either 'easy' or 'hard'.\n")


    # Extract keywords and definitions
    keywords = extract_keywords(text)
    definitions = extract_definitions(text, keywords)

    # Ensure defined concepts are included in keywords
    for concept in definitions:
        if concept not in keywords:
            keywords.append(concept)

    # Display extracted keywords
    print("\nKeywords:")
    print(keywords)

    # -------------------------
    # Definition-based questions
    # -------------------------
    if definitions:
        print("\nDefinition-based Questions:")
        for q in generate_definition_mcq(definitions):
            print("\n" + q["question"])
            for opt in q["options"]:
                print("-", opt)

    # -------------------------
    # Difficulty-based questions
    # -------------------------
    if difficulty == "easy":
        print("\nConceptual Understanding MCQs:")
        for q in generate_contextual_mcq(text, keywords):
            print("\n" + q["question"])
            print(q["context"])
            for opt in q["options"]:
                print("-", opt)

    elif difficulty == "hard":
        print("\nTrue / False:")
        for q in generate_true_false(text, keywords):
            print("\n" + q["statement"])
            print(f"({q['answer']})")

        print("\nShort Answer:")
        for q in generate_short_answer(keywords):
            print("-", q)

    else:
        print("Invalid difficulty level.")


if __name__ == "__main__":
    main()
