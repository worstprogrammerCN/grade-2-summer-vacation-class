## import modules here 
import helper
import submission
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn import linear_model

training_data = helper.read_data('./asset/training_data.txt')
classifier_path = './asset/classifier.dat'
#submission.train(training_data, classifier_path)

#test_data = helper.read_data('./asset/tiny_test.txt')
#prediction = submission.test(test_data, classifier_path)
#print(prediction)  
data = helper.read_data('./asset/training_data.txt')
X, Y = submission.preprocess(data)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
clf = linear_model.SGDClassifier()
clf.fit(X_train, Y_train)
prediction = clf.predict(X_test)

print(f1_score(Y_test, prediction, average='micro'))

input("wait for exit......")