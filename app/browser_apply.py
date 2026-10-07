"""
Guided browser automation.

This module intentionally does NOT bypass CAPTCHAs, anti-bot controls, or make legal /
work-authorization declarations without human approval. Arbitrary ATS systems change often,
so production deployments should add site-specific adapters for Workday, Greenhouse, Lever,
iCIMS, etc.
"""
from pathlib import Path
from playwright.async_api import async_playwright

SENSITIVE_TERMS = [
    "sponsorship", "authorized to work", "work authorization", "citizen",
    "disability", "veteran", "race", "gender", "salary expectation",
    "background", "criminal", "non-compete"
]

async def open_guided_application(url: str, resume_path: str | None = None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # Safe convenience autofill only. Sensitive questions remain unanswered.
        fields = [
            ("input[name*=first i]", "Sai Jagan"),
            ("input[name*=last i]", "Yalamanchili"),
            ("input[type=email]", "saijagan.yalamanchili7@gmail.com"),
            ("input[type=tel]", "+1 989-933-2400"),
        ]
        for selector, value in fields:
            try:
                loc = page.locator(selector).first
                if await loc.count():
                    await loc.fill(value)
            except Exception:
                pass

        if resume_path:
            try:
                file_inputs = page.locator("input[type=file]")
                if await file_inputs.count():
                    await file_inputs.first.set_input_files(str(Path(resume_path).resolve()))
            except Exception:
                pass

        # Keep browser open for user review; caller may replace this with a secure remote browser.
        return {"status": "REVIEW_REQUIRED", "page_title": await page.title()}
