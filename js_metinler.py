# JS dosyalarında kullanıcıya görünen ve henüz çevrilmemiş Türkçe metinleri listeler
# (yorum satırları ve T('Türkçe', 'English') ile yazılmış satırlar hariç).
import re
import sys

for yol in sys.argv[1:]:
    print("=====", yol)
    yorum = False
    for i, satir in enumerate(open(yol, encoding="utf-8"), 1):
        t = satir.strip()
        if yorum:
            if "*/" in t:
                yorum = False
            continue
        if t.startswith("/*") and "*/" not in t:
            yorum = True
            continue
        if t.startswith(("//", "*", "/*")):
            continue
        kod = re.sub(r"//.*$", "", t)
        if re.search(r"\bT\(", kod):
            continue
        if re.search(r"[çğıöşüÇĞİÖŞÜ]", kod) and re.search(r"['\"`]", kod):
            print(f"{i}: {kod[:170]}")
