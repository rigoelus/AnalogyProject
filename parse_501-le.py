#!/usr/bin/env python3

import copy
import json
import re
import sys

output = {'source': '501 questions learning express'}
questions = []

infile = '501-le.txt'
lines = [x.strip() for x in open(infile).readlines()]

word_regex = r'[A-Za-z_ ]+'
ques_regex = re.compile(word_regex + r'\s*:\s*' + word_regex + r'\s*::\s*'\
                        + word_regex + r'\s*:\s*' + word_regex)
ques_splitter1 = re.compile(r'\s*::+\s*')
ques_splitter2 = re.compile(r'\s*:\s*')
choice_regex = re.compile('[A-Za-z]\.\s*'+word_regex)

FINDING_QUESTION = 0
PARSING_CHOICES = 1
PARSING_ANSWERS = 2
FINISHED = 3
state = FINDING_QUESTION
EMPTY_QUESTION = {'question':'', 'choices':[], 'answer':[]}
curr_question = copy.deepcopy(EMPTY_QUESTION)

QUESTION_BLANK = '_'*5

i = 0
question_idx = 0 # for parsing answers
while i < len(lines):
    if state == FINDING_QUESTION:
        while i < len(lines):
            if lines[i] == 'Answers:':
                state = PARSING_ANSWERS
                i += 1
                break
            elif ques_regex.match(lines[i]):
                ques = [ques_splitter2.split(x) for x in ques_splitter1.split(lines[i].lower())]
                for j in range(len(ques)):
                    if '_' in ques[j]:
                        ques[j] = QUESTION_BLANK
                curr_question['question'] = ques

                state = PARSING_CHOICES
                i += 1
                break
            else:
                i += 1
    elif state == PARSING_CHOICES:
        while i < len(lines):
            if choice_regex.match(lines[i]):
                splits = lines[i].lower().split(' ')
                curr_question['choices'].append(splits[-1])

                i += 1
            else:
                questions.append(curr_question)
                curr_question = copy.deepcopy(EMPTY_QUESTION)
                state = FINDING_QUESTION
                break
    elif state == PARSING_ANSWERS:
        while i < len(lines):
            if question_idx >= len(questions):
                #print("More answers than questions. Skipping.", file=sys.stderr)
                i += 1
                break
            answer = lines[i].lower()
            assert len(answer) == 1
            questions[question_idx]['answer'] = ord(answer)-ord('a')
            question_idx += 1
    elif state == FINISHED:
        break

output['questions'] = questions
print(json.dumps(output))
