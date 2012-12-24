#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 21, 2012
Program for converting tests to Respondus format
@author: Gary Kokaisel
'''

import sys
import zipfile, re
import easygui  # http://www.ferg.org/easygui/tutorial.html#contents_item_9.2

# regular expressions to find test_file answers (very useful pythonic regex tool online http://re-try.appspot.com/)

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
            
# initialize global variables

# boolean flags are for each regular expression case
case_one = False
case_two = False
case_three = False
case_four = False

# a list for storing answers
answer_key = []

# some strings for working with the i/o files
save_output = ''
output_file = ''
test_file = ''

# helper function to launch program dialog, and to set input and output file paths
def set_file_paths():
    global save_output, output_file, test_file
    
    # load GUI to begin program dialog   
    msg = "This program will attempt to format a test file for use with Respondus, Do you want to continue?"
    title = "Respondus Format Utility version 1.0 Beta"
    if easygui.ccbox(msg, title):  # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:  # user chose Cancel
        sys.exit(0)
    
    # launch GUI to choose location for output file    
    save_output = sys.stdout
    output_file = open(easygui.filesavebox(msg='Before we begin choose where to save your formatted test file?',
                   default='formatted_test.txt'), 'w')
    sys.stdout = output_file
    
    # launch GUI to load test file, and store as string (replacing singles lines with double lines to make matching regexes easier)    
    file_choice = easygui.indexbox(msg="Choose the file type of your test file (Note: Word is very experimental)",
                                   choices=("Plain text file (.txt)", "Word 2007, 2010 file (.docx)", "Quit"))
    
    if file_choice is 0:   
        
        # launch GUI to load test file     
        input_file = easygui.fileopenbox(msg='Where is the test file to format?')
        try:
            with open(input_file) as inputFileHandle:
                test_file = inputFileHandle.read().replace('\n', '\n\n')
        except IOError:
            sys.stderr.write('Could not open %s\n' % input_file)
            sys.exit(-1)  
        
    elif file_choice is 1: 
        
        # launch GUI to load document and unzip files       
        docx = zipfile.ZipFile(easygui.fileopenbox(msg='Where is the test file to format?'))
        
        # load xml document from word directory
        content = docx.read('word/document.xml')
        
        # substitute xml tags with line breaks (still needs tweaking, but sorta works)     
        test_file = re.sub('<(.|\n)*?>', '\n', content)
    else:
        sys.exit(0)
 
# helper function to distinquish between test questions and test answer key 
def process_test_file():      
    global answer_key, case_one, case_two, case_three, case_four           
    # find matches for the various regular expression cases
    # re.I ignores letter case, and re.X ignores comments and whitespace (unless included in pattern) within regular expression
    
    # If case 1    
    answer_match = re.findall(regex_case_one, test_file, flags=re.I | re.X)
    if answer_match:
        case_one = True
        answer_key = answer_match        
    
        # prints the test questions without answer key by substituting matched answers with empty string    
        print re.sub(regex_case_one, '', test_file, flags=re.I | re.X)
        
    
    # If case 2    
    answer_match = re.findall(regex_case_two, test_file, flags=re.I | re.X)
    if answer_match:
        case_two = True
        answer_key = answer_match
        
        # prints the test questions without answer key by substituting matched answers with empty string   
        print re.sub(regex_case_two, '', test_file, flags=re.I | re.X)
       
    
    # If case 3    
    answer_match = re.findall(regex_case_three_a, test_file, flags=re.I | re.X)
    if answer_match:
        case_three = True
        answer_key = answer_match
        
        # prints the test questions without answer key by substituting matched answers with empty string    
        print re.sub(regex_case_three_b, '', test_file, flags=re.I | re.X)
    
    
    # If case 4    
    answer_match = re.findall(regex_case_four_a, test_file, re.I | re.X)
    if answer_match:
        case_four = True
        answer_key = answer_match
        
        # prints the test questions without answer key by substituting matched answers with empty string     
        print re.sub(regex_case_four_b, '', test_file, flags=re.I | re.X)
       
# helper function to format answer key in Respondus format   
def format_answer_key():   
    global answer_key, case_one, case_two, case_three, case_four    
     
    # the following code will print answer key as a numerically ordered list of answers in Respondus format  
    print 'Answers:'
    number = 0
    for answer in answer_key:
        number += 1
    
        # append ordered numbers to answer key   
        answer_key = str(number) + '.' + answer
    
        # remove the word answer from answer key ignoring case sensitivity    
        if case_one or case_three:
    
            # returns the answer string in qoutes wherever found without case sensitivity    
            insensitive_answer = re.compile(re.escape('answer'), flags=re.I)
    
            # substitutes the answer string with an empty string (thereby removing it from list)    
            print insensitive_answer.sub('', answer_key)
            
        elif case_two:
            
            # returns the answer string in qoutes wherever found without case sensitivity    
            insensitive_answer = re.compile(re.escape('ans:'), flags=re.I)
            
            # substitutes the answer string with an empty string (thereby removing it from list)  
            print insensitive_answer.sub('', answer_key)
            
        elif case_four:
            
            # returns the answer string in qoutes wherever found without case sensitivity   
            insensitive_answer = re.compile(re.escape('answer:'), flags=re.I)
            
            # substitutes the answer string with an empty string (thereby removing it from list)  
            print insensitive_answer.sub('', answer_key)

# load helper functions
set_file_paths()
process_test_file()
format_answer_key()

# load GUI to display success message
easygui.msgbox("Format complete!", ok_button="Close", image="tick_64.png")

# flush and close output
output_file.flush()
output_file.close()
sys.stdout = save_output
