#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 21, 2012
Program for converting tests to Respondus format
@author: Gary Kokaisel
'''

import sys
import re
import easygui

# regular expressions to find test answers (very useful pythonic regex tool online http://re-try.appspot.com/)

regex_case_one = \
    r'''
            
\banswer\b[' '][a-z]{1}                     # Match word answer (ignoring case), followed by a space, followed by exactly one alpha character
                                            # for the following case... Answer a
                                        

            '''
regex_case_two = \
    r'''

\bans\b[':'][a-z]{1}                        # Match word ans (ignoring case), followed by colon, followed by exactly one alpha character
                                            # For the following case... ANS: a

            '''
regex_case_three_a = \
    r'''

\banswer\b[' ']+[a-z]{1}                    # Match word answer (ignoring case), followed by one or more spaces, followed by exactly one alpha character
                                            # For the following case... Answer  d     


            '''
regex_case_three_b = \
    r'''
           
\banswer\b[' ']+[a-z]+.*                    # Match word answer (ignoring case), followed by one or more spaces, followed by one or more alpha characters, 
                                            # followed by any character to end of line
                                            
                                            # For the following case... 
                                            # Answer  d     % correct 45      a= 12  b= 30  c= 14  d= 45      r = .41

            '''
regex_case_four_a = \
    r'''

\banswer\b[':'][' ']+[a-z]{1}               # Match word answer (ignoring case), followed by colon, followed by one or more spaces, followed by exactly one
                                            # alpha character
                                            
                                            # For the following case... Answer: a

            '''
regex_case_four_b = \
    r'''

(\banswer\b[':'][' ']+[a-z].*)              # Match word answer (ignoring case), followed by colon, followed by one or more spaces, followed by an alpha 
                                            # character, followed by any character to end of line
(\n+[a-z].*)+                               # Match a new line, followed by an alpha character, followed by any character to end of line, repeat pattern
                                                                                  
                                            
|\banswer\b[':'][' ']+[a-z]+.*              # Or, match word answer (ignoring case), followed by colon, followed by one or more spaces, 
                                            # followed by one or more alpha characters, followed by any character to end of line
                                            
                                            # For the following cases...
                                            # Answer: C
                                            # or...
                                            # Answer: D
                                            # Diff: 2 Page Ref: 6
                                            # Topic: Before Civilization
                                            # Skill: Conceptual
                                            # or even...
                                            # Answer:  B
                                            # Diff: 2
                                            # Topic:  The Solar System
                                            # Geog Standards:  New Geog Standards 4
                                            # Bloom's Taxonomy:  Knowledge
                                            # even better...
                                            # Answer:  D
                                            # Diff: 1
                                            # Topic:  3.1 Demand
                                            # Question Status:  Previous Edition


            '''

# boolean flags for each test case

case_one = False
case_two = False
case_three = False
case_four = False

# launch GUI to choose location for output file

saveout = sys.stdout
outfile = open(easygui.filesavebox(msg='Where to save formatted test?',
               default='formatted_test.txt'), 'w')
sys.stdout = outfile

# launch GUI to load test file, and store as string (replacing singles lines with double lines to make matching regexes easier)

input_file = easygui.fileopenbox(msg='Where is test to format?')
try:
    with open(input_file) as inputFileHandle:
        test = inputFileHandle.read().replace('\n', '''

''')
except IOError:
    sys.stderr.write('Could not open %s\n' % input_file)
    sys.exit(-1)

# find matches for the various test cases
# re.I ignores case, and re.X ignores comments and whitespace (unless included in pattern) within regular expression
# If Case 1

answer_match = re.findall(regex_case_one, test, flags=re.I | re.X)
if answer_match:
    case_one = True
    answer_list = answer_match

    # prints test without answers by substituting matched expression with empty string

    print re.sub(regex_case_one, '', test, flags=re.I | re.X)

# If Case 2

answer_match = re.findall(regex_case_two, test, flags=re.I | re.X)
if answer_match:
    case_two = True
    answer_list = answer_match

    # prints test without answers by substituting matched expression with empty string

    print re.sub(regex_case_two, '', test, flags=re.I | re.X)

# If Case 3

answer_match = re.findall(regex_case_three_a, test, flags=re.I | re.X)
if answer_match:
    case_three = True
    answer_list = answer_match

    # prints test without answers by substituting matched expression with empty string

    print re.sub(regex_case_three_b, '', test, flags=re.I | re.X)

# If Case 4

answer_match = re.findall(regex_case_four_a, test, re.I | re.X)
if answer_match:
    case_four = True
    answer_list = answer_match

    # prints test without answers by substituting matched expression with empty string

    print re.sub(regex_case_four_b, '', test, flags=re.I | re.X)

# print answer list as a numerically ordered list of answers in Respondus format

print 'Answers:'
number = 0
for answer in answer_list:
    number += 1

    # append ordered numbers to answer list

    answer_list = str(number) + '.' + answer

    # remove the word answer from answer list ignoring case sensitivity

    if case_one or case_three:

        # returns the string in qoutes wherever found without case sensitivity

        insensitive_answer = re.compile(re.escape('answer'), flags=re.I)

        # substitutes the literal string from above with an empty string (thereby removing it from list)

        print insensitive_answer.sub('', answer_list)
    elif case_two:
        insensitive_answer = re.compile(re.escape('ans:'), flags=re.I)
        print insensitive_answer.sub('', answer_list)
    elif case_four:
        insensitive_answer = re.compile(re.escape('answer:'),
                flags=re.I)
        print insensitive_answer.sub('', answer_list)

# flush output

outfile.flush()
outfile.close()
sys.stdout = saveout
