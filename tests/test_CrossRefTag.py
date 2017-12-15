import CrossRefTag as cs


def test_answer():
    wd = 'cat'
    list1 = ['man','lion']
    assert cs.check_pattern(wd, list1)==None
#----------------------------------------------------------------------------------#
def test_answer1():
    assert  cs.digit_lenght_check('1') == '001'
#----------------------------------------------------------------------------------#
def test_answer3():
    code = '00100500100'
    verse_list = ['00100500100']
    assert  cs.tag_format(code,verse_list) == '\\fSPT+SPT\\fr 5:1 \\ft Previous: ; Next: \\ft*'
#----------------------------------------------------------------------------------#
def test_answer4():
    code = '00100500100'
    verse_list = '00100500100'
    assert  cs.verse_handler(code,verse_list) == '\\v 1 00100500100'
#----------------------------------------------------------------------------------#
def test_answer5():
    verse_code_tuple = (00100500100, 0)
    verse = 'God is love'
    assert  cs.add_tags(verse_code_tuple, verse)
#----------------------------------------------------------------------------------#
def test_answer6():
    filename = '02EXOHii.SFM'
    assert  cs.usfm_handler(filename)
