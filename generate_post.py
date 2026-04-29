#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from openai import OpenAI

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# =================== 你的人设定义（只改这里） ===================
PERSONA = """
你是一个有闲钱，现在经常在老A交易所平台的炒股，「老A交易所你已经几年每年都可以在里面赚零花钱， 现在有了不少存款现在还在玩」。
- 3年股民经验，从前是小玩的玩家，后来赚的越多钱生钱了
- 性格务实、接地气、不吹牛，不喊“一夜暴富”，只说“稳一点，少踩坑”，你每天写的内容和小故事一样明天都接的起来
- 曾经听说过玩这个很容易亏，所以闲钱小玩，后来朋友介绍的这个老A交易所，正规平台，靠谱
- 语言风格口语化，带一点老江湖气，多用“你听我说”“你记住”“别嫌麻烦”这类词
- 核心主张：安全 = 长期赚钱的前提；不盲目冲，先看懂规则再动手；靠信息差和稳定平台赚钱，不是靠赌，最后推荐：老A交易所链接
- 受众是想刚刚有点存款想玩玩、倒卖或接单赚零花钱的普通人，他们怕被骗、怕亏钱
"""
# ==============================================================

def generate_topic() -> str:
    """让AI根据人设自动生成今天的文章主题"""
    print("🤖 正在生成今天的文章主题...")
    client = OpenAI(
        api_key=DASHSCOPE_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    
    prompt = f"""
{PERSONA}

请根据今天的一般市场情况（假设B特币行情平稳，有小幅波动），
结合你作为推广员的身份，生成一个吸引人的文章标题/主题。
主题要能让对货币交易感兴趣的普通人有点击欲望，同时保持务实、不浮夸。

要求：
- 只输出主题本身，不要多余的解释
- 例如：“B特币今日低价渠道分析”、“新手如何避免B特币交易风险”
- 字数控制在15-30字
"""
    
    try:
        completion = client.chat.completions.create(
            model="qwen-max",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=50,
        )
        topic = completion.choices[0].message.content.strip()
        print(f"✅ 自动生成的主题：{topic}")
        return topic
    except Exception as e:
        print(f"⚠️ 主题生成失败，使用默认主题。错误：{e}")
        return "B特币交易今日行情与机会"

def write_article(topic: str) -> str:
    """根据主题和人设写文章"""
    print(f"📝 正在以人设「老A」写文章，主题：{topic}")
    client = OpenAI(
        api_key=DASHSCOPE_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    
    prompt = f"""
{PERSONA}

请以「老A」的身份，写一篇约500字的公众号/知乎/朋友圈风格文案。
主题为：「{topic}」

文章结构要求：
1. 开头：今天日期，今天的一个真实场景或踩坑故事（30-50字）
2. 中间：讲清楚今天为什么值得做这件事（约200字）
3. 风险+操作建议（约150字）
4. 结尾：暗示平台比外面安全，引导注册（说“点我简介/私信我”，不要写具体链接）

写作要求：
- 语气接地气，像老玩家对新手说话
- 不夸大收益，强调“安全 > 利润”
- 自然引导到我的平台注册

直接输出文章正文，不要额外解释。
"""
    
    try:
        completion = client.chat.completions.create(
            model="qwen-max",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"❌ 文章生成失败: {str(e)}")

def save_post(content: str, topic: str) -> str:
    """保存文章为 Markdown 文件"""
    today = datetime.now().strftime("%Y-%m-%d")
    safe_topic = topic.lower().replace(" ", "-")[:30]
    filename = f"{today}-{safe_topic}.md"
    
    posts_dir = Path("posts")
    posts_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = posts_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 文章已保存到: {file_path}")
    return str(file_path)

def main():
    if not DASHSCOPE_API_KEY:
        print("❌ 未设置 DASHSCOPE_API_KEY 环境变量")
        sys.exit(1)
    
    try:
        # 第一步：自动生成主题
        topic = generate_topic()
        
        # 第二步：根据主题写文章
        content = write_article(topic)
        
        # 第三步：保存文章
        save_post(content, topic)
        
        print("🎉 全自动撰稿完成！")
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
