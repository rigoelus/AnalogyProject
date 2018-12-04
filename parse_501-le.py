#!/usr/bin/env python3

import copy
import json
import re
import sys

output = {'source': '501 questions learning express'}
questions = []

infile = '501-le.txt'
lines = [x.strip() for x in open(infile).readlines()]

word_regex = r'[^:]+'
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
EMPTY_QUESTION = {'question':'', 'choices':[], 'answer': 0, 'blank': 0}
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
                blank_j = 0
                for j, word in enumerate(sum(ques, [])):
                    if '_' in word:
                        blank_j = j
                        break

                curr_question['blank'] = blank_j

                # permute the question such that the blank is the last word
                if blank_j % 2 == 0: # swap `a`, `b`; and `c` and `d`
                    ques[0][0], ques[0][1] = ques[0][1], ques[0][0]
                    ques[1][0], ques[1][1] = ques[1][1], ques[1][0]
                if blank_j < 2:
                    ques[0], ques[1] = ques[1], ques[0]

                ques = sum(ques, []) # flatten after swapping

                ques[3] = QUESTION_BLANK
                curr_question['question'] = ques

                state = PARSING_CHOICES
                i += 1
                break
            else:
                i += 1
    elif state == PARSING_CHOICES:
        while i < len(lines):
            if choice_regex.match(lines[i]):
                splits = lines[i].lower().strip().split('.', 1)
                curr_question['choices'].append(splits[-1].strip())

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
            i += 1
    elif state == FINISHED:
        break

output['questions'] = questions
print(json.dumps(output))
