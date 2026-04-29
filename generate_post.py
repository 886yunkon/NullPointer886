#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from datetime import datetime
from pathlib import Path

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def call_deepseek(topic: str) -> str:
    if not DEEPSEEK_API_KEY:
        raise Exception("❌ 未设置 DEEPSEEK_API_KEY 环境变量")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    # =================== 请在这里修改你的人设 ===================
    prompt = f"""
你的身份设定：
- 你是一位对编程和技术充满热情的开发者，喜欢用轻松幽默的方式分享学习心得
- 你的说话风格偏向口语化，偶尔使用网络热词，但不过分
- 你喜欢用生活中的小故事引出技术道理
- 文章受众是初入职场或自学编程的年轻人，他们喜欢真实、不装、有干货的内容

写作要求：
- 大约500字左右
- 基于以下主题写一篇博客文章：「{topic}」
- 标题自拟，要抓人眼球
- 用自然的中文语气，避免生硬的“首先、其次、最后”
- 加入一个你自己的小故事或体感细节

直接输出文章的Markdown正文，不要多余的解释。
"""
    # ========================================================

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1500,
    }

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )

    if response.status_code != 200:
        raise Exception(f"❌ API 调用失败: {response.text}")

    return response.json()["choices"][0]["message"]["content"]

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
        content = call_deepseek(args.topic)
        save_post(content, args.topic)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
