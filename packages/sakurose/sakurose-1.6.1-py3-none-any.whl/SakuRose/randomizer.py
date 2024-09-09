import random
import string

generated_numbers = []
generated_strings = []
generated_texts = []

def randint(min_value, max_value, unique=False):
    num = random.randint(min_value, max_value)
    if unique:
        while num in generated_numbers:
            num = random.randint(min_value, max_value)
        generated_numbers.append(num)
    return num

def randstr(length, unique=False):
    letters = string.ascii_letters + string.digits
    rand_str = ''.join(random.choice(letters) for _ in range(length))
    if unique:
        while rand_str in generated_strings:
            rand_str = ''.join(random.choice(letters) for _ in range(length))
        generated_strings.append(rand_str)
    return rand_str

def randtext(*args):
    unique = False
    if isinstance(args[-1], bool):
        unique = args[-1]
        args = args[:-1]
    else:
        args = args
    
    probabilities = []
    texts = []
    
    for arg in args:
        if '-' in arg and arg.split('-')[-1].endswith('%'):
            text, prob = arg.rsplit('-', 1)
            probabilities.append(float(prob.rstrip('%')) / 100)
            texts.append(text)
        else:
            probabilities.append(1)
            texts.append(arg)
    
    total_prob = sum(probabilities)
    probabilities = [p / total_prob for p in probabilities]
    
    chosen_text = random.choices(texts, weights=probabilities, k=1)[0]
    
    if unique:
        while chosen_text in generated_texts:
            chosen_text = random.choices(texts, weights=probabilities, k=1)[0]
        generated_texts.append(chosen_text)
    
    return chosen_text