from question_generator import (
    extract_keywords,
    generate_mcq,
    generate_true_false,
    generate_short_answer
)

text = input("Paste your lecture text:\n\n")

keywords = extract_keywords(text)

print("\n🔑 Keywords:")
print(keywords)

print("\n--- 🧠 Multiple Choice Questions ---")
for q in generate_mcq(keywords):
    print("\n" + q["question"])
    for opt in q["options"]:
        print("-", opt)

print("\n--- ✅ True / False ---")
tf_questions = generate_true_false(text, keywords)

if tf_questions:
    for q in tf_questions:
        print("\n" + q["statement"])
        print("(True)")
else:
    print("No suitable sentences found for True/False questions.")

print("\n--- Short Answer ---")
for q in generate_short_answer(keywords):
    print("-", q)
