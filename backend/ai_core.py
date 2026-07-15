import os
import re
import urllib.request
from bs4 import BeautifulSoup
import json
import requests
from dotenv import load_dotenv

# Try to load env file to get API key if running locally
load_dotenv('backend/.env')
load_dotenv('.env')

# --- Default Models ---
MODEL_NAME_OPENAI = "gpt-4o-mini"
MODEL_NAME_ANTHROPIC = "claude-3-haiku-20240307"
MODEL_NAME_DEEPSEEK = "deepseek-chat"
MODEL_NAME_GROQ = "llama-3.3-70b-versatile"
MODEL_NAME_GEMINI = "gemini-1.5-flash" # Assuming if needed

API_URL_OPENAI = "https://api.openai.com/v1/chat/completions"
API_URL_ANTHROPIC = "https://api.anthropic.com/v1/messages"
API_URL_DEEPSEEK = "https://api.deepseek.com/chat/completions"
API_URL_GROQ = "https://api.groq.com/openai/v1/chat/completions"
API_URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

def extract_url_content(text: str) -> str:
    urls = re.findall(r'(https?://[^\s()]+)', text)
    if not urls:
        return ""
    
    context = "\n\n--- Scraped Context from URLs ---\n"
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract()
                text_content = soup.get_text(separator=' ', strip=True)
                context += f"\nURL: {url}\nContent: {text_content[:5000]}\n"
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            context += f"\nURL: {url}\n(Could not read content)\n"
    return context

def _get_active_provider(user) -> dict:
    """Returns the priority API provider details based on user's saved keys."""
    # Priority: Anthropic > OpenAI > DeepSeek > Groq > Gemini
    if user:
        if getattr(user, 'anthropic_api_key', None):
            return {"provider": "anthropic", "key": user.anthropic_api_key, "url": API_URL_ANTHROPIC, "model": MODEL_NAME_ANTHROPIC}
        if getattr(user, 'openai_api_key', None):
            return {"provider": "openai", "key": user.openai_api_key, "url": API_URL_OPENAI, "model": MODEL_NAME_OPENAI}
        if getattr(user, 'deepseek_api_key', None):
            return {"provider": "deepseek", "key": user.deepseek_api_key, "url": API_URL_DEEPSEEK, "model": MODEL_NAME_DEEPSEEK}
        if getattr(user, 'groq_api_key', None):
            return {"provider": "groq", "key": user.groq_api_key, "url": API_URL_GROQ, "model": MODEL_NAME_GROQ}
        if getattr(user, 'gemini_api_key', None):
            return {"provider": "gemini", "key": user.gemini_api_key, "url": API_URL_GEMINI, "model": MODEL_NAME_GEMINI}
        # Fallback to env vars if no user keys found (e.g., admin usage)
    
    # Check env vars with same priority
    if os.getenv("ANTHROPIC_API_KEY"):
        return {"provider": "anthropic", "key": os.getenv("ANTHROPIC_API_KEY"), "url": API_URL_ANTHROPIC, "model": MODEL_NAME_ANTHROPIC}
    if os.getenv("OPENAI_API_KEY"):
        return {"provider": "openai", "key": os.getenv("OPENAI_API_KEY"), "url": API_URL_OPENAI, "model": MODEL_NAME_OPENAI}
    if os.getenv("DEEPSEEK_API_KEY"):
        return {"provider": "deepseek", "key": os.getenv("DEEPSEEK_API_KEY"), "url": API_URL_DEEPSEEK, "model": MODEL_NAME_DEEPSEEK}
    if os.getenv("GROQ_API_KEY"):
        return {"provider": "groq", "key": os.getenv("GROQ_API_KEY"), "url": API_URL_GROQ, "model": MODEL_NAME_GROQ}
    if os.getenv("GEMINI_API_KEY"):
        return {"provider": "gemini", "key": os.getenv("GEMINI_API_KEY"), "url": API_URL_GEMINI, "model": MODEL_NAME_GEMINI}
        
    raise ValueError("No AI API Keys found. Please go to Settings → AI Configuration and add an API key.")

def _call_ai_api(prompt: str, user=None, system_prompt: str = None, history: list = None) -> str:
    """Universal AI API caller."""
    provider_info = _get_active_provider(user)
    provider = provider_info["provider"]
    api_key = provider_info["key"]
    url = provider_info["url"]
    model = provider_info["model"]
    
    if provider == "anthropic":
        headers = {
            "x-api-key": api_key.strip(),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Format messages for Anthropic
        messages = []
        if history:
            for msg in history:
                role = 'user' if msg.get('role') == 'user' else 'assistant'
                # Anthropic doesn't allow 'system' in messages, it's a top-level param
                if msg.get('role') != 'system':
                    messages.append({'role': role, 'content': msg.get('content', '')})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "max_tokens": 1024,
            "messages": messages,
            "temperature": 0.7
        }
        if system_prompt:
            payload["system"] = system_prompt
            
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if res.status_code != 200:
            raise ValueError(f"Anthropic API Error: {res.text}")
            
        return res.json()["content"][0]["text"]
        
    else:
        # OpenAI compatible (OpenAI, DeepSeek, Groq)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key.strip()}"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        if history:
            for msg in history:
                role = 'user' if msg.get('role') == 'user' else 'assistant'
                if msg.get('role') == 'system' and not system_prompt: # Use history system prompt if provided
                    messages.insert(0, {'role': 'system', 'content': msg.get('content', '')})
                elif msg.get('role') != 'system':
                    messages.append({'role': role, 'content': msg.get('content', '')})
                    
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7
        }
        
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if res.status_code != 200:
            raise ValueError(f"{provider.capitalize()} API Error: {res.text}")
            
        return res.json()["choices"][0]["message"]["content"]

def handle_ai_error(e: Exception) -> dict:
    msg = str(e)
    print(f"AI ERROR: {msg}")
    return {"error": msg}

def generate_email_content(prompt: str, user=None) -> dict:
    try:
        system_prompt = "You are an expert cold email copywriter. Write a highly converting cold email based on instructions. Output ONLY the HTML body of the email. Do not wrap in markdown tags like ```html."
        full_prompt = f"Make it short, punchy, and use Spintax (e.g. {{Hi|Hello}} {{Name|Friend}}) for variation.\n\nUser instructions: {prompt}\n{extract_url_content(prompt)}"
        text = _call_ai_api(full_prompt, user, system_prompt=system_prompt).strip()
        
        if text.startswith("```html"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        return {"html": text.strip()}
    except Exception as e:
        return handle_ai_error(e)

def optimize_subject(subject: str, user=None) -> dict:
    try:
        prompt = f"Rewrite the following email subject line into a Spintax format to bypass spam filters. Output ONLY the spintax string, nothing else. Example output: {{Quick question|Thoughts}} regarding {{your website|the project}}\n\nSubject to rewrite: {subject}"
        text = _call_ai_api(prompt, user).strip()
        return {"subject": text}
    except Exception as e:
        return handle_ai_error(e)

def generate_icebreakers(leads_csv: str, user=None) -> dict:
    try:
        prompt = f"You are an AI sales assistant. I have a list of leads in comma-separated format. For each lead, generate a highly personalized, single-sentence icebreaker based on their company or name.\nCRITICAL RULES:\n1. Return exactly the SAME lines I provided, but append `, \"Your Icebreaker here\"` to the end of each line.\n2. Do NOT add any headers.\n3. Do NOT add any explanations, greetings, or markdown wrappers. Output ONLY the raw text lines.\n\nInput Data:\n{leads_csv}"
        text = _call_ai_api(prompt, user).strip()
        
        if text.startswith("```csv"): text = text[6:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        return {"csv": text.strip()}
    except Exception as e:
        return handle_ai_error(e)

def analyze_reply_sentiment(text: str, user=None) -> str:
    try:
        prompt = f"You are an AI sales assistant. Read this email reply and classify its sentiment. Choose ONLY ONE from these exact tags: Interested, Not Interested, Meeting Booked, Out of Office, Questions / Objections, Unknown.\n\nEmail:\n{text}"
        sentiment = _call_ai_api(prompt, user).strip()
        valid = ["Interested", "Not Interested", "Meeting Booked", "Out of Office", "Questions / Objections", "Unknown"]
        for v in valid:
            if v.lower() in sentiment.lower():
                return v
        return "Unknown"
    except Exception as e:
        print(f"Sentiment Analysis Error: {e}")
        return "Unknown"

def generate_autopilot_campaign(prompt: str, user=None) -> dict:
    try:
        system_prompt = "You are an expert email marketing copywriter."
        full_prompt = f"Based on the following description, generate a full cold email campaign. You must return ONLY a valid JSON object with keys: 'subject_a', 'body_a', 'subject_b', 'body_b'. Use spintax for everything. Do not use markdown blocks like ```json around the output, just raw JSON.\n\nUser Input: {prompt}\n{extract_url_content(prompt)}"
        text = _call_ai_api(full_prompt, user, system_prompt=system_prompt).strip()
        
        if text.startswith("```json"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
            
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return {"error": "AI generated invalid JSON. Please try again."}
    except Exception as e:
        return handle_ai_error(e)

def chat_with_assistant(message: str, history: list = None, user=None) -> str:
    try:
        system_prompt = (
            "You are an Elite Direct Response Marketing Strategist and World-Class B2B Cold Email Copywriter with a proven track record of generating millions in pipeline. "
            "Your sole objective is to help the user craft hyper-personalized, ruthlessly concise, and ridiculously high-converting cold emails.\\n\\n"
            "CRITICAL RULES YOU MUST OBEY:\\n"
            "1. ULTRA-CONCISE: Never write an email longer than 75-125 words. Attention spans are zero.\\n"
            "2. HYPER-RELEVANT: Focus entirely on the prospect's pain points.\\n"
            "3. FORMATTING FOR READABILITY: Use short paragraphs (1-2 sentences max). Use bold text.\\n"
            "4. SOFT CTA: Never ask for a 30-minute call. End with a low-friction CTA.\\n"
            "5. NO SPAMMY LANGUAGE: Avoid all salesy buzzwords.\\n"
            "6. DELIVER MASSIVE VALUE: Provide actionable frameworks, subject line variations.\\n"
            "7. ALWAYS PROVIDE VARIATIONS: Provide 2 distinct angles."
        )
        
        text = _call_ai_api(message, user, system_prompt=system_prompt, history=history).strip()
        return text
    except Exception as e:
        return f'AI Error: {str(e)}'

def draft_reply_to_email(client_message: str, user=None) -> str:
    try:
        prompt = f"You are an expert sales assistant. Read the following reply from a client and draft a polite, professional response. If they are interested, try to book a meeting or offer more details. If they have a question, answer it logically. If they are not interested, politely thank them. Output ONLY the email body (no subject line). Do NOT wrap in markdown like ```html.\n\nClient's Reply:\n{client_message}"
        text = _call_ai_api(prompt, user).strip()
        
        if text.startswith("```html"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        return text.strip()
    except Exception as e:
        print(f"AI Reply Draft Error: {e}")
        return "I apologize, but I could not automatically generate a reply due to an error."