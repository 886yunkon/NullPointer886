#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from openai import OpenAI

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

def call_qwen(topic: str) -> str:
    if not DASHSCOPE_API_KEY:
        raise Exception("❌ 未设置 DASHSCOPE_API_KEY 环境变量")

    # =================== 请在这里修改你的人设 ===================
    prompt = f"""
你的身份设定：
- 你是一位货币交易行业 3 年，从前是游戏搬砖玩家，后来转做平台推广，分享学习心得，最后点到现在在从事的平台：（网站链接），推荐加入
- 你的说话风格务实、接地气、不吹牛。不喊“一夜暴富”，只说“稳一点，少踩坑”偏向口语化，偶尔使用网络热词，但不过分
- 你喜欢用生活经历中的小故事引出”板砖辛苦但是回报满满“的道理
- 文章受众是初次认识货币搬砖，听说过B特币的年轻人，他们喜欢真实、不装、有干货的内容

写作要求：
- 大约500字左右
- 基于以下主题写一篇博客文章：「{topic}」
- 标题自拟，要抓人眼球
- 用自然的中文语气，避免生硬的“首先、其次、最后”
- 加入一个你自己的小故事或体感细节

直接输出文章的Markdown正文，不要多余的解释。
"""
    # ========================================================

    try:
        client = OpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen-max",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"❌ 阿里云API调用失败: {str(e)}")

def save_post(content: str, topic: str) -> str:
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
    parser = argparse.ArgumentParser(description="生成 AI 博客文章")
    parser.add_argument("--topic", required=True, help="文章主题")
    args = parser.parse_args()

    try:
        print(f"📝 开始生成文章，主题：{args.topic}")
        content = call_qwen(args.topic)
        save_post(content, args.topic)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
