import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier,GradientBoostingClassifier,ExtraTreesClassifier,AdaBoostClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from numpy import random


import clf
import parameter
import toolbox
import feature_selection
def main():
    ##参数设置
    target_file = '/media/rong/My Passport/GWAS/data_split/'


    # for p in np.linspace(0,0.9,10):
        ###加载数据
        # for epoch in range(10):
    evaluation = []
    for i in os.listdir(target_file):
        path = os.path.join(target_file,i)
        #加载数据
        train_x,train_y = toolbox.load_data(os.path.join(path,'final_train.out'))
        test_x,test_y = toolbox.load_data(os.path.join(path,'final_test.out'))
        valid_x,valid_y = toolbox.load_data(os.path.join(path,'final_valid.out'))

        # while 1:
        #     feature = feature_selection.random_select(p,train_x.shape[1])
        #     if len(feature[0]):
        #         break
        Optimiter = feature_selection.GWO(5,10,train_x.shape[1],0.5,train_x,train_y,valid_x,valid_y)
        # print(Optimiter.__dict__)
        feature = Optimiter.gwo()
        train_x = train_x[:,feature[0]]
        test_x = test_x[:,feature[0]]
        print(train_x.shape[1],test_x.shape[1])
        #训练
        one_clf = clf.classifier(GaussianNB)
        one_clf.fit(train_x,train_y)
        predict = one_clf.predict(test_x)
        print(predict)
        one_evaluation = one_clf.evaluate(test_y,predict)
        evaluation.append(one_evaluation)
        print('length of features:{},acc:{}'.format(len(feature[0]),one_evaluation))
    # print('p:{},epcoch:{},mean+-std'.format(p,epoch))
    print(np.mean(evaluation),np.std(evaluation))
    ##分类

if __name__ == '__main__':
    main()