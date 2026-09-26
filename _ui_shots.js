const { chromium } = require("playwright-core");
const path = require("path");

const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const OUT = path.resolve("ui_shots");
const URL = process.env.RH_URL || "http://localhost:8512";

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errors = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push("PAGEERROR: " + e.message));

  await page.goto(URL, { waitUntil: "domcontentloaded" });

  // 1. splash
  try {
    await page.waitForSelector(".raphaid-splash-root", { timeout: 20000 });
    await page.waitForTimeout(1200);
    await page.screenshot({ path: OUT + "/01_splash.png" });
    console.log("captured splash");
  } catch (e) {
    console.log("no splash:", e.message);
  }

  // 2. workspace
  try {
    await page.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 40000 });
  } catch (e) {
    console.log("splash detach:", e.message);
  }
  try { await page.waitForSelector(".rh-topbar", { timeout: 90000 }); } catch (e) { console.log("no topbar"); }
  await page.waitForTimeout(2500);
  await page.screenshot({ path: OUT + "/02_dashboard.png" });

  // 3. scrolled state — the header must stay pinned
  const before = await page.evaluate(function () {
    const el = document.querySelector(".rh-topbar");
    return el ? Math.round(el.getBoundingClientRect().y) : null;
  });
  await page.evaluate(function () {
    const m = document.querySelector('[data-testid="stMain"]');
    if (m) m.scrollTop = 700;
  });
  await page.waitForTimeout(700);
  const after = await page.evaluate(function () {
    const el = document.querySelector(".rh-topbar");
    return el ? Math.round(el.getBoundingClientRect().y) : null;
  });
  console.log("STICKY CHECK  y:", before, "->", after, after !== null && Math.abs(after) < 20 ? "(PINNED)" : "(SCROLLS AWAY)");
  await page.screenshot({ path: OUT + "/03_scrolled.png" });

  // 4. raw HTML leak check (ignoring <style>/<script>)
  const leak = await page.evaluate(function () {
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) {
      const t = n.nodeValue || "";
      if (t.indexOf("<div") < 0 && t.indexOf("</div>") < 0 && t.indexOf("rgba(") < 0) continue;
      let e = n.parentElement, skip = false;
      while (e) { if (e.tagName === "STYLE" || e.tagName === "SCRIPT") { skip = true; break; } e = e.parentElement; }
      if (!skip) out.push(t.slice(0, 90).replace(/\s+/g, " "));
    }
    return out.slice(0, 6);
  });
  console.log("RAW-HTML LEAKS:", JSON.stringify(leak));

  // 5. Medical Assistant
  const clicked = await page.evaluate(function () {
    const btns = [].slice.call(document.querySelectorAll('[data-testid="stSidebar"] button'));
    const t = btns.filter(function (b) { return b.innerText.indexOf("Medical Assistant") >= 0; })[0];
    if (t) { t.click(); return true; }
    return false;
  });
  if (clicked) {
    await page.waitForTimeout(14000);
    await page.screenshot({ path: OUT + "/04_assistant.png" });
    console.log("captured assistant");
  }

  // 6. collapsed sidebar
  await page.evaluate(function () {
    const b = document.querySelector('[data-testid="stSidebarCollapseButton"] button')
           || document.querySelector('[data-testid="collapsedControl"] button');
    if (b) b.click();
  });
  await page.waitForTimeout(2500);
  await page.screenshot({ path: OUT + "/05_collapsed.png" });
  console.log("captured collapsed");

  console.log("CONSOLE ERRORS:", JSON.stringify(errors.slice(0, 6)));
  await browser.close();
})();
