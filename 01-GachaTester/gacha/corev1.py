import random
'''SSR=["去无生"]
SR=["司方觉","晏行舟","宿砚","祁阳细辛","苏易盏","明承影","聂赤措姆","景陵","木阿羌","九羲","阿晦","柳翊","萧谓之","辛夷","墨十二","鼓"]
R=["青竹","长空明","时沧","方不凡","上官凌","江元异","朱砂","孟青岚","姬清越","薛珈","张亦","萧予之","墨影","屈九思","屈兰旌","夏承"]
#设置卡池内容
levels=[SSR,SR,R]
weight=[0.01,0.09,0.9]
#设置等级和各自对应权重'''
with open("characters.txt",'r',encoding="utf-8") as c:
    c1=c.readlines()
#读取文件
ssr=c1[0].rstrip('\n').split(",")
SSR=[]
for n in ssr:
    n=n.strip('"')
    SSR.append(n)
sr=c1[1].rstrip('\n').split(",")
SR=[]
for n in sr:
    n=n.strip('"')
    SR.append(n)
r=c1[2].rstrip('\n').split(",")
R=[]
for n in r:
    n=n.strip('"')
    R.append(n)
levels=[SSR,SR,R]
wei=c1[3].rstrip('\n').split(",")
weight=[]
for w in wei:
    w=float(w)
    weight.append(w)
#只做切片的话得到的结果还是str，所以需要转为float
#文件按行读取各类等级包含角色和等级对应权重，各行转为列表
result=[]
#结果记录器
num=int(input("输入抽取次数:"))
#直接使用input会输入str类型，用int()控制num变量类型
level=random.choices(levels,weights=weight,k=num)
#连续抽取num次
#print(level)
r=open('results.txt','a',encoding="utf-8")
#打开结果记录文件
for l in level:
    res=random.choice(l)
    result.append(res)
    #从对应等级中随机抽选一个角色作为结果，记录进列表中
    r.write(res+" ")
    #将该次结果写入结果记录文件
print(result)
r.close()
#关闭文件，数据写入