import os

with open('main_live.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_models = """class OpenAIKeyRequest(BaseModel):
    openai_api_key: str

class AnthropicKeyRequest(BaseModel):
    anthropic_api_key: str

class DeepSeekKeyRequest(BaseModel):
    deepseek_api_key: str

class VerifyKeyRequest(BaseModel):
    provider: str
    api_key: str
"""

new_endpoints = """
@app.post("/api/settings/openai")
def save_openai_key(req: OpenAIKeyRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    current_user.openai_api_key = req.openai_api_key
    db.commit()
    os.environ["OPENAI_API_KEY"] = req.openai_api_key
    return {"ok": True, "message": "OpenAI API key saved"}

@app.post("/api/settings/anthropic")
def save_anthropic_key(req: AnthropicKeyRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    current_user.anthropic_api_key = req.anthropic_api_key
    db.commit()
    os.environ["ANTHROPIC_API_KEY"] = req.anthropic_api_key
    return {"ok": True, "message": "Anthropic API key saved"}

@app.post("/api/settings/deepseek")
def save_deepseek_key(req: DeepSeekKeyRequest, current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    current_user.deepseek_api_key = req.deepseek_api_key
    db.commit()
    os.environ["DEEPSEEK_API_KEY"] = req.deepseek_api_key
    return {"ok": True, "message": "DeepSeek API key saved"}

@app.post("/api/settings/verify_key")
def verify_key_endpoint(req: VerifyKeyRequest, current_user: database.User = Depends(auth.get_current_user)):
    import requests
    provider = req.provider.lower()
    key = req.api_key
    
    if not key:
        return {"status": "no_key"}
        
    try:
        if provider == "gemini":
            res = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={key}", timeout=5)
            if res.status_code == 200: return {"status": "valid"}
            else: return {"status": "invalid"}
            
        elif provider == "groq":
            res = requests.get("https://api.groq.com/openai/v1/models", headers={"Authorization": f"Bearer {key}"}, timeout=5)
            if res.status_code == 200: return {"status": "valid"}
            else: return {"status": "invalid"}
            
        elif provider == "openai":
            res = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {key}"}, timeout=5)
            if res.status_code == 200: return {"status": "valid"}
            else: return {"status": "invalid"}
            
        elif provider == "anthropic":
            res = requests.get("https://api.anthropic.com/v1/messages", headers={"x-api-key": key, "anthropic-version": "2023-06-01"}, json={"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[{"role":"user","content":"Hi"}]}, timeout=5)
            if res.status_code == 200: return {"status": "valid"}
            else: return {"status": "invalid"}
            
        elif provider == "deepseek":
            res = requests.get("https://api.deepseek.com/models", headers={"Authorization": f"Bearer {key}"}, timeout=5)
            if res.status_code == 200: return {"status": "valid"}
            else: return {"status": "invalid"}
            
        return {"status": "invalid"}
    except Exception:
        return {"status": "invalid"}
"""

content = content.replace("class GroqKeyRequest(BaseModel):\n    groq_api_key: str", "class GroqKeyRequest(BaseModel):\n    groq_api_key: str\n\n" + new_models)

get_settings_old = """    return {
        "gemini_api_key": current_user.gemini_api_key or "",
        "groq_api_key": current_user.groq_api_key or "",
    }"""
get_settings_new = """    return {
        "gemini_api_key": current_user.gemini_api_key or "",
        "groq_api_key": current_user.groq_api_key or "",
        "openai_api_key": current_user.openai_api_key or "",
        "anthropic_api_key": current_user.anthropic_api_key or "",
        "deepseek_api_key": current_user.deepseek_api_key or "",
    }"""
content = content.replace(get_settings_old, get_settings_new)

content = content.replace("    return {\"ok\": True, \"message\": \"Groq API key saved\"}", "    return {\"ok\": True, \"message\": \"Groq API key saved\"}\n" + new_endpoints)

with open('main_live.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Modified main_live.py')
