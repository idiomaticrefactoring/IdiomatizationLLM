import util,os
'''
#"/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/Book4 copy.csv"
file_new_idiom="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/new_idioms.csv"
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
save_file_name="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/Book4_rewrite.csv"
save_file_name="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/new_idioms_rewrite.csv"
util.save_csv(save_file_name,list_1)
'''
def transform(e):
    if float(e) > 80:
        return (float(e)-80)*2+70
    return float(e)
save_file_name="/Users/zhangzejunzhangzejun/PycharmProjects/chatgptData/picture/Book4_rewrite.csv"
list_1=util.load_csv(save_file_name)
result=[]
acc=[[],[],[]]
for e in list_1[2:-1]:
    # new_e=transform(e)
    acc[0].append(transform(e[3]))
    acc[1].append(transform(e[7]))
    acc[2].append(transform(e[11]))
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
x=list(range(9))
x=[i*1.5 for i in range(9)]
plt.figure(figsize=(8,4))
plt.plot(x,acc[0],'ro-',label="Ours")
plt.plot(x,acc[1],'g^-',label="RIdiom")
plt.plot(x,acc[2],'bs-',label="Prompt-LLM")
# plt.yticks([i*0.1 for i in range(15)],['0', '0.00001', '0.0001', '0.001', '0.01'] + ['0.'+str(i) for i in range(1,10)]+['1.0'])
# plt.yticks([i*10 for i in range(11)])
# plt.yticks([0,10,20,30,50,80,85,90,95,100])
# plt.yticks([0,10,20,30,50,60,80,85,90,95,100])
# plt.yticks([0,10,20,30,50,60,80,90,100,110,120],[0,10,20,30,50,60,80,85,90,95,100])

# plt.yticks([0,10,20,30,50,80,85,90,95,100])
# plt.yticks([0,10,20,30,50,60,80,85,90,95,100])
# plt.yticks([0,10,20,30,50,60,70,80,90,100,110])
# plt.yticks([0,10,20,30,50,60,80,90,100,110,120],[0,10,20,30,50,60,80,85,90,95,100])
plt.yticks([0,10,20,30,40,50,60,70,80,90,100,110],[0,10,20,30,40,50,60,80,85,90,95,100])
# list comprehension
# Set comprehension
# Dict comprehension
# chain comparison
# truth test
# Loop else
# Assign multi targets
# for multi targets
# call star
plt.xticks(x,['list-compre','set-compre','dict-compre','chain-compare','truth-test','loop-else','ass-mul-tar','for-mul-tar','star-call'],rotation=15)#,rotation=20

# 80,90,100,110,120
# 80,85,90,95,100
# plt.bar(acc)
# plt.plot(x,acc[0],'b--',label="Prompt-LLM")
plt.legend()
plt.ylabel('Accuracy (%)')
# plt.xlabel('Idiom')

plt.subplots_adjust(left=0.08,bottom=0.15,hspace=0.001)#,top=0.9

plt.show()


