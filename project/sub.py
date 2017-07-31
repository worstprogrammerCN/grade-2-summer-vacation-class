## import modules here 
import helper
import submission
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model
from sklearn import model_selection
from sklearn.kernel_approximation import RBFSampler
import matplotlib.pyplot as plt

training_data = helper.read_data('./asset/training_data.txt')
classifier_path = './asset/classifier.dat'
#submission.train(training_data, classifier_path)

#test_data = helper.read_data('./asset/tiny_test.txt')
#prediction = submission.test(test_data, classifier_path)
#print(prediction)  
data = helper.read_data('./asset/training_data.txt')
X, Y = submission.preprocess(data)
k_range = range(1, 15)
k_scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = model_selection.cross_val_score(knn, X, Y, cv=5, scoring='accuracy')
    print("k=",k," scores are", scores)
    k_scores.append(scores.mean())

plt.plot(k_range, k_scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Cross-Validated Accuracy')
plt.show()
#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=10)
#print(f1_score(Y_test, prediction, average='micro'))

