const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto(process.env.RH_URL || "http://localhost:8508", { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 40000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) {}
  await p.waitForTimeout(2500);
  await p.screenshot({ path: "ui_shots/10_expanded_full.png" });
  const extra = await p.evaluate(function () {
    const out = [];
    const all = document.querySelectorAll("button");
    for (let i = 0; i < all.length; i++) {
      const r = all[i].getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const cs = getComputedStyle(all[i]);
      let par = all[i].parentElement, tid = null;
      for (let d = 0; d < 4 && par; d++) { const t = par.getAttribute("data-testid"); if (t) { tid = t; break; } par = par.parentElement; }
      out.push({ kind: all[i].getAttribute("kind"), parentTestId: tid, rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)], z: cs.zIndex, pos: cs.position, disp: cs.display, vis: cs.visibility });
    }
    return out;
  });
  console.log(JSON.stringify(extra, null, 2));
  await b.close();
})();
