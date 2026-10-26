"""Lighthouse JSON raporlarının kısa özeti. Kullanım: python lh_ozet.py <rapor-klasörü>"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.json"))):
    r = json.load(open(f, encoding="utf-8"))
    a = r["audits"]
    k = r["categories"]
    print(f"===== {os.path.basename(f)}  ({r['finalDisplayedUrl']})")
    print("  puanlar: " + "  ".join(f"{c}: {round((k[c]['score'] or 0) * 100)}" for c in k))
    print("  ölçümler: " + "  ".join(f"{m}: {a[m]['displayValue']}" for m in
                                      ("first-contentful-paint", "largest-contentful-paint", "total-blocking-time",
                                       "cumulative-layout-shift", "speed-index") if m in a))
    lcp = a.get("largest-contentful-paint-element", {}).get("details", {})
    try:
        el = lcp["items"][0]["items"][0]["node"]
        print("  en büyük öğe (LCP):", el.get("nodeLabel", "")[:80], "|", el.get("selector", "")[:70])
        faz = lcp["items"][1]["items"]
        print("  LCP dağılımı: " + ", ".join(f"{x['phase']}: {round(x['timing'])} ms" for x in faz))
    except (KeyError, IndexError):
        pass
    print("  ağırlık:", a.get("total-byte-weight", {}).get("displayValue", "?"))
    firsat = [(x["id"], x["title"], x.get("displayValue", ""), x["details"].get("overallSavingsMs", 0))
              for x in a.values() if x.get("details", {}).get("type") == "opportunity"
              and (x.get("score") is not None and x["score"] < 0.9)]
    for i, t, d, ms in sorted(firsat, key=lambda z: -z[3])[:6]:
        print(f"  fırsat: {t} {d} (~{round(ms)} ms)")
    for c in ("seo", "accessibility", "best-practices"):
        for ref in k[c]["auditRefs"]:
            x = a[ref["id"]]
            if x.get("score") is not None and x["score"] < 1 and ref.get("weight", 0) > 0:
                print(f"  {c} sorunu: {x['title']}")
