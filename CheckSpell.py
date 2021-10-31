import re
import string
from collections import Counter
from chatterbot.conversation import StatementMixin
import numpy as np
from chatterbot.logic import LogicAdapter

import glob
import os

class SpellChecker(LogicAdapter):

  def __init__(self,chatbot, **kwargs):
    super(SpellChecker, self).__init__(chatbot, **kwargs)
    words = []
    for filename in glob.glob('C:/Users/Admin/Desktop/Spell Checker/datasetSpellChecker/*[0-9].txt'):
        with open(os.path.join(os.getcwd(), filename), 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for line in lines:
                words += re.findall(r'[a-zA-Z]+', line.lower())

    self.vocabs = set(words)
    self.word_counts = Counter(words)
    total_words = float(sum(self.word_counts.values()))
    self.word_probas = {word: self.word_counts[word] / total_words for word in self.vocabs}

  def can_process(self, statement):
      words = ['check-spell:', 'correct-spell:', 'Turn-on-Spell-Checker:']
      if any(x in statement.text.split() for x in words):
          return True
      else:
          return False
          
  def process(self,word_input,additional_response_selection_parameters):
    from chatterbot.conversation import Statement
    confidence = 1
    def _level_one_edits(word):
      letters = string.ascii_lowercase
      splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
      deletes = [l + r[1:] for l,r in splits if r]
      swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r)>1]
      replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
      inserts = [l + c + r for l, r in splits for c in letters] 

      return set(deletes + swaps + replaces + inserts)

    def _level_two_edits(word):
      return set(e2 for e1 in _level_one_edits(word) for e2 in _level_one_edits(e1))
    # Off = ['turn-off','Turn-Off','Turn-off','Off','off']
    
    words = ['check-spell:', 'correct-spell:', 'Turn-on-Spell-Checker:']

    word =[]
    
    answer1 = []
    answer2 = []
    for i in word_input.text.split():
      for y in words:
        if i == y:
          word = word_input.text.split()[1:]
          break

    
    vocab = [x for x in self.vocabs]
    for i in word:
      if i in vocab:
        response_statement = Statement(text='{}'.format(i))
       
        answer1.append(str(response_statement))
      else:
        candidates = _level_one_edits(i) or _level_two_edits(i) or [i]
        valid_candidates = [w for w in candidates if w in self.vocabs]
        response_statement = Statement(text='{}'.format(sorted([(c) for c in valid_candidates], key=lambda tup: tup[1], reverse=True)[0:5]))    
        answer2.append(str(response_statement))

    response_statement1 = Statement(text='Correct words: {} + Recommend words: {} '.format(answer1,answer2)) 
    # response_statement2 = Statement(text='Recommend words: {}'.format(answer2))
    response_statement1.confidence = confidence
    # response_statement2.confidence = confidence
    
    return response_statement1  #,response_statement2
  
  

  

