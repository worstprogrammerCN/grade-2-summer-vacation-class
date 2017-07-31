import re
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib

vowel_phonemes_list = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']
vowel_phonemes_set = set(vowel_phonemes_list)
consonant_phonemes_list = ['P', 'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M',
     'N', 'NG', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
consonant_phonemes_set = set(consonant_phonemes_list)
con_vowel_list = consonant_phonemes_list + vowel_phonemes_list

max_pho_len = 17
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
        if phoneme in vowel_phonemes_set:
            vowel_map[vowel_phonemes_list.index(phoneme)] += 1
        elif phoneme in consonant_phonemes_set:
            consonant_map[consonant_phonemes_list.index(phoneme)] += 1
    return vowel_map, consonant_map

def get_vowel_consonant_bitmap(phonemes):
    bitmap = [-1] * max_pho_len
    for phoneme_index in range(len(phonemes)):
        if (phoneme_index + 1) > max_pho_len:
            return bitmap
        if phonemes[phoneme_index] in vowel_phonemes_set:
            bitmap[phoneme_index] = 1
        else:
            bitmap[phoneme_index] = 0
    return bitmap

def is_vowel(phoneme):
    return phoneme[-1].isdigit()
def is_consonant(phoneme):
    return not phoneme[-1].isdigit()
def is_pri_stress(phoneme):
    return phoneme[-1] == '1'
def get_vows_cons_pri_stress_train(phonemes):
    vowels = []
    consonants = []
    primary_stress = ""
    for phoneme in phonemes:
        if is_vowel(phoneme):
            vowels.append(phoneme)
        elif is_consonant(phoneme):
            consonants.append(phoneme)
        if is_pri_stress(phoneme):
            primary_stress = phoneme
    return vowels, consonants, primary_stress
################# preprocessing #################

################# training #################
def preprocess(unprocessed_data):
    X = []
    Y = []
    for line in unprocessed_data:
        pos_primary_stress = -1
        parts = re.split("\s|:", line)
        phonemes = parts[1:]
        phonemes_without_number = get_phonemes_without_number(phonemes)
        vowels, consonants, primary_stress = get_vows_cons_pri_stress_train(phonemes)
        
        
        end_phoneme = con_vowel_list.index(phonemes_without_number[-1])
        vowel_map, consonant_map = get_vowel_consonant_map(phonemes_without_number)
        vowel_consonant_bitmap = get_vowel_consonant_bitmap(phonemes_without_number)
        
        pos_primary_stress_in_vowel = vowels.index(primary_stress) + 1
        x = [len(vowels)/len(phonemes), len(consonants)/len(phonemes), len(phonemes), end_phoneme] + vowel_map + consonant_map + vowel_consonant_bitmap
        X.append(x)
        Y.append(pos_primary_stress_in_vowel)
    return X, Y
def train(data, classifier_file):# do not change the heading of the function
    X, Y = preprocess(data)
    clf = KNeighborsClassifier(n_neighbors=5)
    clf.fit(X, Y)
    joblib.dump(clf, classifier_file)
    return Y

################# testing #################
def get_vows_cons_pri_stress_test(phonemes):
    vowels = []
    consonants = []
    for phoneme in phonemes:
        if phoneme in vowel_phonemes_set:
            vowels.append(phoneme)
        elif phoneme in consonant_phonemes_set:
            consonants.append(phoneme)
    return vowels, consonants
def preprocess_test(unprocessed_data):
    X = []
    for line in unprocessed_data:
        parts = re.split("\s|:", line)
        phonemes = phonemes_without_number = parts[1:]
        vowels, consonants = get_vows_cons_pri_stress_test(phonemes_without_number)
        
        
        end_phoneme = con_vowel_list.index(phonemes_without_number[-1])
        vowel_map, consonant_map = get_vowel_consonant_map(phonemes_without_number)
        vowel_consonant_bitmap = get_vowel_consonant_bitmap(phonemes_without_number)

        x = [len(vowels)/len(phonemes), len(consonants)/len(phonemes), len(phonemes), end_phoneme] + vowel_map + consonant_map + vowel_consonant_bitmap
        X.append(x)
    return X
def test(data, classifier_file):# do not change the heading of the function
    X = preprocess_test(data)
    clf = joblib.load(classifier_file)
    Y = clf.predict(X)
    prediction = []
    for y in Y:
        prediction.append(int(y))
    #for p in prediction:
     #   print(type(p))
     #   print('is int?', p is int, ' p:', p)
    return prediction