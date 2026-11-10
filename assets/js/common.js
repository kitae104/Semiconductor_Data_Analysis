// 공통 스크립트: 파이썬 코드 색칠, 코드 복사 버튼, 맨 위로 이동, 진행률 표시줄

// 파이썬 코드 색칠(VS Code 느낌). 글자는 그대로 두고 <span class="tok-…">로만 감싼다.
// 라벨이 "Python"으로 시작하는 .code-block 의 코드만 대상으로 한다(ChatGPT 질문 상자는 제외).
var PY_CONTROL = /^(?:if|elif|else|for|while|in|not|and|or|is|return|import|from|as|with|try|except|finally|raise|break|continue|pass|yield|assert|del|global|nonlocal|await|async)$/;
var PY_DEF = /^(?:def|class|lambda)$/;
var PY_CONST = /^(?:True|False|None)$/;
var PY_BUILTIN = /^(?:print|len|range|int|float|str|bool|list|dict|set|tuple|round|sum|min|max|abs|sorted|reversed|enumerate|zip|map|filter|type|isinstance|input|open|any|all|format|repr|id)$/;
var PY_TOKEN = new RegExp([
  "(#[^\\n]*)",                                                   // 1 주석
  "((?:[fFrRbBuU]{1,2})?(?:\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?'''|\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*'))", // 2 문자열
  "(\\b\\d+(?:\\.\\d+)?(?:[eE][+-]?\\d+)?\\b|\\.\\d+)",           // 3 숫자
  "(_{2,})",                                                      // 4 빈칸 표시 ____
  "([A-Za-z_\\uAC00-\\uD7A3][A-Za-z0-9_\\uAC00-\\uD7A3]*)",       // 5 이름
  "([+\\-*/%=<>!&|^~]+)"                                          // 6 연산자
].join("|"), "g");

function pySpan(cls, text) {
  var s = document.createElement("span");
  s.className = "tok-" + cls;
  s.textContent = text;
  return s;
}

function pyHighlight(src) {
  var frag = document.createDocumentFragment();
  var last = 0, prevWord = "", prevChar = "", m;
  PY_TOKEN.lastIndex = 0;
  while ((m = PY_TOKEN.exec(src)) !== null) {
    if (m.index > last) {
      var gap = src.slice(last, m.index);
      frag.appendChild(document.createTextNode(gap));
      var trimmed = gap.replace(/\s+$/, "");
      if (trimmed) { prevChar = trimmed.charAt(trimmed.length - 1); prevWord = ""; }
    }
    var tok = m[0];
    if (m[1] !== undefined) {
      frag.appendChild(pySpan("comment", tok));
    } else if (m[2] !== undefined) {
      if (/^[fF]|^[rRbBuU][fF]/.test(tok)) {
        // f-string: {표현식} 부분은 따로 색을 준다
        tok.split(/(\{\{|\}\}|\{[^{}\n]*\})/).forEach(function (part) {
          if (!part) return;
          if (part.charAt(0) === "{" && part !== "{{") frag.appendChild(pySpan("fexpr", part));
          else frag.appendChild(pySpan("string", part));
        });
      } else {
        frag.appendChild(pySpan("string", tok));
      }
    } else if (m[3] !== undefined) {
      frag.appendChild(pySpan("number", tok));
    } else if (m[4] !== undefined) {
      frag.appendChild(pySpan("blank", tok));
    } else if (m[5] !== undefined) {
      var after = src.charAt(PY_TOKEN.lastIndex);
      var cls = null;
      if (prevChar !== "." && PY_DEF.test(tok)) cls = "def";
      else if (prevChar !== "." && PY_CONTROL.test(tok)) cls = "control";
      else if (prevChar !== "." && PY_CONST.test(tok)) cls = "const";
      else if (prevWord === "def") cls = "func";
      else if (prevWord === "class") cls = "class";
      else if (after === "(") cls = (prevChar === "." || !PY_BUILTIN.test(tok)) ? "func" : "builtin";
      else if (prevChar === ".") cls = "attr";
      else cls = "var";
      frag.appendChild(pySpan(cls, tok));
      prevWord = tok;
    } else {
      frag.appendChild(pySpan("op", tok));
      prevWord = "";
    }
    if (m[5] === undefined) prevWord = "";
    prevChar = m[5] !== undefined ? "a" : tok.charAt(tok.length - 1);
    last = PY_TOKEN.lastIndex;
  }
  if (last < src.length) frag.appendChild(document.createTextNode(src.slice(last)));
  return frag;
}

document.addEventListener("DOMContentLoaded", function () {
  // 파이썬 코드 색칠
  document.querySelectorAll(".code-block").forEach(function (block) {
    var label = block.querySelector(".code-label");
    var codeEl = block.querySelector("pre code");
    if (!label || !codeEl || !/^\s*Python/.test(label.textContent)) return;
    var src = codeEl.textContent;
    codeEl.textContent = "";
    codeEl.appendChild(pyHighlight(src));
    codeEl.classList.add("py-highlighted");
  });

  // 코드 블록 복사 버튼
  document.querySelectorAll(".code-block").forEach(function (block) {
    var btn = block.querySelector(".copy-btn");
    var codeEl = block.querySelector("pre code");
    if (!btn || !codeEl) return;
    btn.addEventListener("click", function () {
      var text = codeEl.innerText;
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "복사됨!";
        btn.classList.add("copied");
        setTimeout(function () {
          btn.textContent = "복사";
          btn.classList.remove("copied");
        }, 1500);
      }).catch(function () {
        btn.textContent = "복사 실패";
      });
    });
  });

  // 맨 위로 이동 버튼
  var topBtn = document.getElementById("backToTop");
  if (topBtn) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 400) {
        topBtn.classList.add("show");
      } else {
        topBtn.classList.remove("show");
      }
    });
    topBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // 진행률 표시줄: 현재 주차 번호 / 전체 10주
  var progressFill = document.getElementById("progressFill");
  if (progressFill) {
    var week = parseInt(progressFill.getAttribute("data-week"), 10) || 0;
    var pct = Math.min(100, Math.round((week / 10) * 100));
    progressFill.style.width = pct + "%";
  }

  // 이 차시 목차(TOC): 강의/실습지 페이지(주차 내비게이션이 있는 페이지)에서
  // section.block > h2를 모아 클릭 시 해당 섹션으로 부드럽게 이동하는 목차를 자동 생성한다.
  var weekNav = document.querySelector(".week-nav");
  var heroEl = document.querySelector(".hero, .hero-home");
  if (weekNav && heroEl) {
    var tocSections = Array.prototype.filter.call(
      document.querySelectorAll("main.page > section.block"),
      function (sec) { return sec.querySelector("h2"); }
    );
    if (tocSections.length >= 4) {
      var toc = document.createElement("nav");
      toc.className = "toc-box";
      toc.setAttribute("aria-label", "이 페이지 목차");

      var head = document.createElement("div");
      head.className = "toc-head";

      var title = document.createElement("span");
      title.className = "toc-title";
      var titleText = document.createElement("span");
      titleText.textContent = "이 페이지 목차";
      title.appendChild(titleText);
      head.appendChild(title);

      var toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = "toc-toggle";
      toggle.setAttribute("aria-label", "목차 접기/펼치기");
      toggle.textContent = "❮";
      head.appendChild(toggle);

      toc.appendChild(head);

      var TOC_KEY = "tocCollapsed";
      function applyCollapsed(collapsed) {
        toc.classList.toggle("collapsed", collapsed);
        toggle.textContent = collapsed ? "❯" : "❮";
      }
      toggle.addEventListener("click", function () {
        var collapsed = !toc.classList.contains("collapsed");
        applyCollapsed(collapsed);
        try { localStorage.setItem(TOC_KEY, collapsed ? "1" : "0"); } catch (e) {}
      });
      try {
        applyCollapsed(localStorage.getItem(TOC_KEY) === "1");
      } catch (e) {}

      var list = document.createElement("div");
      list.className = "toc-list";
      tocSections.forEach(function (sec, i) {
        if (!sec.id) sec.id = "sec-" + (i + 1);
        var h2 = sec.querySelector("h2");
        var a = document.createElement("a");
        a.href = "#" + sec.id;
        a.textContent = h2.textContent.trim();
        list.appendChild(a);
      });
      toc.appendChild(list);

      // 목차를 왼쪽 사이드바로 배치하기 위해 hero 이후의 모든 형제 요소를
      // 본문 래퍼(.page-content)로 옮기고, 목차와 나란히 2단 레이아웃(.page-body)을 구성한다.
      // hero가 .hero-with-stats 같은 래퍼 안에 있을 수 있으므로, main.page의 직계 자식을
      // 기준으로 "히어로가 속한 블록"을 찾아 그 다음 형제부터 옮긴다.
      var pageMain = document.querySelector("main.page");
      var heroBlock = heroEl;
      while (heroBlock && heroBlock.parentElement !== pageMain) {
        heroBlock = heroBlock.parentElement;
      }
      if (!heroBlock) heroBlock = heroEl;
      var body = document.createElement("div");
      body.className = "page-body";
      var content = document.createElement("div");
      content.className = "page-content";

      var node = heroBlock.nextSibling;
      while (node) {
        var next = node.nextSibling;
        content.appendChild(node);
        node = next;
      }

      body.appendChild(toc);
      body.appendChild(content);
      pageMain.appendChild(body);
    }
  }

  // 캡처 이미지 자리: <img data-shot="캡처할 화면 설명"> 파일이 아직 없으면
  // 점선 상자(.photo-slot)로 바꿔 "무엇을, 어떤 파일명으로" 저장하면 되는지 보여준다.
  // 해당 경로에 이미지를 저장하면 HTML 수정 없이 새로고침만으로 이미지가 표시된다.
  document.querySelectorAll("img[data-shot]").forEach(function (img) {
    function showSlot() {
      if (!img.parentNode) return;
      var slot = document.createElement("div");
      slot.className = "photo-slot";
      var desc = document.createElement("div");
      desc.appendChild(document.createTextNode("캡처 예정 — "));
      var b = document.createElement("b");
      b.textContent = img.getAttribute("data-shot");
      desc.appendChild(b);
      slot.appendChild(desc);
      var file = document.createElement("code");
      var src = img.getAttribute("src") || "";
      var idx = src.indexOf("assets/");
      file.textContent = idx >= 0 ? src.slice(idx) : src;
      slot.appendChild(document.createTextNode("저장 위치: "));
      slot.appendChild(file);
      img.parentNode.replaceChild(slot, img);
    }
    if (img.complete && img.naturalWidth === 0) {
      showSlot();
    } else {
      img.addEventListener("error", showSlot);
    }
  });

  // 스크롤 등장 애니메이션: section.block / .hero / .hero-home이 화면에 들어오면 서서히 나타남
  if ("IntersectionObserver" in window) {
    var revealTargets = document.querySelectorAll("section.block, .hero, .hero-home");
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("revealed");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0, rootMargin: "0px 0px -40px 0px" }  // 아주 긴 섹션(PART 2 등)도 보이기 시작하면 나타나게 한다
    );
    revealTargets.forEach(function (el, i) {
      el.classList.add("reveal-init");
      el.style.transitionDelay = Math.min(i * 40, 160) + "ms";
      revealObserver.observe(el);
    });
  }
});

// 모션 그래픽(.mg): 화면에 보일 때만 재생하고, 멈춤·처음부터 버튼을 붙인다
document.addEventListener("DOMContentLoaded", function () {
  var figs = document.querySelectorAll(".mg");
  if (!figs.length) return;
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { en.target.classList.toggle("mg-run", en.isIntersecting); });
  }, { threshold: 0.25 }) : null;
  figs.forEach(function (fig) {
    fig.classList.add("mg-js");
    if (io) io.observe(fig); else fig.classList.add("mg-run");
    var bar = document.createElement("div");
    bar.className = "mg-ctrl";
    var pause = document.createElement("button");
    pause.type = "button"; pause.className = "mg-btn"; pause.textContent = "멈춤";
    pause.addEventListener("click", function () {
      var paused = fig.classList.toggle("mg-paused");
      pause.textContent = paused ? "재생" : "멈춤";
    });
    var again = document.createElement("button");
    again.type = "button"; again.className = "mg-btn"; again.textContent = "처음부터";
    again.addEventListener("click", function () {
      fig.classList.add("mg-restart");
      void fig.offsetWidth;
      fig.classList.remove("mg-restart", "mg-paused");
      pause.textContent = "멈춤";
    });
    bar.appendChild(pause); bar.appendChild(again);
    var cap = fig.querySelector("figcaption");
    fig.insertBefore(bar, cap || null);
  });
});
