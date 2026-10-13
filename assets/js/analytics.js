/* 방문자 통계(GoatCounter). 사이트 코드는 아래 한 곳에서만 바꾼다. */
(function () {
    var SITE_CODE = "semiconductor-data-analysis";

    var host = location.hostname;
    if (location.protocol === "file:" || host === "localhost" || host === "127.0.0.1") {
        return;
    }

    var s = document.createElement("script");   
    s.async = true;
    s.src = "https://gc.zgo.at/count.js";
    s.setAttribute("data-goatcounter", "https://" + SITE_CODE + ".goatcounter.com/count");
    document.head.appendChild(s);
})();
