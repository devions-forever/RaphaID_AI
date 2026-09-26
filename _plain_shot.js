const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.goto("http://localhost:8507", { waitUntil: "domcontentloaded" });
  await p.waitForTimeout(6000);
  await p.screenshot({ path: "ui_shots/20_plain_expanded.png", clip: { x: 0, y: 0, width: 700, height: 300 } });
  console.log("saved plain expanded crop");
  await b.close();
})();
