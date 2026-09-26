const { chromium } = require("playwright-core");

(async () => {
  const b = await chromium.launch({
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
    headless: true,
  });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto("http://localhost:8503", { waitUntil: "domcontentloaded" });
  try {
    await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 30000 });
  } catch (e) {
    console.log("splash wait:", e.message);
  }
  await p.waitForTimeout(3000);

  const hits = await p.evaluate(function () {
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) {
      const t = n.nodeValue || "";
      if (t.indexOf("<div") >= 0 || t.indexOf("</div>") >= 0 || t.indexOf("rgba(") >= 0) {
        const el = n.parentElement;
        const path = [];
        let e = el;
        for (let i = 0; i < 6 && e; i++) {
          const tid = e.getAttribute ? e.getAttribute("data-testid") : null;
          path.push(e.tagName.toLowerCase() + (tid ? "[" + tid + "]" : ""));
          e = e.parentElement;
        }
        out.push({ path: path.join(" < "), head: t.slice(0, 130).replace(/\s+/g, " ") });
      }
    }
    return out.slice(0, 10);
  });

  console.log(JSON.stringify(hits, null, 2));
  await b.close();
})();
