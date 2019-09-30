import argparse
import pandas
import re
import os
import shutil
import pandas as pd
import numpy as np
def load_data(trainfilename):
    db = pd.read_csv(trainfilename,sep=' ')
    db = np.array(db)
    data = db[:,6:].astype(float)
    label = db[:,5].astype(int)
    print(data.shape,label.shape)
    return data,label

def set_args():
    parse = argparse.ArgumentParser()
    parse.description=''

    parse.add_argument('-f1',help='file1',default='')
    parse.add_argument('-f2',help='file2',default='')
    parse.add_argument('-f3',help='file3',default='')
    parse.add_argument('-o',help='output',default='')
    parse.add_argument('-t',help='type',default='')

    args = parse.parse_args()
    return args

def data_split(f1,f2,f3,f4,valid=None):
    # creat subject dict
    subject_dict = dict()
    db1 = pandas.read_excel(f1, header=None)
    db2 = pandas.read_excel(f2, header=None)

    print(db1.iloc[0])
    for i in range(db1.shape[0]):
        #print(db1.iloc[i,1],db1.iloc[i,0])
        subject_dict[db1.iloc[i,1]] = db1.iloc[i,0]
    for i in range(db2.shape[0]):
        subject_dict[db2.iloc[i,1]] = db2.iloc[i,0]

    # with open(f1,'r') as f:
    #     for line in f:
    #         words = line.split(' ')
    #         subject_dict[words[1]] = words[0]
            # print(words)
    test_id = []
    p = re.compile('\d+_S_\d+')
    with open(f3,'r') as f:
        for line in f:
            # print(p.findall(line))
            # print(p.findall(line)[0])
            if p.findall(line)[0] in subject_dict:
                test_id += ['{} {}\n'.format(subject_dict[p.findall(line)[0]],p.findall(line)[0])]
                subject_dict.pop(p.findall(line)[0])
            # print(subject_dict[p.findall(line)[0]])

    #valid
    valid_id = []
    with open(valid,'r') as f:
        for line in f:
            # print(p.findall(line))
            # print(p.findall(line)[0])
            if p.findall(line)[0] in subject_dict:
                valid_id += ['{} {}\n'.format(subject_dict[p.findall(line)[0]],p.findall(line)[0])]
                subject_dict.pop(p.findall(line)[0])
    valid_filename = os.path.join(f4,'valid.txt')
    with open(valid_filename,'w') as f:
        for i in valid_id:
            f.write(i)
    #############
    test_filename = os.path.join(f4,'test.txt')
    train_filename = os.path.join(f4,'train.txt')


    with open(test_filename,'w') as f:
        for i in test_id:
            f.write(i)

    with open(train_filename,'w') as f:
        for item in subject_dict.items():
            f.write('{} {}\n'.format(item[1],item[0]))

def get_subject_set(filename):
    '''
    获取subject集合
    :param filename:
    :return:
    '''
    s = set()
    db = pandas.read_excel(filename,header = None)
    for i in range(db.shape[0]):
        s.add(db.iloc[i,1])
    return s

def edit_character(input_file,f1=None,f2=None):
    '''
    修改性状
    :param input_file:
    :param f1:
    :param f2:
    :return:
    '''
    type_A = get_subject_set(f1)
    type_B = get_subject_set(f2)
    output = 'default.txt'
    with open(input_file, 'r') as fp1, open(output, 'w') as fp2:
        for line in fp1:
            line = line.strip().split(' ')
            if line[1] in type_A:
                line[-1] = '1'
            elif line[1] in type_B:
                line[-1] = '2'
            else:
                line[-1] = '-9'
            # line[-1] = int(line[1] in type_A)
            print(' '.join(line))
            fp2.write(' '.join(line)+'\n')
    shutil.move(output,input_file)


def main():
    for i in range(5):
        data_split('/media/rong/My Passport/GWAS/subject_list/MCIc.xlsx',
                   '/media/rong/My Passport/GWAS/subject_list/MCInc.xlsx',
                   '/media/rong/My Passport/GWAS/data_split/fold{}/fold{}_test.txt'.format(i,i),
                   '/media/rong/My Passport/GWAS/data_split/fold{}'.format(i),
                   '/media/rong/My Passport/GWAS/Origin/valid/valid.txt')
    # edit_character('/media/rong/My Passport/GWAS/data_split/fold0/Mydata.fam',
    #                '/media/rong/My Passport/GWAS/subject_list/MCIc.xlsx',
    #                '/media/rong/My Passport/GWAS/subject_list/MCInc.xlsx')
    # args = set_args()
    # print(args.f1,args.f2,args.f3)
    # edit_character(args.f1,args.f2,args.f3)

    # data_split('/media/rong/My Passport/GWAS/subject_list/MCIc.xlsx',
    #                '/media/rong/My Passport/GWAS/subject_list/MCInc.xlsx',
    #                '/media/rong/My Passport/GWAS/data_split/valid.txt',
    #                '/media/rong/My Passport/GWAS/data_split/')

if __name__ == '__main__':
    main()