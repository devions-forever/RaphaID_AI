const { chromium } = require("playwright-core");
const URL = process.env.RH_URL || "http://localhost:8509";
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  await p.goto(URL, { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 45000 }); } catch (e) {}
  try { await p.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) {}
  await p.waitForTimeout(2500);

  const info = await p.evaluate(function () {
    const sb = document.querySelector('[data-testid="stSidebar"]');
    const out = { structure: [], buttons: [] };
    if (!sb) return { error: "no sidebar" };
    const walk = function (el, depth) {
      if (depth > 3) return;
      for (let i = 0; i < el.children.length; i++) {
        const c = el.children[i];
        const cs = getComputedStyle(c);
        const r = c.getBoundingClientRect();
        const tid = c.getAttribute("data-testid");
        if (tid) {
          out.structure.push({
            depth: depth,
            testid: tid,
            pos: cs.position,
            top: cs.top,
            overflowY: cs.overflowY,
            h: Math.round(r.height),
            scrollH: c.scrollHeight,
            clientH: c.clientHeight,
            bg: cs.backgroundColor,
            z: cs.zIndex,
          });
        }
        walk(c, depth + 1);
      }
    };
    walk(sb, 0);
    const btns = sb.querySelectorAll("button");
    for (let i = 0; i < btns.length; i++) {
      const r = btns[i].getBoundingClientRect();
      let par = btns[i].parentElement, tid = null;
      for (let d = 0; d < 5 && par; d++) { const t = par.getAttribute("data-testid"); if (t) { tid = t; break; } par = par.parentElement; }
      out.buttons.push({ kind: btns[i].getAttribute("kind"), parent: tid, rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)] });
    }
    return out;
  });
  console.log(JSON.stringify(info, null, 2));
  await b.close();
})();
