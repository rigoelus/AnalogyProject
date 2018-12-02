#!/usr/bin/env python3

from collections import defaultdict
import itertools
import json

from gensim.models import Word2Vec
from nltk.corpus import brown, gutenberg, reuters
import numpy as np

import methods

with open('501-le.json') as f:
    questions = json.load(f)['questions']

brown1 = Word2Vec(brown.sents(), iter=10, min_count=5, size=500, workers=4, sg=1)
#reuters1 = Word2Vec(reuters.sents(), iter=10, min_count=5, size=500, workers=4, sg=1)
print("Finished training models")

results = defaultdict(lambda: np.array([0, 0, 0])) # (correct, incorrect, skipped)

method_funcs = [('Vanilla1Blank', methods.Vanilla1Blank), ('OnlyBlank1Blank', methods.OnlyBlank1Blank),
                ('Ignore1Blank', methods.Ignore1Blank), ('AddOpposite1Blank', methods.AddOpposite1Blank)]
#models = [('brown1', brown1), ('reuters1', reuters1)]
models = [('brown1', brown1)]

for ques_i, ques in enumerate(questions):
    choices = ques['choices']
    question = ques['question']
    answer = ques['answer']
    blank = ['_' in x for x in question].index(True)

    for func_name, func in method_funcs:
        for model_name, model in models:
            word_vecs = [methods.getVector(model, x) for x in question[:3]]
            if not np.all(np.array(word_vecs)):
                results[func_name][2] += 1
                continue

            model_answer = func(*word_vecs, [methods.getVector(model, x) for x in choices])

            if answer == model_answer:
                results[func_name][0] += 1
            else:
                results[func_name][1] += 1

for func_name, func in method_funcs:
    prop_correct = results[func_name][0] / (results[func_name][0] + results[func_name][1])
    print(func_name, 'prop. correct:', prop_correct, 'skipped:', results[func_name][2])
