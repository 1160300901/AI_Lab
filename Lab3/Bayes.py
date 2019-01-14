#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : Bayes.py
@Time : 2018/11/2 22:17
@Site : 
@Software: PyCharm
'''

'''
Function ParserQueries: 解析问题查询文件
'''


def ParserQueries(queriesFile):
    f_query = open(queriesFile, "r")
    querieslist = []
    for line in f_query.readlines():
        if line.strip() == '':
            continue
        line = line.strip().replace(' ', '')
        line = line.replace('P(', '')
        line = line.replace(')', '')
        list = line.split('|')
        query = []
        query.append(tuple([list[0]]))
        temp = list[1].split(',')
        for i in range(len(temp)):
            query.append(tuple(temp[i].split('=')))
        querieslist.append(query)
    f_query.close()
    return querieslist


'''
Function ParserNetwork: 解析贝叶斯网络文件
'''


def ParserNetwork(networkFile):
    with open(networkFile, 'r') as f_net:
        lines = f_net.readlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].rstrip('\n')
    while '' in lines:
        lines.remove('')
    # 解析第一行N个顶点
    N = int(lines[0])
    # 解析第二行顶点的名字
    names = lines[1].split(' ')
    Network = {}
    for i in range(0, N):
        Network[names[i]] = []
    # 解析有向图的01表,存到二维数组中
    parentTable = [[0] * N for i in range(N)]
    for i in range(2, N + 2):
        line = lines[i].split(' ')
        # print line
        for j in range(0, N):
            parentTable[i - 2][j] = int(line[j])
    # print parentTable
    column = 0
    temp = [0] * N
    sum = 0
    row = N + 2
    # 读每个节点的CPT表
    for i in range(0, N):
        # 遍历每一列,如果所在列的和为0说明其没有父节点
        for k in range(0, N):
            temp[k] = parentTable[k][column]
            sum += temp[k]
            # print sums
        column += 1
        if sum == 0:
            CPT = []
            CPT.append((None,))
            CPT.append(tuple(lines[row].split(' ')))
            row += 1
            Network[names[i]] = CPT
            # print Network
        else:
            CPT = []
            parents = []
            for col in range(0, N):
                if parentTable[col][i] == 1:
                    parents.append(names[col])
            CPT.append(tuple(parents))
            for k in range(row, row + pow(2, sum)):
                CPT.append(tuple(lines[k].split(' ')))
                row += 1
            Network[names[i]] = CPT
            # print Network
        sum = 0
    return Network, names


'''
Function JointDistribution: 求出所有的联合概率分布
'''


def JointDistribution(TFsequence, network, names):
    length = len(names)
    sums = 1
    for i in range(0, length):
        value = TFsequence[i]
        parents = network[names[i]]
        # 如果没有父节点
        if cmp((None,), parents[0]) == 0:
            if value == '0':
                # F时的概率
                sums *= float(parents[1][1])
            else:
                # T时的概率
                sums *= float(parents[1][0])
        # 有父节点
        else:
            number_of_father = len(parents[0])  # 父节点个数
            chooseposition = 0
            for j in range(0, number_of_father):  # 遍历父节点
                pat = parents[0][j]
                value2 = TFsequence[names.index(pat)]  # 查看父节点是真还是假
                if value2 == '0':
                    continue
                else:
                    chooseposition += pow(2, number_of_father - j - 1)
            if value == '0':
                sums *= float(parents[chooseposition + 1][1])  # 当前节点为F
            else:
                sums *= float(parents[chooseposition + 1][0])  # 当前节点为T
    return str(sums)


'''
Function calculate: 贝叶斯网络的推理,求解查询问题的概率
'''


def calculate(Network, names, querieslist):
    N = len(names)
    jointPro = [[0 for i in range(2)] for j in range(0, pow(2, N))]
    # 生成联合概率序列,0表示F,1表示T
    for i in range(0, pow(2, N)):
        jointPro[i][0] = bin(i).replace('0b', '').zfill(N)
        temp = jointPro[i][0]
        # 计算联合概率
        jointPro[i][1] = JointDistribution(temp.zfill(N), Network, names)
    # 将问题的条件节点真假值映射为1和0,如果是条件节点且为真则为1,为假则为0,否则为2
    check = [2 for i in range(0, N)]

    for i in range(0, len(querieslist)):
        query = querieslist[i]
        # print query
        # 问询节点
        query_node = ''.join(list(query[0][0]))
        # print query_node
        positions = names.index(query_node)
        for j in range(1, len(query)):
            condition = query[j]
            # 条件节点
            condition_node = ''.join(list(condition[0]))
            position = names.index(condition_node)
            if cmp(condition[1], 'true') == 0:
                check[position] = 1
            else:
                check[position] = 0
        check = [str(x) for x in check]
        # 条件节点012序列
        seq = ''.join(check)
        check = [2 for i in range(0, N)]
        denominator = 0  # 分母
        numerator = 0  # 分子
        flag = 0
        listresult = []
        # 计算分母
        for k in range(0, pow(2, N)):
            for j in range(0, N):
                if cmp(seq[j], '2') != 0 and cmp(seq[j], jointPro[k][0][j]) != 0:
                    flag = 1
            if flag == 0:
                denominator += float(jointPro[k][1])
                listresult.append(jointPro[k])
            flag = 0
        # 计算分子
        for j in range(0, len(listresult)):
            if cmp(listresult[j][0][positions], '1') == 0:
                numerator += float(listresult[j][1])
        print [numerator / denominator, 1 - numerator / denominator]


def main():
    querieslist = ParserQueries("burglarqueries.txt")
    print querieslist
    Network, names = ParserNetwork("burglarnetwork.txt")
    print Network
    # print names
    calculate(Network, names, querieslist)


if __name__ == '__main__':
    main()
