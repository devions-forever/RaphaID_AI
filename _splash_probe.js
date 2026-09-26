const { chromium } = require("playwright-core");

(async () => {
  const b = await chromium.launch({
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
    headless: true,
  });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto("http://localhost:8503", { waitUntil: "domcontentloaded" });
  try {
    await p.waitForSelector(".raphaid-splash-root", { timeout: 20000 });
  } catch (e) {
    console.log("no splash:", e.message);
    await b.close();
    return;
  }
  await p.waitForTimeout(900);

  const info = await p.evaluate(function () {
    const root = document.querySelector(".raphaid-splash-root");
    if (!root) return { error: "root missing" };
    const cs = getComputedStyle(root);
    const kids = [];
    for (let i = 0; i < root.children.length; i++) {
      const c = root.children[i];
      const r = c.getBoundingClientRect();
      kids.push({
        tag: c.tagName,
        cls: c.className,
        w: Math.round(r.width),
        h: Math.round(r.height),
        x: Math.round(r.x),
        y: Math.round(r.y),
        disp: getComputedStyle(c).display,
      });
    }
    const pr = root.getBoundingClientRect();
    return {
      root: {
        display: cs.display,
        flexDirection: cs.flexDirection,
        alignItems: cs.alignItems,
        justifyContent: cs.justifyContent,
        position: cs.position,
        w: Math.round(pr.width),
        h: Math.round(pr.height),
        x: Math.round(pr.x),
        y: Math.round(pr.y),
        parentTag: root.parentElement ? root.parentElement.tagName : null,
        parentTestId: root.parentElement ? root.parentElement.getAttribute("data-testid") : null,
        parentDisp: root.parentElement ? getComputedStyle(root.parentElement).display : null,
      },
      children: kids.slice(0, 14),
    };
  });

  console.log(JSON.stringify(info, null, 2));
  await b.close();
})();
