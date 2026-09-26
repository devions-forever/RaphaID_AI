const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto(process.env.RH_URL || "http://localhost:8507", { waitUntil: "domcontentloaded" });
  await p.waitForTimeout(6000);
  const r = await p.evaluate(function () {
    const el = document.querySelector('[data-testid="stSidebarCollapsedControl"]');
    if (!el) return "ABSENT";
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return { rect: [Math.round(rect.x), Math.round(rect.y), Math.round(rect.width), Math.round(rect.height)],
             display: cs.display, visibility: cs.visibility, opacity: cs.opacity,
             position: cs.position, transform: cs.transform, z: cs.zIndex };
  });
  console.log("PLAIN APP control:", JSON.stringify(r, null, 1));
  await b.close();
})();
