import re


text = "her fiancé's résumé is beautiful"

def remove_accent(text):
    accents = re.compile(u"[\u0300-\u036F]|é|è")
    text = accents.sub(u'e',text)
    return text

cleaned_text =  remove_accent(text)
print(cleaned_text)