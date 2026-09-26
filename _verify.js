const { chromium } = require("playwright-core");
const URL = process.env.RH_URL || "http://localhost:8512";
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto(URL, { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 45000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) { console.log("no topbar"); }
  await p.waitForTimeout(2500);
  await p.screenshot({ path: "ui_shots/30_expanded.png" });

  const expanded = await p.evaluate(function () {
    const cc = document.querySelector('[data-testid="stSidebarCollapsedControl"]');
    const tb = document.querySelector(".rh-topbar");
    const r = tb.getBoundingClientRect();
    const items = [].slice.call(tb.querySelectorAll(".rh-topbar-group"));
    const spans = items.map(function (g) { const rr = g.getBoundingClientRect(); return [Math.round(rr.x), Math.round(rr.x + rr.width)]; });
    return {
      topbarRect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
      groupSpans: spans,
      collapsedControl: cc ? { rect: (function (x) { return [Math.round(x.x), Math.round(x.y), Math.round(x.width), Math.round(x.height)]; })(cc.getBoundingClientRect()), z: getComputedStyle(cc).zIndex } : "absent",
    };
  });
  console.log("EXPANDED:", JSON.stringify(expanded));

  // sticky
  await p.evaluate(function () { const m = document.querySelector('[data-testid="stMain"]'); if (m) m.scrollTop = 700; });
  await p.waitForTimeout(600);
  const y = await p.evaluate(function () { const el = document.querySelector(".rh-topbar"); return el ? Math.round(el.getBoundingClientRect().y) : null; });
  console.log("STICKY y after scroll:", y);
  await p.screenshot({ path: "ui_shots/31_scrolled.png" });

  // collapse
  await p.evaluate(function () {
    const cands = document.querySelectorAll('[data-testid*="ollaps"]');
    for (let i = 0; i < cands.length; i++) { if (cands[i].tagName === "BUTTON") { cands[i].click(); return; } }
  });
  await p.waitForTimeout(2500);
  await p.screenshot({ path: "ui_shots/32_collapsed.png" });
  const coll = await p.evaluate(function () {
    const cc = document.querySelector('[data-testid="stSidebarCollapsedControl"]');
    const tb = document.querySelector(".rh-topbar");
    const r = tb.getBoundingClientRect();
    return { topbarRect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
             padLeft: getComputedStyle(tb).paddingLeft,
             ccRect: cc ? [Math.round(cc.getBoundingClientRect().x), Math.round(cc.getBoundingClientRect().y)] : null };
  });
  console.log("COLLAPSED:", JSON.stringify(coll));
  await b.close();
})();
