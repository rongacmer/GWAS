import numpy as np
from numpy import random
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score
def random_select(prop,length):
    feature_prop = random.rand(length)
    return np.where(feature_prop > prop)

class GWO():
    def __init__(self,Agents,T,dim,threshold,data,label,test_data = None,test_label = None,classfier = GaussianNB,w = 0.01):
        self._Agents = Agents  #种群数量
        self._T = T #迭代次数
        self._dim = dim #维度
        self._threshold = threshold #阀值
        self._clasfier = classfier() #fitness分类器
        self._w = w
        # self.train_X,self.test_X,self.train_y,self.test_y = train_test_split(data,label,test_size=0.3,stratify=label) #数据分层
        self.train_X = data
        self.test_X = test_data
        self.train_y = label
        self.test_y = test_label
        self.first_wolf = 0
        self.second_wolf = 1
        self.third_wolf = 2

        self.initpop()


    def initpop(self):
        self.pop = random.rand(self._Agents,self._dim)
        self.pop = (self.pop > self._threshold).astype(float)

    def fitness(self,wolf):
        if np.sum(wolf) == 0:
            return 0,1000
        new_train_x = self.train_X[:,np.where(wolf==1)[0]]
        new_test_X = self.test_X[:,np.where(wolf==1)[0]]
        self._clasfier.fit(new_train_x,self.train_y)
        predict  = self._clasfier.predict(new_test_X)
        acc = accuracy_score(self.test_y,predict)
        F = (1-self._w)*(1-acc)  + self._w * new_train_x.shape[1] /(self._dim-1)
        # F = 1/new_train_x.shape[1]
        return acc,F

    def select_wolf(self):
        fitness_sort = []
        for i,j in enumerate(self.pop):
            fitness_sort.append((i,self.fitness(j)[1]))
        fitness_sort.sort(key=lambda x:x[1])
        self.first_wolf = self.pop[fitness_sort[0][0]]
        self.second_wolf = self.pop[fitness_sort[1][0]]
        self.third_wolf = self.pop[fitness_sort[2][0]]



    def gwo(self):
        for epoch in range(self._T):
            self.select_wolf()
            print('epoch:{}'.format(epoch))
            print(self.fitness(self.first_wolf), self.fitness(self.second_wolf), self.fitness(self.third_wolf))
            print(np.sum(self.first_wolf),np.sum(self.second_wolf),np.sum(self.third_wolf))
            if self.fitness(self.first_wolf)[0] == 0:
                print(self.pop)
            b = 2 - 2*(epoch/self._T)
            for i,wolf in enumerate(self.pop):
                A1 = 2*b*random.rand(self._dim)-b
                C1 = 2 * random.rand(self._dim)
                D1 = C1*self.first_wolf-wolf
                X1 = self.first_wolf - A1*D1

                A2 = 2 * b * random.rand(self._dim) - b
                C2 = 2 * random.rand(self._dim)
                D2 = C2 * self.first_wolf - wolf
                X2 = self.second_wolf - A2 * D2

                A3 = 2 * b * random.rand(self._dim) - b
                C3 = 2 * random.rand(self._dim)
                D3 = C3 * self.first_wolf - wolf
                X3 = self.third_wolf - A3 * D3

                X = (X1 + X2 + X3) / 3

                X = 1 / (1+np.e**(-X))
                self.pop[i] = (X > self._threshold).astype(float)
        return np.where(self.first_wolf > self._threshold)











