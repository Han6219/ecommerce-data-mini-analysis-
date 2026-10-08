# analysis.py
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文显示，防止图表中文乱码
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False

# ----------------------1、模拟原始电商数据（相当于Kaggle下载的数据集）----------------------
data = {
    "user_id": [i for i in range(1,5001)] * 2,
    "hour": [8,10,12,15,19,20,21,22]*1250,
    "city":["北京","上海","Unknown","广州","南昌"]*2000,
    "category":["美妆","服饰","家居","图书","数码"]*2000,
    "behavior":["browse","cart","collect","purchase"]*2500,
    "amount":[0,0,0,120,230,88,19.9,299]*1250
}
df = pd.DataFrame(data)

# 人为制造重复、缺失，模拟真实脏数据
df = pd.concat([df, df.head(50)], ignore_index=True) # 加50条重复行
df.loc[0:100,"city"] = None #制造部分缺失

print("原始数据行数：", len(df))

# ----------------------2、数据清洗（核心步骤）----------------------
## ①删除重复行
df = df.drop_duplicates()

## ②剔除 city 是 Unknown、city为空的行
df = df[ (~df["city"].isna()) & (df["city"] != "Unknown") ]

print("清洗之后数据行数：", len(df))

# 输出清洗好的数据到csv，这个就是要上传github的 cleaned_data.csv
df.to_csv("cleaned_data.csv", index=False, encoding="utf‑8‑sig")


# ----------------------3、分组统计分析----------------------
# 3‑1：不同品类销售额，只统计purchase购买行为
sale_df = df[df["behavior"]=="purchase"].groupby("category")["amount"].sum().reset_index()
sale_df = sale_df.sort_values("amount", ascending=False)
print("\n====各品类销售额====")
print(sale_df)

#3‑2：转化漏斗：去重user_id，统计每种行为独立用户数
funnel = df.groupby("behavior")["user_id"].nunique().reset_index()
print("\n====用户行为漏斗====")
print(funnel)

#3‑3：分小时活跃用户数
hour_active = df.groupby("hour")["user_id"].nunique().reset_index()
print("\n====分时段活跃用户====")
print(hour_active)


# ----------------------4、画三张图，保存图片（后面插入word报告）----------------------
#图1：品类销售额柱状图
plt.figure(figsize=(8,5))
plt.bar(sale_df["category"], sale_df["amount"], color="#6388bb")
plt.title("各商品品类销售额排名")
plt.xlabel("商品品类")
plt.ylabel("总销售额")
plt.tight_layout()
plt.savefig("chart1_品类销售额.png", dpi=150)
plt.close()

#图2：转化漏斗柱状图
plt.figure(figsize=(8,5))
plt.bar(funnel["behavior"], funnel["user_id"], color="#7799cc")
plt.title("用户行为转化漏斗")
plt.xlabel("用户行为")
plt.ylabel("独立用户数")
plt.tight_layout()
plt.savefig("chart2_转化漏斗.png",dpi=150)
plt.close()

#图3：时段活跃度折线图
plt.figure(figsize=(8,5))
plt.plot(hour_active["hour"], hour_active["user_id"], marker="o", color="#4472b3")
plt.title("分时段用户活跃度")
plt.xlabel("小时")
plt.ylabel("独立活跃用户数")
plt.tight_layout()
plt.savefig("chart3_时段活跃.png",dpi=150)
plt.close()

print("\n✅全部执行完成！")
print("输出文件：cleaned_data.csv 、三张png图表")