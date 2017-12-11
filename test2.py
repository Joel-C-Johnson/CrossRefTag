import xml.etree.ElementTree as ET
import json
import pdb


tree1 = ET.parse('ProjectBiblicalTerms.xml')
idRef = tree1.getroot()

tree2 = ET.parse('BiblicalTermsHii.xml')
idTrans = tree2.getroot()

main_dict = {} # to store the final output
term_dict = {} # to save the bible terms and their Hindi translation


pdb.set_trace()
# The terms and the transliteration are generatedTermRendering first
for renders in idTrans[0]:    #idTrans[0] is the tag TermRendering object in BiblicalTermsHii
    Id = renders.find('Id').text    # Id tag conatins the term
    renderings = [renders.find('Renderings').text]  #Renderings contain the transliterated terms
    try:
        term_dict[Id] = renderings#[0].encode("utf-8").decode("utf-8")
    except:
        pass


for t in idRef.findall('Term'):
    word = t.find('Transliteration').text   #This is the term word
    for v in t[3]:
        verse_code = v.text # The code of the verse
        if verse_code not in main_dict: # If a verse code is not in the main_dict, then insert it directly without having to check
            main_dict[verse_code] = {word: term_dict[word]}
        else: # If the verse code is already in then it needs to be added to the value of the main_dict[verse_code]
            temp_dict = main_dict[verse_code]
            temp_dict[word] = term_dict[word]
            main_dict[verse_code] = temp_dict

# this is to write to external file
obj = open('data.json', 'wb')
data = json.dumps(main_dict)
obj.write(data)
obj.close