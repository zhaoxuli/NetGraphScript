# -*- coding: utf-8 -*-
import os
import  pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def data_process(file_name,out_file):
    name_lst = []
    quant_num_lst = []
    #提取节点信息 按照规则筛选 名字及量化文章数量
    ctx = open(file_name).readlines()
    for ele in ctx:
        ele = ele[:-1]
        [firstPub,hasQuant,lastPub,numArticle,quantNums,name] = ele.split(',')
        if ((hasQuant=='TRUE')and(int(numArticle)>5)and
            (int(lastPub)>2010)and(int(lastPub)-int(firstPub)>5)):
            name_lst.append(name)
            quant_num_lst.append(int(quantNums))
    #生成网络结构信息缓存文件
    all_nums = len(name_lst)
    net_info = []
    out_ctx = ''
    for i in range(all_nums-1):
        for j in range(i+1,all_nums):
            quant_num_res = quant_num_lst[i] - quant_num_lst[j]
            info = name_lst[i]+','+name_lst[j]+','+ str(quant_num_res) +'\n'
            net_info.append(info)
    target = open(out_file,'w')
    for ele in  net_info:
        target.write(ele)
    target.close

def  draw_netGraph(net_info_file):
    # 显示中文,及字体设置
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.unicode_minus'] = False
    # 读取文件
    df = pd.read_csv(net_info_file, header=None, names=['First', 'Second', 'quantRes'], encoding='gbk')
    # 计算段落人物关系权重
    df['weight'] = df.quantRes
    plt.figure(figsize=(12, 12))
    # 生成社交网络图
    G = nx.Graph()
    # 添加边
    for idx in df.index:
        G.add_edge(df.First[idx], df.Second[idx], weight=df.weight[idx])
    # 量化文章差大于8 认为 水平差距很大  量化文章差小于8 认为水平接近
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if (abs(d['weight']) >= 8)]
    emidle = [(u, v) for (u, v, d) in G.edges(data=True) if (abs(d['weight']) < 8)]
    #esmall = [(u, v) for (u, v, d) in G.edges(data=True) if (d['weight'] < 0)]
    # 图的布局
    # 节点在一个圆环上均匀分布
    pos = nx.circular_layout(G)
    # 点
    nx.draw_networkx_nodes(G, pos, alpha=0.6, node_size=350)
    # 边
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2, alpha=0.6, edge_color='r')
    nx.draw_networkx_edges(G, pos, edgelist=emidle, width=1, alpha=0.3, edge_color='b', style='dashed')
    # 标签
    nx.draw_networkx_labels(G, pos, font_size=10)
    # 生成结果
    plt.axis('off')
    plt.title('QuantCompare')
    plt.show()

if __name__ =="__main__":
    file_name = './Source_data.csv'
    out_file = 'after_process.csv'
    if os.path.exists(out_file) == False:
        data_process(file_name,out_file)
    draw_netGraph(out_file)


