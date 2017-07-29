## import modules here 
import helper
import submission
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn import linear_model

training_data = helper.read_data('./asset/training_data.txt')
classifier_path = './asset/classifier.dat'
submission.train(training_data, classifier_path)

test_data = helper.read_data('./asset/tiny_test.txt')
prediction = submission.test(test_data, classifier_path)
ground_truth = [1, 1, 2, 1]
print(f1_score(ground_truth, prediction, average='micro'))

input("wait for exit......")