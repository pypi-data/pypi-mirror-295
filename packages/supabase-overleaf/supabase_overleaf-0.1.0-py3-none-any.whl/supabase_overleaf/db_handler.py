import asyncio
from postgrest import AsyncPostgrestClient
from config.config import SUPABASE_URL, SUPABASE_KEY
import logging


async def insert_templates_general(templates):
    client = AsyncPostgrestClient(
        f"{SUPABASE_URL}/rest/v1", headers={"apikey": SUPABASE_KEY})

    inserted_count = 0
    for template in templates:
        template_data = {
            'title': template.get('title'),
            'description': template.get('description'),
            'link': template.get('link'),
            'author': template.get('author'),
            'preview_image_url': template.get('preview_image_url')
        }

        template_data = {k: v for k,
                        v in template_data.items() if v is not None}

        try:
            await client.table('overleaf_templates_general').insert(template_data).execute()
            inserted_count += 1
            logging.info(f"Successfully inserted general info for template: {template_data['title']}")
        except Exception as e:
            logging.error(f"Error inserting general info for template {template_data['title']}: {str(e)}")

    logging.info(f"Inserted general info for {inserted_count} out of {len(templates)} templates.")
    return inserted_count


async def get_existing_links_general():
    client = AsyncPostgrestClient(
        f"{SUPABASE_URL}/rest/v1", headers={"apikey": SUPABASE_KEY})
    response = await client.table('overleaf_templates_general').select('link').execute()
    return [item['link'] for item in response.data]


async def update_template_general(template):
    client = AsyncPostgrestClient(
        f"{SUPABASE_URL}/rest/v1", headers={"apikey": SUPABASE_KEY})

    template_data = {
        'title': template.get('title'),
        'description': template.get('description'),
        'author': template.get('author'),
        'preview_image_url': template.get('preview_image_url')
    }

    template_data = {k: v for k, v in template_data.items() if v is not None}

    try:
        await client.table('overleaf_templates_general').update(template_data).eq('link', template['link']).execute()
        logging.info(f"Successfully updated general info for template: {template_data['title']}")
        return True
    except Exception as e:
        logging.error(f"Error updating general info for template {template_data['title']}: {str(e)}")
        return False


async def insert_templates_detail(templates):
    client = AsyncPostgrestClient(
        f"{SUPABASE_URL}/rest/v1", headers={"apikey": SUPABASE_KEY})

    inserted_count = 0
    for template in templates:
        template_data = {
            'link': template.get('link'),
            'last_updated': template.get('last_updated'),
            'license': template.get('license'),
            'abstract': template.get('abstract'),
            'open_template_link': template.get('open_template_link'),
            'view_pdf_link': template.get('view_pdf_link')
        }

        template_data = {k: v for k,
                        v in template_data.items() if v is not None}

        try:
            await client.table('overleaf_templates_detail').insert(template_data).execute()
            inserted_count += 1
            logging.info(f"Successfully inserted detail info for template: {template.get('title')}")
        except Exception as e:
            logging.error(f"Error inserting detail info for template {template.get('title')}: {str(e)}")

    logging.info(f"Inserted detail info for {inserted_count} out of {len(templates)} templates.")
    return inserted_count


async def update_template_detail(template):
    client = AsyncPostgrestClient(
        f"{SUPABASE_URL}/rest/v1", headers={"apikey": SUPABASE_KEY})

    template_data = {
        'last_updated': template.get('last_updated'),
        'license': template.get('license'),
        'abstract': template.get('abstract'),
        'open_template_link': template.get('open_template_link'),
        'view_pdf_link': template.get('view_pdf_link')
    }

    template_data = {k: v for k, v in template_data.items() if v is not None}

    try:
        await client.table('overleaf_templates_detail').update(template_data).eq('link', template['link']).execute()
        logging.info(f"Successfully updated detail info for template: {template.get('title')}")
        return True
    except Exception as e:
        logging.error(f"Error updating detail info for template {template.get('title')}: {str(e)}")
        return False
