# Screenshots use the live data file.
"""Serve the repo locally and take desktop and mobile screenshots with live data (run in GitHub Actions)."""
import asyncio, os, subprocess, sys, time
from PIL import Image
from playwright.async_api import async_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "docs", "screenshots")


async def main():
    os.makedirs(OUT, exist_ok=True)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8099"], cwd=ROOT)
    time.sleep(1.5)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            for name, w, h, dsf in [("desktop", 1280, 1440, 1), ("mobile", 390, 844, 2)]:
                ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dsf, timezone_id="Europe/Warsaw", locale="en-GB")
                pg = await ctx.new_page()
                await pg.goto("http://localhost:8099/")
                await pg.wait_for_function("document.querySelectorAll('#mess-stats .stat').length > 0", timeout=30000)
                await pg.wait_for_timeout(800)
                png = os.path.join(OUT, name + ".png")
                await pg.screenshot(path=png)
                Image.open(png).save(os.path.join(OUT, name + ".webp"), quality=82)
                os.remove(png)
            await b.close()
    finally:
        srv.terminate()


asyncio.run(main())
