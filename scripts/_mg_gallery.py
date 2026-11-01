"""(임시) 모션 그래픽 점검용 갤러리 페이지 생성: python scripts/_mg_gallery.py 1 2 3"""
import re, sys, os
weeks = [int(a) for a in sys.argv[1:]] or [1]
figs = []
for w in weeks:
    h = open(f"lectures/week{w:02d}/index.html", encoding="utf-8").read()
    figs += re.findall(r'<figure class="mg">.*?</figure>', h, re.S)
rows = []
for i, f in enumerate(figs):
    rows.append(f'<div class="pair">{f}{f}</div>')
html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><link rel="stylesheet" href="../assets/css/common.css">
<style>body{{background:#fff;padding:8px}} .pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:6px}} .mg-ctrl,.illustration-note,figcaption{{display:none}} .mg{{margin:0}}</style></head><body>
{''.join(rows)}
<script>
const T = [{",".join(str(t) for t in [])}];
window.freeze = (a, b) => {{ document.querySelectorAll('.pair').forEach(p => {{ const [x, y] = p.querySelectorAll('.mg'); [[x, a], [y, b]].forEach(([el, ms]) => el.getAnimations({{subtree:true}}).forEach(an => {{ an.pause(); an.currentTime = ms; }})); }}); }};
</script></body></html>"""
open("_workspace/mg_gallery.html", "w", encoding="utf-8").write(html)
print(len(figs))
