import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn import linear_model

from sklearn.externals import joblib


vowel_phonemes = set(['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW'])
consonant_phonemes = set(['P', 'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M',
     'N', 'NG', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'])
################# preprocessing for reading test_data #####################
def preprocess_test(unprocessed_data):
    X = []
    count = 0
    for line in unprocessed_data:
        parts = re.split("\s|:", line)
        vowels = []
        constants = []
        primary_stress = ""
        for index in range(1, len(parts)):
            phoneme = parts[index]
            if phoneme in vowel_phonemes:
                vowels.append(parts[index])
            else if phoneme in consonant_phonemes:
                consonants.append(parts[index])
            else:
                print("error!")
                return
        if count < 4:
            print(parts)
            count += 1
        
        len_word = len(parts[0])
        len_stresses = len(parts[1:])
        is_first_vowel_primary = int(primary_stress == vowels[0])
        x = [len_word, len_stresses, len_vowels, len_consonants, is_first_vowel_primary]

        X.append(x)
################# preprocessing for reading training_data #################
def preprocess(unprocessed_data):
    X = []
    Y = []
    count = 0
    for line in unprocessed_data:
        parts = re.split("\s|:", line)
        word = parts[0]
        pos_primary_stress = -1
        primary_stress = ""
        vowels = []
        consonants = []
        for index in range(1, len(parts)):
            if re.match('[a-zA-Z]+\d', parts[index]): #若是vowel则尾部必带有数字
                vowels.append(parts[index])
            else:
                consonants.append(parts[index])
            if parts[index].find('1') != -1: #若含有'1'则是primary_stress
                primary_stress = parts[index]
        if count < 4:
            print(parts)
            count += 1

        len_phonemes = len(parts[1:])
        is_first_vowel_primary = int(primary_stress == vowels[0])
        pos_primary_stress_in_vowel = vowels.index(primary_stress)
        x = [len(word), len_phonemes, len(vowels), len(consonants), is_first_vowel_primary]

        X.append(x)
        Y.append(pos_primary_stress_in_vowel)
    return X, Y
################# training #################

def train(data, classifier_file):# do not change the heading of the function
    X, Y = preprocess(data)
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.33, random_state=42)
    clf = linear_model.SGDClassifier()
    clf.fit(X_train, Y_train)
    #fo = open(classifier_file, "w")
    #fo.write(clf)
    joblib.dump(clf, classifier_file) 
    pass # **replace** this line with your code    

################# testing #################

def test(data, classifier_file):# do not change the heading of the function
    clf = joblib.load(classifier_file)
    return clf.predict(data)
    