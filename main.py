"""
* NIM_1 NAMA_1: peran_mahasiswa_1
* NIM_2 NAMA_2: peran_mahasiswa_2
* NIM_3 NAMA_3: peran_mahasiswa_3
* NIM_4 NAMA_4: peran_mahasiswa_4
"""

import re
import json
from pathlib import Path
from collections import Counter

# Resolve path relatif terhadap lokasi file main.py ini sendiri
# Jadi tidak peduli kamu run dari directory mana, path selalu benar
BASE_DIR = Path(__file__).parent          # → .../Tugas1/
RESOURCE_DIR = BASE_DIR / "resource"      # → .../Tugas1/resource/
RESULTS_DIR  = BASE_DIR / "results"       # → .../Tugas1/results/

# Buat folder results kalau belum ada
RESULTS_DIR.mkdir(exist_ok=True)


# =============================================================================
# TASK A
# =============================================================================

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
        if year_match:
            entry["year"] = year_match.group(1)

        title_match = re.search(r'"([^"]+)"', block)
        if title_match:
            entry["title"] = title_match.group(1).strip()
        else:
            no_quote_match = re.search(r'\(\d{4}\)\.\s+([^.]+)\.', block)
            if no_quote_match:
                title_candidate = no_quote_match.group(1).strip()
                title_candidate = re.sub(r'\s*\((?:PDF|Thesis)\)', '', title_candidate).strip()
                entry["title"] = title_candidate

        if year_match and '(' + year_match.group(1) + ')' in block:
            before_year = block[:block.index('(' + year_match.group(1) + ')')].strip()
            before_year = re.sub(r'[.,\s]+$', '', before_year)
            if before_year:
                entry["authors"] = before_year
        else:
            author_match = re.match(r'^([^".\n]+?)(?:\.\s+"|\s+")', block)
            if author_match:
                entry["authors"] = author_match.group(1).strip()
            else:
                author_fallback = re.match(r'^([^.]+)\.', block)
                if author_fallback:
                    cand = author_fallback.group(1).strip()
                    if re.search(r'[A-Z]', cand):
                        entry["authors"] = cand

        if entry.get("title") or entry.get("authors"):
            results.append(entry)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"[Task A] Selesai: {len(results)} referensi → {output}")
    return results


# =============================================================================
# TASK B
# =============================================================================

STOPWORDS_ID = {
    "yang", "di", "dan", "ini", "itu", "dari", "pada", "ke", "dengan",
    "untuk", "adalah", "juga", "oleh", "dalam", "tidak", "tersebut",
    "sebagai", "telah", "atau", "ada", "ia", "mereka", "kita", "akan",
    "dapat", "lebih", "bagi", "sejak", "karena", "namun", "serta",
    "bahwa", "hingga", "antara", "kemudian", "saat", "bila", "ketika",
    "setelah", "sebelum", "menjadi", "sudah", "belum", "sangat", "hanya",
    "pun", "pula", "atas", "bawah", "seperti", "sebuah", "salah", "satu",
    "dua", "tiga", "beberapa", "suatu", "para", "hal", "cara", "maka",
    "agar", "maupun", "selain", "yaitu", "yakni", "jika", "apabila",
    "meski", "walau", "walaupun", "meskipun", "sehingga", "tentang",
    "terhadap", "selama", "sekitar", "sesuai", "berdasarkan", "menurut",
    "mengenai", "melainkan", "daripada", "diantara", "oleh", "tahun",
    "abad", "a", "b", "c", "d", "e", "f", "masa", "nya", "mu", "ku",
    "si", "sang", "saja", "lah", "kah", "an", "baik", "lain", "lainnya",
    "setiap", "tiap", "banyak", "semua", "seluruh", "berbagai", "sejumlah"
}

def word_frequency(
    filepath=RESOURCE_DIR / "doc_2.txt",
    output=RESULTS_DIR / "b_kataunik.txt",
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

    print(f"[Task B] Selesai: top {top_n} kata → {output}")
    return top_words


# =============================================================================
# TASK C
# =============================================================================

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
        r'^.*(Iklan|Bisnis|Joinwin|Sbobet|Casino|Poker|Slot|\d{9,}|\d+\.\d+\.\d+\.\d+).*$',
        '', raw, flags=re.MULTILINE | re.IGNORECASE
    )

    lines = [line.strip() for line in raw.split('\n')]
    lines = [line for line in lines if line]

    with open(output, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines) + '\n')

    print(f"[Task C] Selesai: {len(lines)} baris dialog → {output}")
    return lines


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("NLP Task 1 — Pemrosesan Bahasa Alami")
    print("=" * 50)

    parse_references()
    word_frequency()
    clean_subtitle()

    print("=" * 50)
    print("Semua task selesai.")