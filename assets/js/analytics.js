/* 방문자 통계(GoatCounter). 사이트 코드는 아래 한 곳에서만 바꾼다.
   count.js는 외부 도메인 대신 같은 폴더의 사본(assets/js/count.js, ISC 라이선스)을 쓴다. */
(function () {
    var SITE_CODE = "semiconductor-data-analysis";
    var BASE = "https://" + SITE_CODE + ".goatcounter.com";

    var host = location.hostname;
    var isLocal = location.protocol === "file:" || host === "localhost" || host === "127.0.0.1";

    // 1) 방문 기록 (로컬 확인 중에는 집계하지 않는다)
    if (!isLocal) {
        var s = document.createElement("script");
        s.async = true;
        s.src = document.currentScript.src.replace(/analytics\.js(\?.*)?$/, "count.js");
        s.setAttribute("data-goatcounter", BASE + "/count");
        document.head.appendChild(s);
    }

    // 2) 전체/오늘 방문 수 표시: #visitStats 요소가 있는 페이지에서만
    var box = document.getElementById("visitStats");
    if (!box) return;

    function pad(n) { return (n < 10 ? "0" : "") + n; }
    var d = new Date();
    var today = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());

    function load(query) {
        return fetch(BASE + "/counter/TOTAL.json" + query).then(function (r) {
            if (!r.ok) throw new Error(r.status);
            return r.json();
        });
    }

    Promise.all([load(""), load("?start=" + today + "&end=" + today)])
        .then(function (res) {
            box.textContent = "전체 방문 " + res[0].count + " · 오늘 " + res[1].count;
            box.hidden = false;
        })
        .catch(function () { /* 통계를 못 가져오면 조용히 숨긴 채 둔다 */ });
})();
