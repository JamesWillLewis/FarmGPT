import os
import sys
import openai

GPT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS_DEFAULT = 16
TEMPERATURE_DEFAULT = 0.2
INITIAL_PROMPT = "Ask me a question"
NEXT_PROMPT = "Ask me another question"
SYSTEM_MESSAGE = "You are asking the user US Civics questions." \
                 "After the user responds, check their answer and ask another question."

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = sys.argv[1] if len(sys.argv) > 1 else INITIAL_PROMPT
completion_args = {}
if len(sys.argv) > 2:
    completion_args['temperature'] = float(sys.argv[2])
if len(sys.argv) > 3:
    completion_args['max_tokens'] = int(sys.argv[3])

print(f"You asked: '{prompt}' with args: {completion_args}")
print(f'Using model {GPT_MODEL}')
print(f'Type q to quit')

current_prompt = INITIAL_PROMPT

messages = [
    {"role": "system", "content": SYSTEM_MESSAGE},
    {"role": "user", "content": current_prompt},
]

while True:

    question_response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=messages,
        **completion_args)

    gpt_question = question_response['choices'][0]['message']['content']
    print(f'GPT says: {gpt_question}')
    answer = input("Your answer: ")
    if answer == 'q':
        break

    messages.append({"role": "assistant", "content": gpt_question})
    messages.append({"role": "user", "content": answer})


