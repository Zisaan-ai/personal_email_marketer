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

MODEL_NAME = "llama-3.3-70b-versatile"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

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

def _call_ai_api(prompt: str) -> str:
    """Helper to make a direct REST API call to Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API Key is missing. Please go to Settings → AI Configuration and add your Groq API key.")
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}"
    }
    
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    
    if response.status_code != 200:
        try:
            err_data = response.json()
            err_msg = err_data.get("error", {}).get("message", response.text)
            raise ValueError(f"Groq API Error: {err_msg}")
        except json.JSONDecodeError:
            raise ValueError(f"Groq API Error {response.status_code}: {response.text}")
            
    data = response.json()
    try:
        text = data["choices"][0]["message"]["content"]
        return text
    except (KeyError, IndexError):
        raise ValueError("Unexpected response format from Groq API.")

def handle_ai_error(e: Exception) -> dict:
    """Helper to cleanly format AI errors for the frontend."""
    msg = str(e)
    print(f"AI ERROR: {msg}")
    return {"error": msg}

def generate_email_content(prompt: str) -> dict:
    try:
        full_prompt = f"""
        You are an expert cold email copywriter. Write a highly converting cold email based on these instructions.
        Make it short, punchy, and use Spintax (e.g. {{Hi|Hello}} {{Name|Friend}}) for variation.
        Output ONLY the HTML body of the email. Do not wrap in markdown tags like ```html.
        
        User instructions: {prompt}
        {extract_url_content(prompt)}
        """
        text = _call_ai_api(full_prompt).strip()
        if text.startswith("```html"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return {"html": text.strip()}
    except Exception as e:
        return handle_ai_error(e)

def optimize_subject(subject: str) -> dict:
    try:
        prompt = f"""
        Rewrite the following email subject line into a Spintax format to bypass spam filters.
        Output ONLY the spintax string, nothing else. Example output: {{Quick question|Thoughts}} regarding {{your website|the project}}
        
        Subject to rewrite: {subject}
        """
        text = _call_ai_api(prompt).strip()
        return {"subject": text}
    except Exception as e:
        return handle_ai_error(e)

def generate_icebreakers(csv_content: str) -> dict:
    try:
        prompt = f"""
        You are an AI sales assistant. I have a list of leads in comma-separated format.
        For each lead, generate a highly personalized, single-sentence icebreaker based on their company or name.
        
        CRITICAL RULES:
        1. Return exactly the SAME lines I provided, but append `, "Your Icebreaker here"` to the end of each line.
        2. Do NOT add any headers like "Email,Name,Company,Icebreaker" unless they were already in the input.
        3. Do NOT add any explanations, greetings, or markdown wrappers. Output ONLY the raw text lines.
        4. Make the icebreakers professional but conversational.
        
        Input Data:
        {csv_content}
        """
        text = _call_ai_api(prompt).strip()
        if text.startswith("```csv"):
            text = text[6:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return {"csv": text.strip()}
    except Exception as e:
        return handle_ai_error(e)

def analyze_sentiment(text: str) -> str:
    try:
        prompt = f"""
        You are an AI sales assistant. Read this email reply and classify its sentiment.
        Choose ONLY ONE from these exact tags:
        Interested
        Not Interested
        Meeting Booked
        Out of Office
        Questions / Objections
        Unknown

        Email:
        {text}
        """
        sentiment = _call_ai_api(prompt).strip()
        valid = ["Interested", "Not Interested", "Meeting Booked", "Out of Office", "Questions / Objections", "Unknown"]
        for v in valid:
            if v.lower() in sentiment.lower():
                return v
        return "Unknown"
    except Exception as e:
        print(f"Sentiment Analysis Error: {e}")
        return "Unknown"

def generate_autopilot_campaign(prompt: str) -> dict:
    try:
        full_prompt = f"""
        You are an expert email marketing copywriter. 
        Based on the following product/service description (or scraped URL content), generate a full cold email campaign.
        
        You must return ONLY a valid JSON object with the following exact keys:
        - "subject_a": A highly optimized spintax subject line for the first email.
        - "body_a": The HTML body of the first email (use Spintax).
        - "subject_b": An alternative spintax subject line (or follow-up subject).
        - "body_b": The HTML body of a follow-up email if they don't reply (use Spintax).
        
        Do not use markdown blocks like ```json around the output, just raw JSON.

        User Input: {prompt}
        {extract_url_content(prompt)}
        """
        text = _call_ai_api(full_prompt).strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return {"error": "AI generated invalid JSON. Please try again."}
    except Exception as e:
        return handle_ai_error(e)

def chat_with_assistant(message: str, history: list = None) -> str:
    try:
        if not history:
            history = []
        
        # Format history for Groq
        system_prompt = (
            "You are a Senior Cold Email Copywriter and Direct Response Marketing Strategist. "
            "Your objective is to help the user write highly converting, personalized, and punchy cold emails. "
            "Always follow these rules:\\n"
            "1. Be conversational and professional.\\n"
            "2. Keep emails extremely concise (under 150 words usually).\\n"
            "3. Use proven frameworks like AIDA (Attention, Interest, Desire, Action) or PAS (Problem, Agitation, Solution).\\n"
            "4. Focus on the prospect's benefits, not just product features.\\n"
            "5. Always end with a clear, low-friction Call To Action (CTA).\\n"
            "6. When asked for advice, give strategic, actionable, and data-backed recommendations."
        )
        groq_history = [{'role': 'system', 'content': system_prompt}]
        for msg in history:
            role = 'user' if msg.get('role') == 'user' else 'assistant'
            groq_history.append({'role': role, 'content': msg.get('content', '')})
            
        groq_history.append({'role': 'user', 'content': message})
        
        import os, requests
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key: return 'API Key is missing.'
        
        payload = {
            'model': MODEL_NAME,
            'messages': groq_history,
            'temperature': 0.7
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        res = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if res.status_code != 200:
            return f'AI Error: {res.text}'
            
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f'AI Error: {str(e)}'

def draft_reply_to_email(client_message: str) -> str:
    try:
        prompt = f"""
        You are an expert sales assistant. Read the following reply from a client and draft a polite, professional response.
        If they are interested, try to book a meeting or offer more details. 
        If they have a question, answer it logically (make reasonable assumptions or say you'll get back to them).
        If they are not interested, politely thank them for their time and leave the door open.
        
        Output ONLY the email body (no subject line). Do NOT wrap in markdown like ```html. Do not include signature, just the main message.
        
        Client's Reply:
        {client_message}
        """
        text = _call_ai_api(prompt).strip()
        if text.startswith("```html"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        print(f"AI Reply Draft Error: {e}")
        return "I apologize, but I could not automatically generate a reply due to an error."
