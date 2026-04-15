import re
class Analyzer:
    def __init__(self, text: str):
        self.text = text

    @property
    def sentences(self):
        return re.findall(r"[^.!?]+([.!?]|[^.!?]$)", self.text)
    
    @property
    def characters(self):
        return re.findall(r"\w", self.text)
    
    @property
    def words(self):
        return re.findall(r"\b\w+\b", self.text)

    @property
    def sentences_number(self):
        return len(self.sentences)
    
    @property
    def question_sentences_number(self):
        return len(re.findall(r"[^.!?]+\?", self.text))

    @property
    def affirmative_sentences_number(self):
        return len(re.findall(r"[^.!?]+(\.|[^.!?]$)", self.text))
    
    @property
    def imperative_sentences_number(self):
        return len(re.findall(r"[^.!?]+!", self.text))
    
    @property
    def average_sentence_length(self):
        if self.sentences_number == 0:
            return 0

        return len(self.characters) / self.sentences_number
    
    @property
    def average_word_length(self):
        if len(self.words) == 0:
            return 0

        return len(self.characters) / len(self.words)
    
    @property
    def smiles_number(self):
        return len(re.findall(r"(?<=\s)(?:;|:)-*(?:\[+|\]+|\(+|\)+)(?=\s)", self.text))
    
    @property
    def capital_letters(self):
        return re.findall(r"[A-Z]", self.text)
    
    @property
    def replace_sequences(self):
        return re.sub(r"a+b{2,}c+", "qqq", self.text)
    
    @property
    def longest_words_number(self):
        max_length = len(max(self.words, key=len))

        return len(re.findall(rf"\b\w{{{max_length}}}\b", self.text))
    
    @property
    def words_before_punctuation_mark(self):
        return len(re.findall(r"\b\w+(?:\.|,)", self.text))
    
    @property
    def longest_word_ends_with_e(self):
        words_ends_with_e = re.findall(r"\b\w*e\b", self.text)

        if len(words_ends_with_e) == 0:
            return None
        
        return max(words_ends_with_e, key=len)
    
    def __str__(self):
        return f"""Number of Sentences: {self.sentences_number}
    Including:
        Affirmative: {self.affirmative_sentences_number}
        Question: {self.question_sentences_number}
        Imperative: {self.imperative_sentences_number}
Average Sentence Length: {self.average_sentence_length}
Average Word Length: {self.average_word_length}
Number of Smiles: {self.smiles_number}
Capital Letters: {self.capital_letters}
Number of the Longest Words: {self.longest_words_number}
Words before Punctuation Mark: {self.words_before_punctuation_mark}
The Longest Words That Ends with \'e\': {self.longest_word_ends_with_e}

Text With Replaced Sequences:
{self.replace_sequences}
"""

