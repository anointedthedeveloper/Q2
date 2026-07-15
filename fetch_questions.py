import json
import time
import requests
from bs4 import BeautifulSoup

FILEPATH = r'c:\Users\Admin\Desktop\Q2\Use of English.json'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_real_question(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    h1 = soup.select_one('h1.mb-6.text-xl.font-semibold')
    if h1:
        return h1.get_text(separator=' ', strip=True)
    # fallback: any short h1
    for h1 in soup.find_all('h1'):
        text = h1.get_text(separator=' ', strip=True)
        if 10 < len(text) < 400:
            return text
    return None

def looks_like_passage(question):
    """Return True if the question field contains passage text instead of a real question."""
    q = question.strip()
    if not q:
        return False
    # Real questions are short and usually end with ? or are a short phrase
    # Passage text is long prose
    if len(q) < 200:
        return False
    # If it's long AND doesn't end with '?' it's almost certainly passage text
    q_norm = ' '.join(q.split())
    if q_norm.endswith('?'):
        return False
    return True

with open(FILEPATH, encoding='utf-8') as f:
    data = json.load(f)

fixed = 0
skipped = 0
for q in data:
    if not q.get('passage', '').strip():
        continue
    question = q.get('question', '')
    if not looks_like_passage(question):
        continue

    url = q.get('url', '')
    if not url:
        continue

    print(f"Fetching id={q['id']} {url}")
    real_q = fetch_real_question(url)

    if real_q:
        print(f"  -> {real_q[:100]}")
        q['question'] = real_q
        fixed += 1
    else:
        print(f"  -> Could not extract, skipping")
        skipped += 1

    time.sleep(0.5)

print(f"\nFixed {fixed} | Skipped {skipped}")

with open(FILEPATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
