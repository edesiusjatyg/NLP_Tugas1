"""
* 245150200111021 Edesius Jaty Giovanni: Task B
* 245150207111053 Alia Atikah Sana: Task B
* 245150200111055 CHRISTIANO ALFONSIUS PURBA: Task A
* 245150200111060 DAMAR TYAGA WISTARA: Task C
* 245150200111058 Luthfi Pratama Sahni: Task C
"""

import re
import json
import os
from collections import Counter

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

# TASK A
def parsing_a():
  filepath=os.path.join(BASE_DIR, "resource/doc_1.txt")
  output=os.path.join(BASE_DIR, "results/a_judul.json")

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
      year_match = re.search(r'\b((19|20)\d{2})\b', block)
    if not year_match:
      year_match = re.search(r'(?<=[A-Za-z])((19|20)\d{2})\b', block)
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

    if year_match and '('+year_match.group(1)+')' in block:
      before_year = block[:block.index('('+year_match.group(1)+')')].strip()
      before_year = before_year.strip().rstrip('.,')
      entry["authors"] = before_year
    else:
      author_match = re.match(r'^([^.\n]+?)\.', block)
      if author_match:
        cand = author_match.group(1).strip()
        if cand and 'http' not in cand:
          entry["authors"] = cand
    
    # buat handle kasus index 13 (URL)
    if not entry.get("title") and not entry.get("authors"):
      entry["title"] = block.strip()
    if entry.get("title") or entry.get("authors"):
      results.append(entry)

  with open(output, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

  return results


# TASK B
def word_freq():
  filepath=os.path.join(BASE_DIR, "resource/doc_2.txt")
  stopwords_file=os.path.join(BASE_DIR, "resource/indonesian-stopwords-complete.txt")
  output=os.path.join(BASE_DIR, "results/b_kataunik.txt")
  top_n=30

  with open(stopwords_file, "r", encoding="utf-8") as f:
    stopwords = set(line.strip().lower() for line in f if line.strip())

  with open(filepath, "r", encoding="latin-1") as f:
    raw = f.read()

  raw = raw.lower()
  tokens = re.findall(r'\b[a-z]{2,}\b', raw)
  filtered = [tok for tok in tokens if tok not in stopwords]
  freq = Counter(filtered)
  top_words = freq.most_common(top_n)

  with open(output, "w", encoding="utf-8") as f:
    for word, count in top_words:
      f.write(f"{word}\t{count}\n")

  return top_words


# TASK C
def subtitle_cleaning():
  filepath=os.path.join(BASE_DIR, "resource/doc_3.srt")
  output=os.path.join(BASE_DIR, "results/c_subtitle.txt")

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
  parsing_a()
  word_freq()
  subtitle_cleaning()