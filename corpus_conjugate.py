import re

NUM_QUESTIONS = 10
MAX_WORDS_PER_LINE = 15
SOURCE_PATH = "_data/europarl_v7_es.txt"
TRANSLATION_PATH = "_data/europarl_v7_en.txt"
REPLACEMENTS_PATH = "_data/por_para.txt"

replace_with = []
look_for = []
with open(REPLACEMENTS_PATH, "r") as textfile:
    for line in textfile:
        if line.strip():
            look_for.append(line.split(";")[0].strip())
            replace_with.append(" {} ".format(line.split(";")[1].strip()))

source = []

line_num = 0
questions = []
test = []

with open(SOURCE_PATH, "r") as textfile_es:
    with open(TRANSLATION_PATH, "r") as textfile_en:
        for line_es, line_en in zip(textfile_es, textfile_en):
            line_num += 1
            if len(questions) >= NUM_QUESTIONS:
                break
            elif len(line_es.split(" ")) > MAX_WORDS_PER_LINE:
                continue
            else:
                for regex, replacement in zip(look_for, replace_with):
                    match = re.search(regex, line_es, flags=re.IGNORECASE)
                    if match:
                        question = re.sub(regex, replacement, line_es, flags=re.IGNORECASE)
                        questions.append("{}. {} ({})\n\t{}".format(
                            line_num,
                            question.strip(),
                            match.group().strip(),
                            line_en.strip()))
                        question_test = {
                            "line_num": line_num,
                            "question": question.strip(),
                            "answer": match.group().strip(),
                            "english": line_en.strip(),
                        }
                        test.append(question_test)
                        # print(questions[-1])
                        break
for question in test:
    print("{}. {}\n\t{}".format(
        question["line_num"],
        question["question"],
        question["english"],
    ))
    if input("> ").lower() == question["answer"]:
        print("Correct!\n")
    else:
        print(f"Incorrect, the correct answer is: '{question['answer']}'")