const { chromium } = require("playwright-core");

const URL = process.env.RH_URL || "http://localhost:8506";

(async () => {
  const b = await chromium.launch({
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
    headless: true,
  });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto(URL, { waitUntil: "domcontentloaded" });
  try {
    await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 40000 });
  } catch (e) {
    console.log("splash wait:", e.message);
  }
  await p.waitForTimeout(3000);
  // The cold start is slow (torch etc.) — wait for the clinical bar to exist.
  try {
    await p.waitForSelector(".rh-topbar", { timeout: 90000 });
  } catch (e) {
    console.log("topbar never appeared:", e.message);
  }
  await p.waitForTimeout(1500);

  const info = await p.evaluate(function () {
    const el = document.querySelector(".rh-topbar");
    if (!el) return { error: "topbar missing", bodyHead: (document.body.innerText || "").slice(0, 200) };
    const cs = getComputedStyle(el);
    const out = {
      topbar: {
        position: cs.position,
        top: cs.top,
        rect: (function (r) { return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; })(el.getBoundingClientRect()),
      },
      ancestors: [],
      scrollers: [],
    };
    let e = el.parentElement;
    let d = 0;
    while (e && d < 14) {
      const s = getComputedStyle(e);
      out.ancestors.push({
        tag: e.tagName,
        testid: e.getAttribute("data-testid"),
        overflow: s.overflow,
        overflowY: s.overflowY,
        display: s.display,
        h: s.height,
        scrollH: e.scrollHeight,
        clientH: e.clientHeight,
      });
      if (e.scrollHeight > e.clientHeight + 4) {
        out.scrollers.push({
          tag: e.tagName,
          testid: e.getAttribute("data-testid"),
          overflowY: s.overflowY,
          scrollH: e.scrollHeight,
          clientH: e.clientHeight,
        });
      }
      e = e.parentElement;
      d++;
    }
    return out;
  });
  console.log(JSON.stringify(info, null, 2));

  // Try scrolling the likely scroller and see if the topbar stays put
  const before = await p.evaluate(function () {
    const el = document.querySelector(".rh-topbar");
    return el ? Math.round(el.getBoundingClientRect().y) : null;
  });
  await p.evaluate(function () {
    const cands = [
      document.querySelector('[data-testid="stMain"]'),
      document.querySelector('[data-testid="stAppViewContainer"]'),
      document.querySelector("section.main"),
      document.scrollingElement,
    ].filter(Boolean);
    for (let i = 0; i < cands.length; i++) {
      cands[i].scrollTop = 400;
    }
    window.scrollTo(0, 400);
  });
  await p.waitForTimeout(600);
  const after = await p.evaluate(function () {
    const el = document.querySelector(".rh-topbar");
    return el ? Math.round(el.getBoundingClientRect().y) : null;
  });
  console.log("TOPBAR y before/after scroll:", before, after);
  await b.close();
})();
