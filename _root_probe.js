const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto("http://localhost:8503", { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { timeout: 20000 }); } catch (e) { console.log("no splash"); await b.close(); return; }
  await p.waitForTimeout(900);
  const out = await p.evaluate(function () {
    const root = document.querySelector(".raphaid-splash-root");
    const cs = getComputedStyle(root);
    const r = root.getBoundingClientRect();
    return {
      inlineStyleAttr: (root.getAttribute("style") || "").slice(0, 200),
      display: cs.display,
      flexDirection: cs.flexDirection,
      alignItems: cs.alignItems,
      justifyContent: cs.justifyContent,
      position: cs.position,
      width: cs.width,
      height: cs.height,
      rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
      parentTestId: root.parentElement ? root.parentElement.getAttribute("data-testid") : null,
      parentClass: root.parentElement ? root.parentElement.className : null,
      parentDisplay: root.parentElement ? getComputedStyle(root.parentElement).display : null,
      parentOverflow: root.parentElement ? getComputedStyle(root.parentElement).overflow : null,
    };
  });
  console.log(JSON.stringify(out, null, 2));
  await b.close();
})();
