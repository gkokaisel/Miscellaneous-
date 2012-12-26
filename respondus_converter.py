#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 21, 2012
Program for converting tests to Respondus format
version 1.5
@author: Gary Kokaisel

Resources:
Regular expression operations, http://docs.python.org/2/library/re.html
Python regular expressions, http://www.tutorialspoint.com/python/python_reg_expressions.htm
Regular Expressions Syntax Referance, http://www.regular-expressions.info/reference.html
Online pythonic regex tool http://re-try.appspot.com/
Easy GUI tutorial, http://www.ferg.org/easygui/tutorial.html#contents_item_9.2
'''

import sys
import string
import zipfile, re
import easygui

answer_regex =\
r'''

(^Answer|\nAnswer|Answer:|ANSWER:|ANS:)(.*)                            # find answer key in its many variations

'''
true_false_regex =\
r'''

(Answer:\s+True)|(Answer:\s+False)
|(Answer\s+True)|(Answer\s+False)
|(ANS:\s+True)|(ANS:\s+False)

'''
feedback_regex =\
r'''

(Diff:.*|Topic:.*|Skill:.*|Geog\sStandards:.*                          # find common feedback terms...
|Bloom's\sTaxonomy:.*|AACSB:.*|Question\sStatus:.*)                    # Diff: 3
                                                                       # Topic:  Shape of Earth
                                                                       # Geog Standards:  New Geog Standards 4
                                                                       # Bloom's Taxonomy:  Knowledge

'''
stats_regex =\
r'''

(%.*)                                                       # removes any stastical type of feedback from test...
                                                            # % correct 60      a= 60  b= 7  c= 18  d= 16      r = .21

'''
regexes = [true_false_regex, answer_regex, feedback_regex, stats_regex]

def main():
    def process_test(test):
        answer_match = string_find(answer_regex, test)
        if answer_match:
            answer_key = [x[1] for x in answer_match]
            test = string_replace(regexes[0], "A) True\nB) False\n", test)
            for regex in regexes[1:2]:
                test = string_replace(regex, '', test)
            print test
            format_answers(answer_key)

    def string_replace(pattern, string_old, string_new):
        return re.sub(pattern, string_old, string_new, flags=re.I | re.X)

    def string_find(pattern, string):
        return re.findall(pattern, string, flags=re.I | re.X)

    def format_answers(answers):
        print 'Answers:'
        number = 0
        for answer in answers:
            number += 1
            answers = str(number) + '.' + answer.replace(":", "")
            answers = string_replace(regexes[3], "", answers)
            print string.capwords(answers)

    msg = "This program will attempt to format a test file for use with Respondus, Do you want to continue?"
    title = "Respondus Format Utility version 1.5 Beta"
    if easygui.ccbox(msg, title):
        pass
    else:
        sys.exit(0)
    sys.stdout = open(easygui.filesavebox(msg='Before we begin choose where to save your formatted test file?',
                                          default='formatted_test.txt'), 'w')
    file_choice = easygui.indexbox(msg="Choose the file type of your test file (Note: Word is very experimental)",
                                   choices=("Plain text file (.txt)", "Word 2007, 2010 file (.docx)", "Quit"))
    if file_choice is 0:
        input_file = easygui.fileopenbox(msg='Where is the test file to format?')
        try:
            with open(input_file) as inputFileHandle:
                process_test(inputFileHandle.read().replace("\n", "\n\n"))
        except IOError:
            sys.stderr.write('Could not open %s\n' % input_file)
            sys.exit(-1)
    elif file_choice is 1:
        docx = zipfile.ZipFile(easygui.fileopenbox(msg='Where is the test file to format?'))
        content = docx.read('word/document.xml')
        process_test(re.sub('<(.|\n)*?>', '\n', content))
    else:
        sys.exit(0)
    easygui.msgbox("Format complete!", ok_button="Close", image="tick_64.png")
    sys.stdout.flush()
    sys.stdout.close()

if __name__ == "__main__":
    main()
