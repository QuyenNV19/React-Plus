import re

class WhitespaceTokenizer:

    def lowercase(self, text):
        return text.lower()

    def normalize_whitespace(self, text):
        text = text.split()
        return " ".join(text)

    def tokenize(self, text):
        text = self.lowercase(text)
        text = self.normalize_whitespace(text)
        return text.split()
    
    def remove_punctuation(self,text):
        punctuation = re.compile(r'[!;():,."/<>\-]')
        text = punctuation.sub(' ',text)
        return text

    def Count_token_frequency(self,tokens):
        text = self.remove_punctuation(tokens)
        text = self.tokenize(text)
        count = {}

        for i in text:
            count[i] = count.get(i,0)+1
        return count
    
    def batch_tokenize(self, texts):
        return [self.tokenize(text) for text in texts]
        


if __name__ == "__main__":
    text = ["Hello world!"," NLP is fun."]
    tokenizer = WhitespaceTokenizer()
    print(tokenizer.batch_tokenize(text))
