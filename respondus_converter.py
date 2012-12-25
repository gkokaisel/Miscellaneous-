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

answer_regexes = \
    r'''
            
(Answer|Answer:|ANSWER:|ANS:)(.*)                                      # find answer key in its many variations                                        
                                        

            '''
feedback_regexes = \
r'''

(Diff:.*|Topic:.*|Skill:.*|Geog\sStandards:.*|Bloom's\sTaxonomy:.*|AACSB:.*|Question\sStatus:.*)    
                                                                       # find common feedback terms...
                                                                       # Diff: 3
                                                                       # Topic:  Shape of Earth
                                                                       # Geog Standards:  New Geog Standards 4
                                                                       # Bloom's Taxonomy:  Knowledge

'''
stastical_regexes = \
r'''

(\%.*)                                                                 # removes any stastical type of feedback from test...
                                                                       # % correct 60      a= 60  b= 7  c= 18  d= 16      r = .21   
                                                                                                                                                
'''

# helper function to distinquish between test questions and test answer key 
def process_test_file(test_file):      
    answer_key = []
    # re.I ignores letter case, and re.X ignores comments and whitespace (unless included in pattern) within regular expression      
    answer_match = re.findall(answer_regexes, test_file, flags=re.I | re.X)
 
    if answer_match:   
        # list comprehension to return just the letter answer within tuple
        answer_key = [x[1] for x in answer_match]
        
        # sustitute answers with empty string   
        clean_test = re.sub(answer_regexes, '', test_file, flags=re.I | re.X)      
        print re.sub(feedback_regexes, '', clean_test, flags=re.I | re.X)   
        format_answer_key(answer_key)
         
# helper function to format answer key in Respondus format   
def format_answer_key(answer_key):   
  
     
    # the following code will print answer key as a numerically ordered list of answers in Respondus format  
    print 'Answers:'
    number = 0
    for answer in answer_key:       
        number += 1    
        # append ordered numbers to answer key   
        answer_key = str(number) + '.' + answer
        
        # remove any stastical type feedback from answer key
        print re.sub(stastical_regexes, "", answer_key, flags=re.I | re.X)


# main function to launch program dialog, and to set input and output file paths
def main():
    
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
                process_test_file(test_file)
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
        process_test_file(test_file)
    else:
        sys.exit(0)  
        
    # flush and close output
    output_file.flush()
    output_file.close()
    sys.stdout = save_output
            

if __name__ == "__main__":
    main()


# load GUI to display success message
easygui.msgbox("Format complete!", ok_button="Close", image="tick_64.png")


