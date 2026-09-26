const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto(process.env.RH_URL || "http://localhost:8508", { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 40000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) {}
  await p.waitForTimeout(2500);
  const dump = async function (label) {
    const r = await p.evaluate(function () {
      const el = document.querySelector('[data-testid="stSidebarCollapsedControl"]');
      if (!el) return "ABSENT";
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      let par = el.parentElement, chain = [];
      for (let i = 0; i < 4 && par; i++) { chain.push(par.tagName + "[" + (par.getAttribute("data-testid") || "") + "]"); par = par.parentElement; }
      return {
        rect: [Math.round(rect.x), Math.round(rect.y), Math.round(rect.width), Math.round(rect.height)],
        display: cs.display, visibility: cs.visibility, opacity: cs.opacity,
        position: cs.position, z: cs.zIndex, transform: cs.transform,
        parentChain: chain,
        sidebarExpanded: (document.querySelector('[data-testid="stSidebar"]') || {}).getAttribute ? document.querySelector('[data-testid="stSidebar"]').getAttribute("aria-expanded") : null,
      };
    });
    console.log(label, JSON.stringify(r, null, 1));
  };
  await dump("EXPANDED:");
  await p.evaluate(function () {
    const cands = document.querySelectorAll('[data-testid*="ollaps"] button, [data-testid*="ollaps"]');
    for (let i = 0; i < cands.length; i++) { if (cands[i].tagName === "BUTTON") { cands[i].click(); return; } }
  });
  await p.waitForTimeout(2500);
  await dump("COLLAPSED:");
  await b.close();
})();
