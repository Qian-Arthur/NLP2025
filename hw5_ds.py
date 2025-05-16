import os
import requests
import webbrowser
from pathlib import Path

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
OUTPUT_FILE = "generated_webpage.html"

def generate_webpage_content(api_key: str, theme: str) -> str:
    """
    调用DeepSeek API生成网页内容
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 精心设计的系统提示词
    system_prompt = """你是一个专业的前端开发工程师。请生成完整的HTML+CSS代码，要求：
    1. 现代响应式设计
    2. 包含导航栏、主体内容区和页脚
    3. 美观的色彩搭配
    4. 包含至少3个内容区块
    5. 使用Flexbox或Grid布局
    6. 添加适当的交互动画
    输出只需包含完整的HTML代码，不需要额外解释。"""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"网页主题：{theme}"}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {str(e)}")
        return ""

def save_and_preview(content: str):
    """
    保存并预览生成的网页
    """
    try:
        # 确保内容以<!DOCTYPE html>开头
        if not content.strip().lower().startswith("<!doctype html>"):
            content = f"<!DOCTYPE html>\n{content}"
            
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        
        # 获取绝对路径确保浏览器能正确加载
        abs_path = Path(OUTPUT_FILE).resolve()
        print(f"网页已生成至：{abs_path}")
        webbrowser.open(f"file://{abs_path}")
    except Exception as e:
        print(f"文件操作失败: {str(e)}")

if __name__ == "__main__":
    # 配置参数
    api_key = os.getenv("DEEPSEEK_API_KEY") or "sk-0fbf3033883c45c39ee13b3939401132"  # 建议使用环境变量
    theme = input("请输入网页主题（如：AI科技博客）：").strip() or "如何制造一个小黄人"
    
    # 生成内容
    html_content = generate_webpage_content(api_key, theme)
    
    if html_content:
        save_and_preview(html_content)
    else:
        print("网页生成失败，请检查API密钥和网络连接")
