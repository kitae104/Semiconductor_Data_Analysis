// 공통 스크립트: 코드 복사 버튼, 맨 위로 이동, 진행률 표시줄
document.addEventListener("DOMContentLoaded", function () {
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
      title.appendChild(document.createTextNode("📑 "));
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
      desc.appendChild(document.createTextNode("📸 캡처 예정 — "));
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
      { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );
    revealTargets.forEach(function (el, i) {
      el.classList.add("reveal-init");
      el.style.transitionDelay = Math.min(i * 40, 160) + "ms";
      revealObserver.observe(el);
    });
  }
});
