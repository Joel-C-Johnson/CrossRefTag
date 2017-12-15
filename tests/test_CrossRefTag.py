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
    assert  cs.tag_format(code,verse_list) == 00
#----------------------------------------------------------------------------------#
#
# def verse_handler(code, verse):
#     'Returns a string back starting in the format "\\v (digit)"'
#     verse_num = str(int(code[6:9]))
#     final_verse = '\\v ' + str(verse_num) + ' ' + verse
#     return final_verse
#
# def test_answer4():
#     code = '00100500100'
#     verse_list = '00100500100'
#     assert  verse_handler(code,verse_list) == '\\v 1 00100500100'
