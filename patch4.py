with open('main_live.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = "return result"
new_str = """from fastapi.encoders import jsonable_encoder
        return jsonable_encoder(result)"""

text = text.replace(old_str, new_str)

with open('main_live.py', 'w', encoding='utf-8') as f:
    f.write(text)
