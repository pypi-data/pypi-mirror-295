import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import os
import logging


async def crawl_template_list():
    base_url = "https://cn.overleaf.com/latex/templates/recent/page/"
    templates = []
    last_processed_page = 0

    # 检查是否有之前的进度
    if os.path.exists('templates_progress.json'):
        with open('templates_progress.json', 'r') as f:
            data = json.load(f)
            last_processed_page = data['last_page']
        logging.info(f"Resuming from page {last_processed_page + 1}")

    async with aiohttp.ClientSession() as session:
        page = last_processed_page + 1
        while True:
            url = f"{base_url}{page}"
            try:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    template_elements = soup.select(".gallery-thumbnail")

                    if not template_elements:
                        logging.info(f"No templates found on page {page}. This might be the last page.")
                        break

                    for element in template_elements:
                        title_element = element.select_one('.caption__title')
                        description_element = element.select_one(
                            '.caption__description')
                        author_element = element.select(
                            'div.caption > div')[-1]
                        link_element = element.select_one('a')
                        if title_element and link_element:
                            template = {
                                'title': title_element.text.strip(),
                                'description': description_element.text.strip() if description_element else "",
                                'link': 'https://cn.overleaf.com' + link_element['href'],
                                'author': author_element.text.strip() if author_element else "Unknown",
                                'preview_image_url': link_element.find('img')['src'] if link_element.find('img') else None
                            }
                            templates.append(template)

                            # Save template to JSON
                            save_template_to_json(template)

                logging.info(f"Processed page {page}, found {len(templates)} templates so far.")

                # save progress
                with open('templates_progress.json', 'w') as f:
                    json.dump({'last_page': page}, f)

                # Check if not last page
                if '"last_page": {}'.format(page) in html:
                    logging.info(f"Reached the last page ({page}). Stopping the crawl.")
                    break

                page += 1
                await asyncio.sleep(1)  # Be respectful to the server

            except Exception as e:
                logging.error(f"Error processing page {page}: {str(e)}")
                # save progress and exit the loop
                with open('templates_progress.json', 'w') as f:
                    json.dump({'last_page': page - 1}, f)
                break

    logging.info(f"Crawling completed. Total templates found: {len(templates)}")
    return templates


def save_template_to_json(template):
    # data/general, Make sure the directory exists
    if not os.path.exists('data/general'):
        os.makedirs('data/general')

    # Use the template's unique identifier (e.g., part of the link) as the filename
    filename = f"general_{template['link'].split('/')[-1]}.json"
    filepath = os.path.join('data/general', filename)

    # Let the template's title be the filename as json files
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=4)

    logging.info(f"Saved general information for template: {template['title']} to {filepath}")


# use example
async def main():
    templates = await crawl_template_list()
    logging.info(f"Total templates crawled: {len(templates)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())
