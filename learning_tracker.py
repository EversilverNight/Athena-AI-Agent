import json
import datetime
from pathlib import Path
from duckduckgo_search import DDGS
from langchain_community.llms import Ollama
from config.settings import load_settings

LOG_FILE = Path("memory/learning_log.json")
NEWS_LOG_FILE = Path("memory/ai_news_log.json")

def update_behavior_model(user_text):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "input": user_text
    }

    # Ensure memory folder exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load old logs
    data = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        except:
            pass

    # Add new entry
    data.append(entry)

    # Save log
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def learn_from_ai_news():
    print("📰 Searching for latest AI news...")
    settings = load_settings()
    llm = Ollama(model=settings["light_model"])

    try:
        # Fetch AI news headlines
        with DDGS() as ddgs:
            results = ddgs.text("latest AI technology news", max_results=5)
            headlines = [res["title"] + " — " + res["body"] for res in results]

        print("📡 News fetched. Analyzing...")

        insights = []
        for article in headlines:
            prompt = f"""Analyze this AI news and extract key improvement ideas for a local offline AI assistant like Athena:
            
{article}

Respond only with practical insights, tools, or behaviors that Athena can learn or adapt."""
            result = llm(prompt)
            insights.append({"headline": article, "insight": result})

        # Save insights
        with open(NEWS_LOG_FILE, "w") as f:
            json.dump(insights, f, indent=2)

        print("✅ AI insights logged for future learning.")
    except Exception as e:
        print("❌ Failed to fetch or analyze news:", e)
