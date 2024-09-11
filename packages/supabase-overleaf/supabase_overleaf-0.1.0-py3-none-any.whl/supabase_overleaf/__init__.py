from .crawler_general import get_overleaf_tags
from .crawler_detail import get_template_details
from .db_handler import SupabaseHandler

__all__ = ['get_overleaf_tags', 'get_template_details', 'SupabaseHandler']

__version__ = "0.1.0"
