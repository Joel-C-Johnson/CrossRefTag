# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import string
import nltk
import pdb
import glob

tree1 = ET.parse('ProjectBiblicalTerms.xml')
root1 = tree1.getroot()

tree2 = ET.parse('BiblicalTermsHii.xml')
root2 = tree2.getroot()

main_dict = {} # to store the final output
term_dict = {} # to save the bible terms and their Hindi transliteration
term_reference_dict = {}
# The terms and the transliteration are generatedTermRendering first

for renders in root2[0]:    #root2[0] is the tag TermRendering object in BiblicalTermsHii
    # pdb.set_trace()
    Id = renders.find('Id').text    # Id tag conatins the term
    renderings = renders.find('Renderings').text  #Renderings contain the transliterated terms
    
    if renderings != None:
        translation_words = renderings.split(',')
    else:
        translation_words = ['']
    term_dict[Id] = translation_words


for t in root1.findall('Term'):
    word = t.find('Transliteration').text   #This is the term word
    term_reference_list = []
    for v in t[3]:
        verse_code = v.text # The code of the verse
        term_reference_list.append(verse_code)
        if verse_code not in main_dict: # If a verse code is not in the main_dict, then insert it directly without having to check
            main_dict[verse_code] = {word: term_dict[word]}
        else: # If the verse code is already in then it needs to be added to the value of the main_dict[verse_code]
            temp_dict = main_dict[verse_code]
            temp_dict[word] = term_dict[word]
            main_dict[verse_code] = temp_dict
    term_reference_dict[word] = term_reference_list

books = {"1": "GEN", "2": "EXO", "3": "LEV", "4": "NUM", "5": "DEU", "6": "JOS", "7": "JDG", "8": "RUT", "9": "1SA", "10": "2SA", "11": "1KI", "12": "2KI", "13": "1CH", "14": "2CH", "15": "EZR", "16": "NEH", "17": "EST", "18": "JOB", "19": "PSA", "20": "PRO", "21": "ECC", "22": "SNG", "23": "ISA", "24": "JER", "25": "LAM", "26": "EZK", "27": "DAN", "28": "HOS", "29": "JOL", "30": "AMO", "31": "OBA", "32": "JON", "33": "MIC", "34": "NAM", "35": "HAB", "36": "ZEP", "37": "HAG", "38": "ZEC", "39": "MAL", "40": "MAT", "41": "MRK", "42": "LUK", "43": "JHN", "44": "ACT", "45": "ROM", "46": "1CO", "47": "2CO", "48": "GAL", "49": "EPH", "50": "PHP", "51": "COL", "52": "1TH", "53": "2TH", "54": "1TI", "55": "2TI", "56": "TIT", "57": "PHM", "58": "HEB", "59": "JAS", "60": "1PE", "61": "2PE", "62": "1JN", "63": "2JN", "64": "3JN", "65": "JUD", "66": "REV"}
books_inverse = {v:k for k,v in books.items()} 

def check_pattern(tr_word, tr_wordlist):
    'Checks if a word selected from the usfm file has a match from the translated word list'
    if tr_wordlist:
       for wd in tr_wordlist:
            match = re.search(tr_word, wd)
            if match:
                pattern = match.group()
                return pattern
    else:
        return None

def digit_lenght_check(num):
    '''to convert all book, chapter and verse codes to 3 digit values
     to match the verse code from the "ProjectBiblicalTerms" file'''
    if len(num) == 1:
        return '00' + num
    else:
        return '0' + num

def tag_format(code, verse_list):
    'adds the tagging format to a word and returns the value'
    current_code = str(int(code[3:6])) + ":" + str(int(code[6:9]))
    previous_index = None
    next_index = None
    if code in verse_list:
        index_value = verse_list.index(code)
        if len(verse_list) == 1:
            previous_index = None
            next_index = None
        elif index_value == 0:
            next_index = index_value + 1
        elif index_value > 0 and (index_value + 1) == len(verse_list):
            previous_index = index_value - 1
        else:
            previous_index = index_value - 1
            next_index = index_value + 1
    else:
        previous_index = None
        next_index = None

    if previous_index is not None:
        previous_code = books[str(int(verse_list[previous_index][0:3]))] + ' ' + str(int(verse_list[previous_index][3:6])) + ':' + str(int(verse_list[previous_index][6:9]))
    else:
        previous_code = ''
    if next_index is not None:
        next_code = books[str(int(verse_list[next_index][0:3]))] + ' ' + str(int(verse_list[next_index][3:6])) + ':' + str(int(verse_list[next_index][6:9]))
    else:
        next_code = ''
    formatted = "\\f + \\fr " + str(current_code) +" \\ft Previous: " + str(previous_code) + "; Next: " + str(next_code) + "\\ft*"
    return formatted

def verse_handler(code, verse):
    'Returns a string back starting in the format "\\v (digit)"'
    verse_num = str(int(code[6:9]))
    final_verse = '\\v ' + str(verse_num) + ' ' + verse
    return final_verse

def add_tags(verse_code_tuple, verse):
    '''Recieves a tuple with verse code and number(string) and the verse as 
    argumenats Each word in the verse is looked up against a list of the bible 
    terms of that specific verse for a match and returns a text with the chain 
    reference formatted tags added to it.'''
    punct_handler = re.sub(r'\s([' + string.punctuation +'])', r'SPT\1', verse)
    punct_handler = re.sub(r'([' + string.punctuation +'])\s', r'\1SPT', punct_handler)
    punct_handler = re.sub(r'([' + string.punctuation +'])', r' \1 ', punct_handler)  #SPT is a marker
    word_list = nltk.word_tokenize(punct_handler)
    main_word_list = []
    verse_code_length = int(verse_code_tuple[1]) + 1
    verse_code = verse_code_tuple[0]
    book_code = verse_code[0:3]
    chapter_code = verse_code[3:6]
    refer_code = verse_code[6:9]
    verse_code_list = []
    for i in range(0, verse_code_length):
        current_value = book_code + chapter_code + digit_lenght_check(str(int(refer_code) + i)) + '00'
        verse_code_list.append(current_value)
    for word in word_list:
        word_list_len = len(main_word_list)
        for v_code in verse_code_list:
            if v_code not in main_dict:
                continue
            else:
                for k, v in main_dict[v_code].items():
                    translation_check = check_pattern(word, v)
                    if translation_check:
                        verse_text = word + tag_format(v_code, term_reference_dict[k])
                        main_word_list.append(verse_text)
                        break
        if len(main_word_list) == word_list_len:
            main_word_list.append(word)
    join_main_word_list = " ".join(main_word_list)
    main_word_text = re.sub(r"``", '"', join_main_word_list)
    main_word_text = re.sub(r'\s([' + string.punctuation + '])\s', r'\1', main_word_text)
    main_word_text = re.sub(r'SPT', ' ', main_word_text)
    return main_word_text

def usfm_handler(filename):
    'To process the usfm files'
    open_file = open(filename, 'r')
    file_text = open_file.read()
    main_text_list = [] 
    chapter_pattern = re.compile('(\\c )(\d+)')
    book_name = re.search('(?<=\id )\w{3}', file_text).group(0)
    book_num = books_inverse[book_name]
    book_code = digit_lenght_check(book_num)
    file_text = re.sub('\*', 'asterix', file_text)
    file_text = re.sub('\?', 'questionmark', file_text)
    file_text = re.sub('\(', 'opening_bracket', file_text) 
    file_text = re.sub('\)', 'closing_bracket', file_text)
    file_text = re.sub('\[', 'openingsquarebracket', file_text)
    file_text = re.sub('\]', 'closingsquarebracket', file_text)
    split_usfm = file_text.split('\\c')
    i = 0
    for chapter_text in split_usfm:
        if i == 0:
            main_text_list.append(chapter_text)
            i += 1
            continue
        else:
            chapter_text = "\\c" + chapter_text
            chapter_number = re.search(chapter_pattern, (chapter_text.split('\n')[0])).group(2)
            chapter_code = digit_lenght_check(chapter_number)
            verse_pattern = re.compile(r'(\\v )(\d+)(.*)')
            verse_pattern2 = re.compile(r'(\\v )(\d+)[abcd]?-(\d+)[abcd]?')
            split_text = chapter_text.split('\\v')
            main_text_list.append(split_text.pop(0))
            for line in split_text:
                
                other_filter_pattern = re.compile(r'\n(\\)(.*)')
                line = re.sub(other_filter_pattern, r'SPTnewlineslSPT\2', line)
                line = "\\v" + line
                result = re.match(verse_pattern, line)
                if result:
                    verse = result.group(3)
                    hypen_verse = re.match(verse_pattern2, line)
                    if hypen_verse:
                        
                        len_reference_code = int(hypen_verse.group(3)) - int(hypen_verse.group(2))
                        first_verse = str(book_code) + str(chapter_code) + digit_lenght_check(hypen_verse.group(2)) + '00'
                        verse_code = (first_verse, str(len_reference_code))
                    else:
                        reference_code = digit_lenght_check(result.group(2))
                        verse_sub = re.sub(verse_pattern, r'' + str(book_code) + str(chapter_code) + str(reference_code) + '00' + str(verse), line)
                        verse_code = (verse_sub[0:11], '0')
                    filtered_line = add_tags(verse_code, verse)
                    actual_verse = verse_handler(verse_code[0], filtered_line)  # A verse line as how it appears on the usfm file
                    main_text_list.append(actual_verse)
                else:
                    main_text_list.append(line)
    final_text = "\n".join(main_text_list)
    final_text = re.sub('opening_bracket', r'(', final_text)
    final_text = re.sub('closing_bracket', r')', final_text)
    final_text = re.sub(' newlinesl ', r'\n\\', final_text)
    final_text = re.sub(r'\\v (\d+) - (\d+)', r'\\v \1-\2', final_text)
    final_text = re.sub('asterix', '*', final_text)
    final_text = re.sub('questionmark', '?', final_text)
    file_text = re.sub('openingsquarebracket', '[', file_text)
    file_text = re.sub('closingsquarebracket', ']', file_text)
    open_file = open('output/' + str(filename), 'w')
    open_file.write(final_text)
    return 'finished'

for filename in glob.glob('usfmfiles/*.SFM'):
    usfm_handler(filename)

