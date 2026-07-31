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
});
