import re
from sklearn.model_selection import train_test_split
from sklearn import linear_model

vowel_phonemes_list = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']
vowel_phonemes_set = set(vowel_phonemes_list)
consonant_phonemes_list = ['P', 'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M',
     'N', 'NG', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
consonant_phonemes_set = set(consonant_phonemes_list)
con_vowel_list = consonant_phonemes_list + vowel_phonemes_list
def get_phonemes_without_number(phonemes):
    phonemes_without_number = []
    for phoneme in phonemes:
        if phoneme[-1].isdigit():
            phonemes_without_number.append(phoneme[:-1])
        else:
            phonemes_without_number.append(phoneme)
    return phonemes_without_number

def get_vowel_consonant_map(phonemes):
    vowel_map = [0] * len(vowel_phonemes_list)
    consonant_map = [0] * len(consonant_phonemes_list)

    for phoneme in phonemes:
        #print(phoneme)
        if phoneme in vowel_phonemes_set:
            vowel_map[vowel_phonemes_list.index(phoneme) - 1] += 1
        elif phoneme in consonant_phonemes_set:
            consonant_map[consonant_phonemes_list.index(phoneme) - 1] += 1
        else:
            print("wrong! with ", phoneme)
    return vowel_map, consonant_map

def get_vowel_consonant_bitmap(phonemes):
    bitmap = [-1] * 15
    for phoneme_index in range(len(phonemes)):
        if phonemes[phoneme_index] in vowel_phonemes_set:
            bitmap[phoneme_index] = 1
        else:
            bitmap[phoneme_index] = 0
    return bitmap
         
def get_phonemes_map(phonemes):
    phonemes_map = [-1] * 15
    for phoneme_index in range(len(phonemes)):
        phonemes_map[phoneme_index] = con_vowel_list.index(phonemes[phoneme_index])
    return phonemes_map
################# preprocessing #################
def preprocess(unprocessed_data):
    X = []
    Y = []
    count = 0
    max_phonemes_len = -1
    max_ph_len_word = ""
    for line in unprocessed_data:
        pos_primary_stress = -1
        parts = re.split("\s|:", line)
        phonemes = parts[1:]
        phonemes_without_number = get_phonemes_without_number(phonemes)
        word = parts[0]
        vowels = []
        consonants = []
        primary_stress = ""
        
        for index in range(1, len(parts)):
            if re.match('[a-zA-Z]+\d', parts[index]): #若是vowel则尾部必带有数字
                vowels.append(parts[index])
            else:
                consonants.append(parts[index])
            if parts[index].find('1') != -1: #若含有'1'则是primary_stress
                primary_stress = parts[index]
        
        is_first_phoneme_vowel = int(parts[1] == vowels[0])
        is_second_phoneme_vowel = int(parts[2] == vowels[0])
        pos_first_vowel = phonemes.index(vowels[0]) + 1
        pos_primary_stress_in_vowel = vowels.index(primary_stress)
        end_phoneme = con_vowel_list.index(phonemes_without_number[-1])
        vowel_map, consonant_map = get_vowel_consonant_map(phonemes_without_number)
        phonemes_map = get_phonemes_map(phonemes_without_number)
        vowel_consonant_bitmap = get_vowel_consonant_bitmap(phonemes_without_number)
        #if pos_primary_stress == 0:
            #print("这个单词", word, "的首个发音为pri_stress")      
        
        if count < 20:
            print(vowel_map)
            print(consonant_map)
            print(phonemes_map)
            print(pos_first_vowel)
            print(parts)
            
            
            count += 1
            
        #x = [len(word), len_phonemes, len(vowels), len(consonants), is_first_phoneme_vowel]    
        if len(vowels) == 1:
            print(line)
        if len(phonemes) > max_phonemes_len:
            max_phonemes_len = len(phonemes)
            max_ph_len_word = phonemes + [word]
        x = [len(vowels)/len(phonemes), len(consonants)/len(phonemes), end_phoneme, len(phonemes)]
        x += vowel_map + consonant_map + vowel_consonant_bitmap
        X.append(x)
        Y.append(pos_primary_stress_in_vowel)
    print('max is: ', max_phonemes_len, " ", max_ph_len_word)
    return X, Y
################# training #################

def train(data, classifier_file):# do not change the heading of the function
    X, Y = preprocess(data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42)
    clf = linear_model.SGDClassifier()
    clf.fit(X_train, Y_train)
    fo = open(classifier_file, "w")
    fo.write(clf)
    pass # **replace** this line with your code    

################# testing #################

def test(data, classifier_file):# do not change the heading of the function
    return [1, 1, 2, 1]