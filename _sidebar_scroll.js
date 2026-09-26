const { chromium } = require("playwright-core");
const URL = process.env.RH_URL || "http://localhost:8510";
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1500, height: 680 } });
  await p.goto(URL, { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 45000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) {}
  await p.waitForTimeout(2500);
  await p.screenshot({ path: "ui_shots/40_sidebar_top.png", clip: { x: 0, y: 0, width: 330, height: 680 } });

  const before = await p.evaluate(function () {
    const h = document.querySelector('[data-testid="stSidebarHeader"]');
    const btn = document.querySelector('[data-testid="stSidebarCollapseButton"] button');
    const c = document.querySelector('[data-testid="stSidebarContent"]');
    return {
      headerY: h ? Math.round(h.getBoundingClientRect().y) : null,
      headerH: h ? Math.round(h.getBoundingClientRect().height) : null,
      headerPos: h ? getComputedStyle(h).position : null,
      btnRect: btn ? (function (r) { return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; })(btn.getBoundingClientRect()) : "NO BUTTON",
      scrollable: c ? c.scrollHeight > c.clientHeight : null,
      scrollH: c ? c.scrollHeight : null,
      clientH: c ? c.clientHeight : null,
    };
  });
  console.log("BEFORE SCROLL:", JSON.stringify(before));

  await p.evaluate(function () {
    const c = document.querySelector('[data-testid="stSidebarContent"]');
    if (c) c.scrollTop = 400;
  });
  await p.waitForTimeout(600);
  const after = await p.evaluate(function () {
    const h = document.querySelector('[data-testid="stSidebarHeader"]');
    const btn = document.querySelector('[data-testid="stSidebarCollapseButton"] button');
    return {
      headerY: h ? Math.round(h.getBoundingClientRect().y) : null,
      btnRect: btn ? (function (r) { return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; })(btn.getBoundingClientRect()) : "NO BUTTON",
      scrollTop: (document.querySelector('[data-testid="stSidebarContent"]') || {}).scrollTop,
    };
  });
  console.log("AFTER SCROLL:", JSON.stringify(after));
  await p.screenshot({ path: "ui_shots/41_sidebar_scrolled.png", clip: { x: 0, y: 0, width: 330, height: 680 } });
  await b.close();
})();
