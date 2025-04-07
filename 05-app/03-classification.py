from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

q1 = "我刚买的XYZ智能手表无法同步我的日历，我应该怎么办？"
q2 = "XYZ手表的电池可以持续多久？"
q3 = "XYZ品牌的手表和ABC品牌的手表相比，有什么特别的功能吗？"
q4 = "安装XYZ智能手表的软件更新后，手表变得很慢，这是啥原因？"
q5 = "XYZ智能手表防水不？我可以用它来记录我的游泳数据吗？"
q6 = "我想知道XYZ手表的屏幕是什么材质，容不容易刮花？"
q7 = "请问XYZ手表标准版和豪华版的售价分别是多少？还有没有进行中的促销活动？"
q8 = "请问XYZ手表标准版和豪华版的售价分别是多少？还有没有进行中的促销活动？"

q_list = [q1, q2, q3, q4, q5, q6, q7,q8]

category_list = ["产品规格", "使用咨询", "功能比较", "用户反馈", "价格查询", "故障问题", "其它"]

classify_prompt_template = """
你的任务是为用户对产品的疑问进行分类。
请仔细阅读用户的问题内容，给出所属类别。类别应该是这些里面的其中一个：{categories}。
直接输出所属类别，不要有任何额外的描述或补充内容。
用户的问题内容会以三个#符号进行包围。

###
{question}
###
"""


for q in q_list:
    classify_prompt = classify_prompt_template.format(categories=category_list, question=q)

    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
        {"role": "system", "content": classify_prompt},
        {"role": "user", "content": q},
    ],
    stream=False
    )   

    print(response.choices[0].message.content)


