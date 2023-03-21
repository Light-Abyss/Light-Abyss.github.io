from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Graph, Timeline
from math import log, sqrt

name = ['', '', '', '']
name[0] = '三体'
name[1] = '三体1地球往事'
name[2] = '三体2黑暗森林'
name[3] = '三体3死神永生'

node_file_name = ['', '', '', '']
for i in range(0, 4) :
    node_file_name[i] = './data/' + name[i] + '-人物节点.csv'
link_file_name = ['', '', '', '']
for i in range(0, 4) :
    link_file_name[i] = './data/' + name[i] + '-人物连接.csv'
out_file_name = './output/三体人物关系图.html'

node_line_list = [[], [], [], []]
for i in range(0, 4) :
    node_file = open(node_file_name[i], 'r')
    node_line_list[i] = node_file.readlines()
    node_file.close()
    del node_line_list[i][0]  # 删除标题行
link_line_list = [[], [], [], []]
for i in range(0, 4) :
    link_file = open(link_file_name[i], 'r')
    link_line_list[i] = link_file.readlines()
    link_file.close()
    del link_line_list[i][0]  # 删除标题行

node_in_graph = [[], [], [], []]
for i in range(0, 4) :
    for one_line in node_line_list[i]:
        one_line = one_line.strip('\n')
        one_line_list = one_line.split(',')
        node_in_graph[i].append(
            opts.GraphNode(
                name = one_line_list[0], 
                value = int(one_line_list[1]), 
                symbol_size = sqrt(int(one_line_list[1])) * 3,
                
            )
        )
link_in_graph = [[], [], [], []]
for i in range(0, 4) :
    for one_line in link_line_list[i]:
        one_line = one_line.strip('\n')
        one_line_list = one_line.split(',')
        link_in_graph[i].append(
            opts.GraphLink(
                source = one_line_list[0], 
                target = one_line_list[1], 
                value = int(one_line_list[2])
            )
        )
color = ['', '', '', '']
color[0] = '#00BFFF'
color[1] = '#9370DB'
color[2] = '#00FF7F'
color[3] = '#FFB6C1'

graph = []
for i in range(0, 4) :
    graph.append(Graph())
    graph[i].add(
        '',
        node_in_graph[i], 
        link_in_graph[i], 
        edge_length = [20,50], 
        repulsion = 5000,
        layout = "force",
        itemstyle_opts = opts.ItemStyleOpts(
            color = color[i],
            opacity = 0.9,    #节点透明度
        )
    )
    graph[i].set_global_opts(title_opts = opts.TitleOpts(title = name[i]+' 人物关系'))

timeline = Timeline(
    opts.InitOpts(
        page_title = '三体人物关系图',
        width = "100%", 
        height = "640px", 
    )
)
for i in range(0, 4) :
    timeline.add(graph[i], name[i])
    
timeline.render(out_file_name)