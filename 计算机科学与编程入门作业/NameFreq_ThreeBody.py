import jieba
import jieba.posseg as pseg

txt_file_name = './data/三体.txt'
node_file_name = './data/三体-人物节点.csv'
link_file_name = './data/三体-人物连接.csv'

txt_file = open(txt_file_name, 'r', encoding = 'utf-8')
line_list = txt_file.readlines()
line_len = len(line_list)
txt_file.close()
jieba.load_userdict('./data/userdict.txt')
ignore_list = ['文明', '阳光', '明白', '苏醒', '望远镜', '卫星', '谢谢',
               '孤峰', '哈勃', '赫尔辛', '王宫', '蓝星', '金字塔', '智慧', 
               '海王星', '空旷', '雷达', '雪山', '红光', '红卫兵']

line_name_list = []
name_cnt_dict = {}
process = 0
for line in line_list :
    words_list = pseg.cut(line)
    line_name_list.append([])
    for word in words_list :
        name = word.word
        flag = word.flag
        if flag == 'nr':
            if len(name) == 1 or name in ignore_list:
                continue
            if name == '小罗' or name == '罗兄' or name == '罗老弟':
                name = '罗辑'
            elif name == '颜颜' :
                name = '庄颜'
            elif name == '丁老' :
                name = '丁仪'
            elif name == '大史' :
                name = '史强'
            elif name == '元首' :
                name = '三体元首'
            elif name == 'AA' :
                name = '艾AA'
            elif name == '玉菲' :
                name = '申玉菲'
            elif name == '惠子' :
                name = '山杉惠子'
            elif name == '文洁' :
                name = '叶文洁'
            
            line_name_list[-1].append(name)
            if name in name_cnt_dict :
                name_cnt_dict[name] += 1
            else :
                name_cnt_dict[name] = 1
    process += 1
    if process % 1000 == 0 :
        print(f'已完成{process} / {line_len}')

name_cnt_limit = 30
link_cnt_limit = 5

relation_dict = {}
for line_name in line_name_list :
    for name_source in line_name :
        if name_cnt_dict[name_source] < name_cnt_limit :
            continue
        if name_source not in relation_dict.keys() :
            relation_dict[name_source] = {}
        for name_target in line_name :
            if name_source != name_target and name_cnt_dict[name_target] >= name_cnt_limit :
                if name_target in relation_dict[name_source].keys() :
                    relation_dict[name_source][name_target] += 1
                else :
                    relation_dict[name_source][name_target] = 1
                    
figure_list = list(name_cnt_dict.items())
figure_list.sort(key = lambda x : x[1], reverse = True)

node_file = open(node_file_name, 'w') 
node_file.write('Name,Weight\n')
for name, cnt in figure_list: 
    if cnt < name_cnt_limit :
        continue
    if name not in relation_dict.keys() :
        continue
    flag = 0
    for item in relation_dict[name].items() :
        if item[1] >= link_cnt_limit :
            flag = 1
            break
    if flag == 0 :
        continue
    node_file.write(name + ',' + str(cnt) + '\n')
node_file.close()


link_file = open(link_file_name, 'w')
link_file.write('Source,Target,Weight\n')
for name_source, link_dict in relation_dict.items():
    for name_target, link in link_dict.items():
        if link >= link_cnt_limit:
            link_file.write(name_source + ',' + name_target + ',' + str(link) + '\n')
link_file.close()