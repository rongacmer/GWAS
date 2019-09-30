import argparse

def set_args():
    parse = argparse.ArgumentParser()
    parse.description=''
    log_predix = 'gwas_rmb_9_30'
    parse.add_argument('-f1',help='file1',default='')
    parse.add_argument('-f2',help='file2',default='')
    parse.add_argument('-f3',help='file3',default='')
    parse.add_argument('-o',help='output',default='')
    parse.add_argument('-t',help='type',default='')

    parse.add_argument('-target',help='target_file',default='/media/rong/My Passport/GWAS/data_split')

    # 输出文件参数
    parse.add_argument('-m_weight', help='model weight', default='/media/rong/My Passport/GWAS/model/' + log_predix)
    parse.add_argument('-log', help='logging', default='/media/rong/My Passport/GWAS/log/' + log_predix)
    args = parse.parse_args()
    return args

