import util,os
'''
#"/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/Book4 copy.csv"
file_new_idiom="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/new_idioms.csv"
file_new_idiom="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/Book4_rewrite.csv"

list_1=util.load_csv(file_new_idiom)
for ind,e in enumerate(list_1):
    for j,e2 in enumerate(e):
        if "%" in e2:
            if "41" in e2:

                print(e2,e2[:-1],str(e2[:-1]))
            list_1[ind][j]=str(e2[:-1])
        if "100" in e2:
            list_1[ind][j] = "100"
print(list_1)
save_file_name="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/Book4_rewrite_new.csv"
# save_file_name="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/new_idioms_rewrite.csv"
util.save_csv(save_file_name,list_1)
'''
def transform(e):
    if float(e) > 90:
        # return (float(e)-80)*2+70
        return (float(e) - 90) * 2 + 60
    return float(e)

def transform_old(e):
    if float(e) > 70:
        return (float(e)-70)/2+80
    return float(e)
def text_fig(ax1,acc,acc_old):
    for ind, e_acc in enumerate(acc):
        # print(">>>", e_acc)

        for ind_idiom, (w, y) in enumerate(zip(x, e_acc)):
            if ind == 0:
                y = y + 1.5
            if ind == 1:
                y = y - 6
            if ind == 2:
                y = y + 3
            ax1.text(w, y, str(round(float(acc_old[ind][ind_idiom]), 1)))

save_file_name="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/new_idioms_rewrite.csv"
list_1=util.load_csv(save_file_name)
result=[]
acc=[[],[]]
acc_old=[[],[]]
for e in list_1[2:-1]:
    # new_e=transform(e)
    acc[0].append(transform(e[3]))
    acc[1].append(transform(e[7]))
    # acc[2].append(transform(e[11]))
    acc_old[0].append(e[3])
    acc_old[1].append(e[7])
    # acc_old[2].append(e[11])
f1 = [[], []]
f1_old=[[],[]]
for e in list_1[2:-1]:
    # new_e=transform(e)
    f1[0].append(transform(e[4]))
    f1[1].append(transform(e[8]))
    # f1[2].append(transform(e[12]))
    f1_old[0].append(e[4])
    f1_old[1].append(e[8])
    # f1_old[2].append(e[12])

precison = [[], []]
precison_old=[[],[]]
for e in list_1[2:-1]:
    # new_e=transform(e)
    precison[0].append(transform(e[5]))
    precison[1].append(transform(e[9]))
    # precison[2].append(transform(e[13]))
    precison_old[0].append(e[5])
    precison_old[1].append(e[9])
    # precison_old[2].append(e[13])
recall = [[], []]
recall_old=[[],[]]
for e in list_1[2:-1]:
    # new_e=transform(e)

    recall[0].append(transform(e[6]))
    if transform(e[10])>50:
        recall[1].append(51)
    else:
        recall[1].append(transform(e[10]))
    # recall[2].append(transform(e[14]))
    recall_old[0].append(e[6])
    recall_old[1].append(e[10])
    # recall_old[2].append(e[14])
    # if float(e[3])>80:
    #     acc[0].append((float(e[3])-80)*2+80)
    #     acc[1].append((float(e[7])-80)*2+80)
    #     acc[2].append((float(e[11])-80)*2+80)
    # else:
    #         acc[0].append(float(e[3]))
    #         acc[1].append(float(e[7]))
    #         acc[2].append(float(e[11]))
print(list_1[2][3:])
print(list_1[2][3:][::4])
print(acc)
import matplotlib.pyplot as plt
# x=list(range(9))
x=[i*1.5 for i in range(4)]
idiom_list=['with','enumerate','chain-assign','fstring']
# plt.figure(figsize=(8,4))
fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 8))#, sharey=True
ax1.plot(x,acc[0],'ro-',label="Ours")
y_ticks_1,y_ticks_label=[0,10,20,30,40,50,60,70,80,95],[0,10,20,30,40,50,90,95,100,'']
# ax1.plot(x,acc[1],'g^-',label="RIdiom")
ax1.plot(x,acc[1],'bs-',label="Prompt-LLM")
ax1.axhline(y=10, color='C7', lw=1, linestyle="--")
# ax1.axhline(y=30, color='C7', lw=1, linestyle="--")
ax1.axhline(y=50, color='C7', lw=1, linestyle="--")
ax1.axhline(y=60, color='C7', lw=1, linestyle="--")
ax1.axhline(y=70, color='C7', lw=1, linestyle="--")
ax1.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax1.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax1.axhline(y=90, color='C7', lw=1, linestyle="--")
# ax1.axhline(y=100, color='C7', lw=1, linestyle="--")
# ax1.axhline(y=110, color='C7', lw=1, linestyle="--")
# ax1.axhline(y=120, color='C7', lw=1, linestyle="--")

text_fig(ax1,acc,acc_old)
ax1.set_yticks(y_ticks_1,y_ticks_label)

# ax1.set_yticks([0,10,20,30,40,50,60,70,80,90,100,110],[0,10,20,30,40,50,60,80,85,90,95,100])
ax1.set_xticks(x,idiom_list,rotation=15)#,rotation=20
ax1.set_ylabel('Accuracy (%)')
ax1.set_title('a) accuracy comparison')
ax1.legend()



ax2.plot(x,f1[0],'ro-',label="Ours")
# ax2.plot(x,f1[1],'g^-',label="RIdiom")
ax2.plot(x,f1[1],'bs-',label="Prompt-LLM")
ax2.axhline(y=10, color='C7', lw=1, linestyle="--")
# ax2.axhline(y=30, color='C7', lw=1, linestyle="--")
ax2.axhline(y=50, color='C7', lw=1, linestyle="--")
ax2.axhline(y=60, color='C7', lw=1, linestyle="--")
ax2.axhline(y=70, color='C7', lw=1, linestyle="--")
ax2.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax2.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax2.axhline(y=90, color='C7', lw=1, linestyle="--")
# ax2.axhline(y=100, color='C7', lw=1, linestyle="--")
# ax2.axhline(y=110, color='C7', lw=1, linestyle="--")
# ax2.axhline(y=120, color='C7', lw=1, linestyle="--")

text_fig(ax2,f1,f1_old)
ax2.set_yticks(y_ticks_1,y_ticks_label)

# ax2.set_yticks([0,10,20,30,40,50,60,70,80,90,100,110],[0,10,20,30,40,50,60,80,85,90,95,100])
ax2.set_xticks(x,idiom_list,rotation=15)#,rotation=20
ax2.set_ylabel('F1-Score (%)')
ax2.set_title('b) F1 comparison')
ax2.legend()


ax3.plot(x,precison[0],'ro-',label="Ours")
# ax3.plot(x,precison[1],'g^-',label="RIdiom")
ax3.plot(x,precison[1],'bs-',label="Prompt-LLM")
# text_fig(ax3,precison,precison_old)
for ind, e_acc in enumerate(precison):
    # print(">>>", e_acc)

    for ind_idiom, (w, y) in enumerate(zip(x, e_acc)):
        if ind == 1:
            if ind_idiom==4:
                y = y - 5
            else:
                if ind_idiom in [0,1,2,6]:
                    y = y + 1
                else:
                    y = y + 3

        if ind == 0:
            if ind_idiom == 4:
                y = y + 1.5
                pass
            else:
                y = y - 5
        if ind == 2:
            y = y + 3
        ax3.text(w, y, str(round(float(precison_old[ind][ind_idiom]), 1)))

ax3.axhline(y=10, color='C7', lw=1, linestyle="--")
# ax3.axhline(y=30, color='C7', lw=1, linestyle="--")
ax3.axhline(y=50, color='C7', lw=1, linestyle="--")
ax3.axhline(y=60, color='C7', lw=1, linestyle="--")
ax3.axhline(y=70, color='C7', lw=1, linestyle="--")
ax3.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax3.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax3.axhline(y=90, color='C7', lw=1, linestyle="--")
# ax3.axhline(y=100, color='C7', lw=1, linestyle="--")
# ax3.axhline(y=110, color='C7', lw=1, linestyle="--")
# ax3.axhline(y=120, color='C7', lw=1, linestyle="--")
ax3.set_yticks(y_ticks_1,y_ticks_label)

# ax3.set_yticks([0,10,20,30,40,50,60,70,80,90,100,110],[0,10,20,30,40,50,60,80,85,90,95,100])
ax3.set_xticks(x,idiom_list,rotation=15)#,rotation=20
ax3.set_ylabel('Precision (%)')
ax3.set_title('c) precision comparison')
ax3.legend()

ax4.plot(x,recall[0],'ro-',label="Ours")
# ax4.plot(x,recall[1],'g^-',label="RIdiom")
ax4.plot(x,recall[1],'bs-',label="Prompt-LLM")
text_fig(ax4,recall,recall_old)
ax4.axhline(y=10, color='C7', lw=1, linestyle="--")
# ax4.axhline(y=30, color='C7', lw=1, linestyle="--")
ax4.axhline(y=50, color='C7', lw=1, linestyle="--")
ax4.axhline(y=60, color='C7', lw=1, linestyle="--")
ax4.axhline(y=70, color='C7', lw=1, linestyle="--")
ax4.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax4.axhline(y=80, color='C7', lw=1, linestyle="--")
# ax4.axhline(y=90, color='C7', lw=1, linestyle="--")
# ax4.axhline(y=100, color='C7', lw=1, linestyle="--")
# ax4.axhline(y=110, color='C7', lw=1, linestyle="--")
# ax4.axhline(y=120, color='C7', lw=1, linestyle="--")
ax4.set_yticks(y_ticks_1,y_ticks_label)

# ax4.set_yticks([0,10,20,30,40,50,60,70,80,90,100,110],[0,10,20,30,40,50,60,80,85,90,95,100])
ax4.set_xticks(x,idiom_list,rotation=15)#,rotation=20
ax4.set_ylabel('Recall (%)')
ax4.set_title('d) recall comparison')
ax4.legend()



# ax1.ylabel('Accuracy (%)')

# ax1.set_yticklabels('Accuracy (%)')
# plt.xlabel('Idiom')

# plt.subplots_adjust(left=0.08,bottom=0.15)#,top=0.9
# plt.subplots_adjust(left=0.04,bottom=0.07)#,top=0.9
# plt.subplots_adjust(bottom=0.07)#,top=0.9
plt.subplots_adjust(top = 0.93,right = 0.98, bottom = 0.07, left = 0.04,hspace=0.4,wspace=0.15)
# plt.margins(0,0)
# plt.show()
dir_file_name="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/"

plt.savefig(dir_file_name+"effectiveness_compare_rq2.pdf", format="pdf", bbox_inches="tight")


