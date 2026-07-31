// 퀴즈 정답 보기 토글
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".reveal-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = btn.nextElementSibling;
      if (!box || !box.classList.contains("answer-box")) return;
      var shown = box.classList.toggle("shown");
      btn.textContent = shown ? "정답 숨기기" : "정답 보기";
    });
  });
});
