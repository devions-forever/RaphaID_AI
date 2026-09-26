const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto("http://localhost:8502", { waitUntil: "domcontentloaded" });
  try { await p.waitForSelector(".raphaid-splash-root", { state: "detached", timeout: 30000 }); } catch (e) {}
  await p.waitForTimeout(2500);
  const leaks = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll("[data-testid='stMarkdownContainer'], pre, code").forEach((el) => {
      const t = el.innerText || "";
      if (t.includes("<div") || t.includes("</div>") || t.includes("style=")) {
        out.push({ tag: el.tagName, testid: el.getAttribute("data-testid"), head: t.slice(0, 160).replace(/\s+/g, " ") });
      }
    });
    return out.slice(0, 12);
  });
  console.log(JSON.stringify(leaks, null, 2));
  await b.close();
})();
