import json
import random
from datetime import datetime
from pathlib import Path

gacha_dir=Path(__file__).resolve().parent
#以本文件所在目录为基准，从项目根目录执行 python gacha/corev1.py 也能正确定位卡池与结果文件
with open(gacha_dir/"characters.json",'r',encoding="utf-8") as c:
    pool=json.load(c)
#从json读取卡池：档位以编号标识，概率按编号顺序对应
tier_ids=sorted(pool["tiers"].keys(),key=int)
#按档位编号排序，档位数量可变时仍能按序对齐概率
levels=[]
for tid in tier_ids:
    levels.append(pool["tiers"][tid])
base_weight=list(pool["probabilities"])
weight=list(base_weight)
#levels与weight按下标一一对应
#base_weight为配置中的原始概率，weight为当前生效概率
tier1=set(pool["tiers"][str(tier_ids[0])])
tier2=set(pool["tiers"][str(tier_ids[1])])
#1档、2档角色集合，用于识别保底与历史记录
results_path=gacha_dir/"results.txt"
history=[]
if results_path.exists():
    with open(results_path,'r',encoding="utf-8") as hist:
        for line in hist:
            line=line.strip()
            if not line:
                continue
            if "character:" in line:
                name=line.split("character:")[-1].strip().rstrip("]").strip()
                history.append(name)
            else:
                history.extend(line.split())
#抽卡前读取已有记录；空文件或不存在则视为无历史
#新日志按行解析角色名，旧空格分隔记录仍可识别
counter_medium=0
for name in reversed(history):
    if name in tier1:
        break
    counter_medium+=1
#从后往前数到最近一次1档，之间的抽数即为counter_medium
counter_lite=0
for name in reversed(history):
    if name in tier2:
        break
    counter_lite+=1
#从后往前数到最近一次2档，之间的抽数即为counter_lite
if counter_medium>30:
    n=counter_medium-30
    weight[0]+=0.02*n
    weight[-1]-=0.02*n
#历史记录已超过30抽未出1档时，先把已发生的概率偏移补上
result=[]
#结果记录器
num=int(input("输入抽取次数:"))
#直接使用input会输入str类型，用int()控制num变量类型
r=open(results_path,'a',encoding="utf-8")
#打开结果记录文件
for i in range(num):
    if counter_medium==49:
        l=list(tier1)
    elif counter_lite==9:
        l=list(tier2)
    else:
        l=random.choices(levels,weights=weight,k=1)[0]
    #满49次未出1档必出1档；满9次未出2档必出2档
    res=random.choice(l)
    result.append(res)
    counter_medium+=1
    counter_lite+=1
    if res in tier1:
        counter_medium=0
        counter_lite=0
        weight=list(base_weight)
        #抽出1档后 medium、lite 一并清零，概率恢复为配置值
    elif counter_medium>30:
        weight[0]+=0.02
        weight[-1]-=0.02
        #超过30抽未出1档时，每再抽1次：1档+0.02，最后一档-0.02
    if res in tier2:
        counter_lite=0
    #抽出2档时仅清零 lite
    draw_tier=""
    for tid in tier_ids:
        if res in pool["tiers"][tid]:
            draw_tier=tid
            break
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    r.write("[{}]|[counter_lite: {};counter_medium: {}]|[tier: {}]|[character: {}]\n".format(now,counter_lite,counter_medium,draw_tier,res))
    #按日志格式写入单次抽卡记录
print(result)
r.close()
#关闭文件，数据写入