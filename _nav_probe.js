const { chromium } = require("playwright-core");

const URL = process.env.RH_URL || "http://localhost:8506";

(async () => {
  const b = await chromium.launch({
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
    headless: true,
  });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto(URL, { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 40000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) {}
  await p.waitForTimeout(2500);

  const info = await p.evaluate(function () {
    const btns = [].slice.call(document.querySelectorAll('[data-testid="stSidebar"] button'));
    return btns.map(function (b2) {
      const cs = getComputedStyle(b2);
      const r = b2.getBoundingClientRect();
      const pEl = b2.querySelector("p");
      const inner = b2.querySelector('[data-testid="stMarkdownContainer"]');
      return {
        kind: b2.getAttribute("kind"),
        testid: b2.getAttribute("data-testid"),
        text: JSON.stringify(b2.innerText),
        w: Math.round(r.width),
        h: Math.round(r.height),
        bg: cs.backgroundColor,
        color: cs.color,
        pColor: pEl ? getComputedStyle(pEl).color : null,
        pFill: pEl ? getComputedStyle(pEl).webkitTextFillColor : null,
        innerHTML: b2.innerHTML.slice(0, 150),
      };
    });
  });
  console.log(JSON.stringify(info, null, 2));
  await b.close();
})();
