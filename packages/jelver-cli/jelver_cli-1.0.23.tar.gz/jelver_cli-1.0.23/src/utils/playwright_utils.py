""" Utility functions for Playwright """

import math
import os

import asyncio
from io import BytesIO
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright


async def wait_for_page_load(page, timeout_s=5):
    try:
        await page.wait_for_load_state('networkidle', timeout=timeout_s * 1000)
    except PlaywrightTimeoutError:
        pass
    return page

async def validate_and_fill(page, selector, input_text, timeout_s=5):
    if not await is_element_found(page, selector):
        raise RuntimeError(f'Selector "{selector}" not found to fill!')
    await page.fill(selector, input_text, timeout=timeout_s * 1000)
    return page

async def click_and_wait_for_idle(page, selector, timeout_s=3):
    if not await is_element_found(page, selector):
        raise RuntimeError(f'Selector "{selector}" not found to click!')

    try:
        await page.click(selector, timeout=timeout_s * 1000)
    except PlaywrightTimeoutError:
        raise RuntimeError('Clicking Selector failed:', selector)

    try:
        await page.wait_for_load_state('networkidle', timeout=timeout_s * 1000)
    except PlaywrightTimeoutError:
        pass
    return page

async def create_context_and_page(profile_dir, headless=True, persistent=False):
    args = []
    context = async_playwright()
    context = await context.start()

    if persistent:
        context = await context.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=headless,
            args=args
        )
    else:
        browser = await context.chromium.launch(
            headless=headless,
            args=args
        )
        context = await browser.new_context()

    page = context.pages[0] if context.pages else await context.new_page()
    return context, page

async def capture_screenshots(page, max_num_screenshots=4):
    viewport_height = await page.evaluate('window.innerHeight')
    full_page_height = await page.evaluate('document.body.scrollHeight')

    screenshots = []
    num_screenshots = math.ceil(full_page_height / viewport_height)

    for i in range(num_screenshots):
        if max_num_screenshots and i >= max_num_screenshots:
            break

        await page.evaluate(f'window.scrollTo(0, {i * viewport_height})')
        screenshot_bytes = await page.screenshot()
        screenshots.append(Image.open(BytesIO(screenshot_bytes)))

    return screenshots

async def fetch_html_and_screenshots(
        page,
        max_page_size_bytes=0,
        max_num_screenshots=None):
    html_task = fetch_page_content(page, max_page_size_bytes)
    screenshots_task = capture_screenshots(
        page,
        max_num_screenshots
    )

    html_result, screenshots_result = await asyncio.gather(
        html_task, screenshots_task
    )

    if isinstance(html_result, Exception):
        raise html_result

    if isinstance(screenshots_result, Exception):
        raise screenshots_result

    return html_result, screenshots_result

async def fetch_page_content(page, max_page_size_bytes=0):
    content = await page.content()
    if max_page_size_bytes and len(content.encode('utf-8')) > max_page_size_bytes:
        raise ValueError("Page size exceeds the maximum limit")
    return content

async def goto_url_with_timeout(page, url, timeout_ms=5000):
    try:
        await asyncio.wait_for(
            page.goto(url, wait_until="networkidle"),
            timeout_ms / 1000
        )
    except asyncio.TimeoutError:
        pass
    return page

async def is_element_found(page, selector):
    locator = page.locator(selector)
    return await locator.count() > 0

