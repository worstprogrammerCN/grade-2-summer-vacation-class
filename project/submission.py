import re
from sklearn.model_selection import train_test_split
from sklearn import linear_model

################# preprocessing #################
def preprocess(unprocessed_data):
    X = []
    Y = []
    count = 0
    for line in unprocessed_data:
        pos_primary_stress = -1
        parts = re.split("\s|:", line)
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
        if count < 4:
            print(parts)
            count += 1
        len_stresses = len(parts[1:])
        is_first_vowel_primary = int(primary_stress == vowels[0])
        pos_primary_stress_in_vowel = vowels.index(primary_stress)
        #if pos_primary_stress == 0:
            #print("这个单词", word, "的首个发音为pri_stress")
        x = [len(word), len_stresses, len(vowels), len(consonants), pos_primary_stress, is_first_vowel_primary]
        X.append(x)
        Y.append(pos_primary_stress_in_vowel)
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