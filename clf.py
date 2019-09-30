from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
class classifier():
    def __init__(self,clf = SVC,**kwargs):
        self._clf = clf(**kwargs)

    def fit(self,data,label):
        self._clf.fit(data,label)

    def predict(self,data):
        return self._clf.predict(data)

    def evaluate(self,y_true,predict):
        return accuracy_score(y_true,predict)
