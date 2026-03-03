import requests
import os
import json
from dotenv import load_dotenv

# Load our secret passwords
load_dotenv()

def scrape_website(url):
    print(f"Scraping {url}...")
    # Add Jina API to the front of our URL
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    return response.text

def summarize_text(text):
    print("Summarizing with AI...")
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": "You are a tech analyst. Summarize the following text into 3 key bullet points."},
            {"role": "user", "content": text[:8000]} 
        ]
    }
        
    response = requests.post(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    data = response.json()

    if "choices" not in data:
        print("Unexpected response:", data)
        return "AI failed."

    return data["choices"][0]["message"]["content"]

def send_telegram_message(message):
    print("Sending to Telegram...")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "Markdown"
}
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    # Let's scrape Hacker News today
    target_url = "https://news.ycombinator.com/"
    
    # 1. Scrape
    raw_content = scrape_website(target_url)
    
    # 2. Summarize
    ai_summary = summarize_text(raw_content)
    
    # 3. Send
    send_telegram_message(f"🚀 *Daily Tech Update*\n\n{ai_summary}")
    
    print("Task Complete!")