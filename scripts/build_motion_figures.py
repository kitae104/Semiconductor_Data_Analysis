"""강의 HTML에 모션 그래픽(<figure class="mg">)을 넣는다. 여러 번 실행해도 같은 결과(멱등)다.

각 그림은 scripts/motion_figures/wNN.py 의 FIGS = [(제목 앵커, 그림)] 에 정의한다.
앵커 제목(h2/h3) 바로 뒤의 첫 단락(<p> 또는 <ul>) 다음에 <!-- mg:id --> ... <!-- /mg:id --> 로 감싸 넣는다.
사용: python scripts/build_motion_figures.py [--week N]
"""
import argparse
import importlib
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))


def find_block_end(html, pos):
    """pos 이후 첫 요소(p/ul/div)의 닫는 태그 끝 위치를 돌려준다."""
    m = re.compile(r"\s*<(p|ul|div)\b", re.S).match(html, pos)
    if not m:
        return pos
    tag = m.group(1)
    depth, i = 0, m.start(1) - 1
    pat = re.compile(rf"<(/?){tag}\b[^>]*>")
    for mm in pat.finditer(html, i):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            return mm.end()
    raise RuntimeError(f"닫는 </{tag}>를 찾지 못함")


def inject(html, anchor, block, fid):
    nl = "\r\n" if "\r\n" in html else "\n"
    html = re.sub(rf"[ \t]*<!-- mg:{re.escape(fid)} -->.*?<!-- /mg:{re.escape(fid)} -->(?:\r?\n)?", "", html, flags=re.S)
    hs = [m for m in re.finditer(r"<h([23])\b[^>]*>(.*?)</h\1>", html, re.S) if anchor in re.sub(r"<[^>]+>", "", m.group(2))]
    if len(hs) != 1:
        raise RuntimeError(f"앵커 '{anchor}' 일치 {len(hs)}건")
    end = find_block_end(html, hs[0].end())
    text = nl.join("  " + ln if ln else ln for ln in block.split("\n"))
    return html[:end] + nl + nl + text + nl + html[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int)
    args = ap.parse_args()
    total = 0
    for w in range(1, 11):
        if args.week and w != args.week:
            continue
        try:
            mod = importlib.import_module(f"motion_figures.w{w:02d}")
        except ModuleNotFoundError:
            continue
        path = os.path.join(BASE, "lectures", f"week{w:02d}", "index.html")
        with open(path, encoding="utf-8", newline="") as f:
            html = f.read()
        for anchor, fig in mod.FIGS:
            html = inject(html, anchor, fig.html(), fig.fid)
            total += 1
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(html)
        print(f"week{w:02d}: 그림 {len(mod.FIGS)}개")
    print(f"완료: {total}개")


if __name__ == "__main__":
    main()
