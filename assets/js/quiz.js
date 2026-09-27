// 정답·체크포인트 보기 토글 — 버튼 글자의 "보기"를 "숨기기"로 바꿔 쓴다("체크포인트 보기" ↔ "체크포인트 숨기기")
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".reveal-btn").forEach(function (btn) {
    var label = btn.textContent;
    btn.addEventListener("click", function () {
      var box = btn.nextElementSibling;
      if (!box || !box.classList.contains("answer-box")) return;
      var shown = box.classList.toggle("shown");
      btn.textContent = shown ? label.replace("보기", "숨기기") : label;
    });
  });
});
