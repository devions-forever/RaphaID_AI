const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto(process.env.RH_URL || "http://localhost:8508", { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 40000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) {}
  await p.waitForTimeout(2500);
  const out = await p.evaluate(function () {
    const res = [];
    const all = document.querySelectorAll('[data-testid="stSidebar"] button');
    for (let i = 0; i < all.length; i++) {
      const t = all[i].innerText || "";
      if (t.indexOf("Dashboard") < 0 && t.indexOf("Pathology") < 0) continue;
      const cs = getComputedStyle(all[i]);
      const inner = all[i].querySelector("p") || all[i].querySelector("div");
      const ics = inner ? getComputedStyle(inner) : null;
      res.push({
        text: t.trim(),
        kind: all[i].getAttribute("kind"),
        bg: cs.backgroundColor,
        bgImage: cs.backgroundImage,
        color: cs.color,
        opacity: cs.opacity,
        visibility: cs.visibility,
        innerTag: inner ? inner.tagName : null,
        innerColor: ics ? ics.color : null,
        innerFill: ics ? ics.webkitTextFillColor : null,
        innerHTML: all[i].innerHTML.slice(0, 130),
      });
    }
    return res;
  });
  console.log(JSON.stringify(out, null, 2));
  await b.close();
})();
