const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1200, height: 800 } });
  await p.goto("http://localhost:8504", { waitUntil: "networkidle" });
  await p.waitForTimeout(4000);
  const out = await p.evaluate(function () {
    const res = {};
    ["t1", "t2", "t3", "t4"].forEach(function (id) {
      const el = document.getElementById(id);
      res[id] = el ? { style: el.getAttribute("style"), disp: getComputedStyle(el).display } : "MISSING";
    });
    return res;
  });
  console.log(JSON.stringify(out, null, 2));
  await b.close();
})();
