#%%


import numpy as np
import matplotlib.pyplot as plt
from tfrbm import BBRBM,GBRBM
from tensorflow.examples.tutorials.mnist import input_data
from sklearn import preprocessing
import parameter
import os
import toolbox
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"       # 使用第二块GPU（从0开始）

def get_data(data,label,train_index,test_index):
    '''
    得到训练集和测试集
    :param data: 总的数据集合
    :param label: 标签，该标签为'AD','NC'...
    :param train_index: 训练集下标
    :param test_index: 测试集下标
    :return:
    '''
    train_x = data[train_index]
    test_x = data[test_index]
    train_y = label[train_index]
    test_y = label[test_index]
    return train_x,train_y,test_x,test_y

def main():

    args = parameter.set_args()

    for i in os.listdir(args.target):
        # 数据加载
        path = os.path.join(args.target,i)
        #加载数据
        train_x,train_y = toolbox.load_data(os.path.join(path,'final_train.out'))
        test_x,test_y = toolbox.load_data(os.path.join(path,'final_test.out'))
        valid_x,valid_y = toolbox.load_data(os.path.join(path,'final_valid.out'))
        data = np.vstack((train_x,test_x,valid_x))
        #debug
        bbrbm = BBRBM(n_visible=data.shape[1],n_hidden=64,learning_rate=0.01,momentum=0.95,use_tqdm=True)
        errs = bbrbm.fit(data,n_epoches=1000,batch_size=10)
        #保存文件
        print('model name:'+args.m_n+'_{}'.format(i))
        bbrbm.save_weights(args.m_weight+'_{}'.format(i),args.m_n+'_{}'.format(i))
        np.save(args.log+'_{}',errs.format(i))

if __name__ == '__main__':
    main()
#%%
# mnist = input_data.read_data_sets('/media/rong/big_data/conn_fmri/MNIST_data', one_hot=True)
# mnist_images = mnist.train.images
#
# bbrbm = BBRBM(n_visible=784, n_hidden=64, learning_rate=0.01, momentum=0.95, use_tqdm=True)
# errs = bbrbm.fit(mnist_images, n_epoches=30, batch_size=10)
# plt.plot(errs)
# plt.show()