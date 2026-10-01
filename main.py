"""
* 245150200111021 Edesius Jaty Giovanni: Regexing Task A & C
* 245150207111053 Alia Atikah Sana: Task B
* NIM_3 NAMA_3: -
* NIM_4 NAMA_4: -
* 
"""

import re
import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).parent
RESOURCE_DIR = BASE_DIR / "resource"
RESULTS_DIR  = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# TASK A
def parse_references(
  filepath=RESOURCE_DIR / "doc_1.txt",
  output=RESULTS_DIR / "a_judul.json"
):
  with open(filepath, "r", encoding="utf-8") as f:
    raw = f.read()

  blocks = re.split(r'\r?\n\s*\r?\n', raw.strip())
  results = []

  for block in blocks:
    block = block.strip()
    if not block:
      continue

    entry = {}

    year_match = re.search(r'\((\d{4})\)', block)
    if not year_match:
      year_match = re.search(r'\b((?:19|20)\d{2})\b', block)
    if not year_match:
      year_match = re.search(r'(?<=[A-Za-z])((?:19|20)\d{2})\b', block)
    if year_match:
      entry["year"] = year_match.group(1)

    title_match = re.search(r'["\u201c]([^"\u201d]+)["\u201d]', block)
    if title_match:
      entry["title"] = title_match.group(1).strip()
    else:
      no_quote_match = re.search(r'\(\d{4}\)[.,]?\s+([^.\n]+?)(?:\s*\((?:PDF|Thesis)\))?\s*\.', block)
      if no_quote_match:
        entry["title"] = no_quote_match.group(1).strip()
      else:
        dot_split = re.split(r'\.\s+', block, maxsplit=2)
        if len(dot_split) >= 2:
          candidate = dot_split[1].strip()
          if candidate and not re.match(r'^\d{4}', candidate) and 'http' not in candidate:
            entry["title"] = candidate

    if year_match and '(' + year_match.group(1) + ')' in block:
      before_year = block[:block.index('(' + year_match.group(1) + ')')].strip()
      before_year = re.sub(r'[.,\s]+$', '', before_year)
      if before_year:
        entry["authors"] = before_year
    else:
      author_match = re.match(r'^([^.\n]+?)\.', block)
      if author_match:
        cand = author_match.group(1).strip()
        if cand and 'http' not in cand:
          entry["authors"] = cand

    if not entry.get("title") and not entry.get("authors"):
      entry["title"] = block.strip()
    if entry.get("title") or entry.get("authors"):
      results.append(entry)

  with open(output, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

  return results


# TASK B
STOPWORDS_ID = {
    "yang", "di", "dan", "ini", "itu", "dari", "pada", "ke", "dengan", "untuk", "adalah", "juga", "oleh", "dalam", "tidak", "tersebut",
    "sebagai", "telah", "atau", "ada", "ia", "mereka", "kita", "akan", "dapat", "lebih", "bagi", "sejak", "karena", "namun", "serta",
    "bahwa", "hingga", "antara", "kemudian", "saat", "bila", "ketika", "setelah", "sebelum", "menjadi", "sudah", "belum", "sangat", "hanya",
    "pun", "pula", "atas", "bawah", "seperti", "sebuah", "salah", "satu", "dua", "tiga", "beberapa", "suatu", "para", "hal", "cara", "maka",
    "agar", "maupun", "selain", "yaitu", "yakni", "jika", "apabila", "meski", "walau", "walaupun", "meskipun", "sehingga", "tentang",
    "terhadap", "selama", "sekitar", "sesuai", "berdasarkan", "menurut", "mengenai", "melainkan", "daripada", "diantara", "oleh", "tahun",
    "abad", "a", "b", "c", "d", "e", "f", "masa", "nya", "mu", "ku", "si", "sang", "saja", "lah", "kah", "an", "baik", "lain", "lainnya",
    "setiap", "tiap", "banyak", "semua", "seluruh", "berbagai", "sejumlah"
}

def word_frequency(
  filepath=RESOURCE_DIR/"doc_2.txt",
  output=RESULTS_DIR/"b_kataunik.txt",
  top_n=30
):
  with open(filepath, "r", encoding="latin-1") as f:
    raw = f.read()

  raw = raw.lower()
  tokens = re.findall(r'\b[a-z]{2,}\b', raw)
  filtered = [tok for tok in tokens if tok not in STOPWORDS_ID]
  freq = Counter(filtered)
  top_words = freq.most_common(top_n)

  with open(output, "w", encoding="utf-8") as f:
    for word, count in top_words:
      f.write(f"{word}\t{count}\n")

  return top_words


# TASK C
def clean_subtitle(
  filepath=RESOURCE_DIR / "doc_3.srt",
  output=RESULTS_DIR / "c_subtitle.txt"
):
  with open(filepath, "r", encoding="utf-8") as f:
    raw = f.read()

  raw = raw.replace('\r\n', '\n').replace('\r', '\n')
  raw = re.sub(r'^\d+\s*$', '', raw, flags=re.MULTILINE)
  raw = re.sub(r'^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\s*$', '', raw, flags=re.MULTILINE)
  raw = re.sub(r'<[^>]+>', '', raw)
  raw = re.sub(r'\n{2,}', '\n', raw)
  raw = re.sub(
    r'^.*(Lebah|L\s*e\s*b\s*a\s*h|Iklan|Bisnis|Joinwin|Sbobet|Casino|Poker|Slot|IG\s*:|https?://\S+|\d{9,}|\d+\.\d+\.\d+\.\d+).*$',
    '', raw, flags=re.MULTILINE | re.IGNORECASE
  )

  lines = [line.strip() for line in raw.split('\n')]
  lines = [line for line in lines if line]

  with open(output, "w", encoding="utf-8") as f:
    f.write('\n'.join(lines) + '\n')

  return lines


if __name__ == "__main__":
  parse_references()
  word_frequency()
  clean_subtitle()