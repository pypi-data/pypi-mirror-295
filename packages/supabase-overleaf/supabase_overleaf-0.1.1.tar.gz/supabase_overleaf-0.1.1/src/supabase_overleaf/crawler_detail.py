import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os,logging


async def crawl_template_details(template_list):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_template_detail(session, template)
                for template in template_list]
        return await asyncio.gather(*tasks)


async def fetch_template_detail(session, template):
    async with session.get(template['link']) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        # Use provided selector to find main content area
        main_content = soup.select_one(
            "#main-content > div > div > div:nth-child(1)")

        if main_content:
            # Get all available details
            title_element = main_content.select_one('.gallery-item-title h1')
            template['title'] = title_element.text.strip(
            ) if title_element else template.get('title')

            author_element = main_content.select_one('.row-spaced .col-md-9')
            template['author'] = author_element.text.strip(
            ) if author_element else template.get('author', 'Unknown')

            last_updated_element = main_content.select_one(
                '[data-toggle="tooltip-gallery-datetime"]')
            if last_updated_element:
                timestamp = last_updated_element.get(
                    'data-timestamp-for-title')
                if timestamp:
                    template['last_updated'] = datetime.fromtimestamp(
                        int(timestamp)).isoformat()
                else:
                    template['last_updated'] = last_updated_element.text.strip()

            license_element = main_content.find('div', string='许可')
            if license_element:
                license_text = license_element.find_next_sibling('div')
                template['license'] = license_text.text.strip(
                ) if license_text else 'Unknown'

            abstract_element = main_content.find('div', string='摘要')
            if abstract_element:
                abstract_text = abstract_element.find_next_sibling('div')
                template['abstract'] = abstract_text.text.strip(
                ) if abstract_text else ''

            preview_image = main_content.select_one(
                '.gallery-large-pdf-preview img')
            template['preview_image_url'] = preview_image['src'] if preview_image else template.get(
                'preview_image_url')

            # Get the Open Template and View PDF links
            open_template_link = main_content.select_one(
                'a.btn.btn-primary.cta-link')
            if open_template_link:
                template['open_template_link'] = 'https://cn.overleaf.com' + \
                    open_template_link['href']

            view_pdf_link = main_content.select_one(
                'a.btn.btn-secondary.cta-link[target="_blank"]')
            if view_pdf_link:
                template['view_pdf_link'] = 'https://cn.overleaf.com' + \
                    view_pdf_link['href']

            # Add other possible fields
            tags = main_content.select('.tag-list .tag')
            if tags:
                template['tags'] = [tag.text.strip() for tag in tags]

            # Save details to JSON file
            save_template_detail_to_json(template)

        else:
            logging.info(f"Warning: Main content not found for template: {template.get('title', 'Unknown')}")

        await asyncio.sleep(1)  # Be respectful to the server
        return template


def save_template_detail_to_json(template):
    # data dir, make directory if not exists
    if not os.path.exists('data/detail'):
        os.makedirs('data/detail')

    # Use the template's unique identifier (e.g., part of the link) as the filename
    filename = template['link'].split('/')[-1] + '.json'
    filepath = os.path.join('data/detail', filename)

    # Save template info to JSON file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=4)

    logging.info(f"Saved detail information for template: {template['title']} to {filepath}")
