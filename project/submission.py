################# preprocessing #################
def preprocess(unprocessed_data):
    
    data = unprocessed_data
    for line in data:
        line = [1, 2]
    return data
################# training #################

def train(data, classifier_file):# do not change the heading of the function
    data = preprocess(data)
    print(data[:4])
    pass # **replace** this line with your code    

################# testing #################

def test(data, classifier_file):# do not change the heading of the function
    return [1, 1, 2, 1]