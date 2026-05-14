import re 

text = ' (to love is to destroy, and to be loved, is to be "the" one <destroyed>} '

def remove_puctuation(text):
    punctuation = re.compile(r'[{};():,."/<>-]')
    text = punctuation.sub(' ',text)
    return text

clean_text = remove_puctuation(text)
print(clean_text)
