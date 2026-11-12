// Renders anim.html into PNG frames: node render.js <outDir> <frames>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const outDir = process.argv[2];
  const N = parseInt(process.argv[3] || '75', 10);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1024, height: 1024 } });
  await page.goto('file://' + path.join(__dirname, 'anim.html'));
  for (let i = 0; i < N; i++) {
    const data = await page.evaluate((t) => { draw(t); return document.getElementById('c').toDataURL('image/png'); }, i / N);
    fs.writeFileSync(path.join(outDir, `f${String(i).padStart(3, '0')}.png`), Buffer.from(data.split(',')[1], 'base64'));
  }
  await browser.close();
  console.log('frames', N);
})();
