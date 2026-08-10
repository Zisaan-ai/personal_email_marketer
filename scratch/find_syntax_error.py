with open(r"C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\app.js", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "toggleMobileNav" in line or "toggleMobileMenu" in line:
        print(f"Line {idx+1}: {line.strip()}")
