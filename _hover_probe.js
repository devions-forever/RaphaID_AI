const { chromium } = require("playwright-core");
const URL = process.env.RH_URL || "http://localhost:8510";
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1500, height: 680 } });
  await p.goto(URL, { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 45000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) {}
  await p.waitForTimeout(2500);
  const measure = async function (tag) {
    const r = await p.evaluate(function () {
      const wrap = document.querySelector('[data-testid="stSidebarCollapseButton"]');
      const btn = wrap ? wrap.querySelector("button") : null;
      const box = function (el) { if (!el) return null; const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
      return {
        wrap: box(wrap),
        wrapDisplay: wrap ? getComputedStyle(wrap).display : null,
        wrapVis: wrap ? getComputedStyle(wrap).visibility : null,
        btn: box(btn),
        btnDisplay: btn ? getComputedStyle(btn).display : null,
        btnOpacity: btn ? getComputedStyle(btn).opacity : null,
        btnHTML: wrap ? wrap.innerHTML.slice(0, 120) : null,
      };
    });
    console.log(tag, JSON.stringify(r));
  };
  await measure("NO HOVER:");
  await p.mouse.move(150, 30);
  await p.waitForTimeout(900);
  await measure("HOVERED:");
  await b.close();
})();
