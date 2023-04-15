import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def load_model(model_name='distilgpt2'):
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    return model, tokenizer

def generate_response(model, tokenizer, prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def main():
    model, tokenizer = load_model()

    print('Welcome to the self-hosted LLM on Raspberry Pi!')
    print('Type "exit" to quit.')

    while True:
        prompt = input('\nYour question: ')
        if prompt.lower() == 'exit':
            break

        response = generate_response(model, tokenizer, prompt)
        print(f'\nLLM response: {response}')

if __name__ == '__main__':
    main()
