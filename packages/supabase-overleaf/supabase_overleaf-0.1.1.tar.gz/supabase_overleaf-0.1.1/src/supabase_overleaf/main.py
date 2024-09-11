import asyncio
import logging
from crawler_general import crawl_template_list
from crawler_detail import crawl_template_details
from db_handler import (
    insert_templates_general, get_existing_links_general, update_template_general,
    insert_templates_detail, update_template_detail
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_templates(templates, is_new=True):
    detailed_templates = await crawl_template_details(templates)

    if is_new:
        general_count = await insert_templates_general(detailed_templates)
        detail_count = await insert_templates_detail(detailed_templates)
        logging.info(f"Inserted {general_count} general and {detail_count} detailed info for new templates.")
    else:
        general_count = sum([await update_template_general(t) for t in detailed_templates])
        detail_count = sum([await update_template_detail(t) for t in detailed_templates])
        logging.info(f"Updated {general_count} general and {detail_count} detailed info for existing templates.")

async def main():
    try:
        existing_links = await get_existing_links_general()
        logging.info(f"Found {len(existing_links)} existing links in the database.")

        template_list = await crawl_template_list()
        logging.info(f"Crawled {len(template_list)} templates in total.")

        new_templates = [t for t in template_list if t['link'] not in existing_links]
        existing_templates = [t for t in template_list if t['link'] in existing_links]

        logging.info(f"Found {len(new_templates)} new templates to insert.")
        logging.info(f"Found {len(existing_templates)} existing templates to update.")

        # Process new templates
        if new_templates:
            await process_templates(new_templates, is_new=True)

        # Process existing templates
        if existing_templates:
            await process_templates(existing_templates, is_new=False)

        logging.info("All templates have been processed.")

    except Exception as e:
        logging.error(f"An error occurred in main process: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())