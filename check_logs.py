import requests, urllib.parse

base64 = "dGVyYXBrY286KDMjSkNrMlZ5bjk0aFk="
headers = {"Authorization": f"Basic {base64}"}

url = "https://167.235.11.154:2083/execute/Fileman/get_file_content?dir=" + urllib.parse.quote("/home/terapkco/xcomic_backend") + "&file=stderr.log"
r = requests.get(url, headers=headers, verify=False)
data = r.json()
print("Keys:", data.keys())
print("Data block:", data.get('data'))
