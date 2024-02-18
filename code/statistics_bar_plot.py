import matplotlib.pyplot as plt
# https://blog.csdn.net/weixin_34613450/article/details/80678522 Python绘图问题：Matplotlib中指定图片大小和像素 width, height
plt.figure(figsize=(16,4))
all_keys=all_keys[:-1]
name_list=all_keys
all_keys_list=list(range(len(all_keys)))
large=1
x=all_keys_list
x=[i*large for i in x]
# x = list(range(len(num_list)))
total_width, n = 0.8*large, len(colum)-1
width = total_width / n

all_row_data=[]
for key in all_keys:
    row_data=[]
    for ind_idiom,dict_idiom in enumerate(result):
        total=sum(dict_idiom.values())

        if key in dict_idiom:
            row_data.append(dict_idiom[key]/total)
        else:
            row_data.append(0)
    all_row_data.append(row_data)
new_row_data=[[0 for j in range(len(all_keys))] for i in range(len(colum)-1)]
for ind_row,row in enumerate(all_row_data):
    for ind_col,col in enumerate(row):
        new_row_data[ind_col][ind_row]=all_row_data[ind_row][ind_col]

def transform_y(e_idiom_node):
    for ind,e in enumerate(e_idiom_node):
        if e<10e-6:
            e_idiom_node[ind]=e*10000
        elif e<10e-5:
            e_idiom_node[ind] =  e*1000+0.1
        elif e < 10e-4:
            e_idiom_node[ind] = e*100+0.2
        elif e < 10e-3:
            e_idiom_node[ind] = e*10+0.3
        elif e < 10e-2:
            e_idiom_node[ind] = e*1+0.4
        else:
            e_idiom_node[ind] = e+0.4
    return e_idiom_node

color_list=['C'+str(i) for i in range(len(colum)-1)]
# ['C0','C1','C2','C3','C4','C5','C6','C8','C9']
for ind_idiom,e_idiom_node in enumerate(new_row_data):
    e_idiom_node=transform_y(e_idiom_node)
    if ind_idiom==1:
        plt.bar(x, e_idiom_node, width=width,tick_label=all_keys, fc=color_list[ind_idiom],label=colum[ind_idiom+1])
        # break
    else:
        plt.bar(x, e_idiom_node, width=width,   fc=color_list[ind_idiom],label=colum[ind_idiom+1])
    # tick_label=all_keys_name_list, label='list_compre',
    x = [x[i] + width for i in range(len(x))]

    print("ind_idiom: ",ind_idiom,color_list[ind_idiom],e_idiom_node)
#
# plt.tight_layout()
plt.axhline(y=0.5, color='C7', lw=1, linestyle="--")
# https://blog.csdn.net/corleone_4ever/article/details/111314048 matplotlib去掉图例边框
# https://blog.csdn.net/weixin_38314865/article/details/115182900 matplotlib设置多个图例横向水平放置
plt.legend(ncol=9,loc=9,bbox_to_anchor=(0.5,1.15),frameon=False)
plt.xlim(-0.4, 33.1)# 使用该指令可调整坐标轴最左/最右刻度到两边的距离 https://www.cnblogs.com/xiao-qingjiang/p/15934443.html
plt.xticks(rotation=35)
plt.yticks([i*0.1 for i in range(15)],['0', '0.00001', '0.0001', '0.001', '0.01'] + ['0.'+str(i) for i in range(1,10)]+['1.0'])
plt.subplots_adjust(left=0.05,bottom=0.23)
# https://blog.csdn.net/AI_ShortLegCork/article/details/121392685
plt.show()