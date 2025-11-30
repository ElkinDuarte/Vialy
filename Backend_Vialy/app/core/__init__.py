"""
Módulo core con funcionalidades principales.
"""

from app.core.prompts import PromptTemplates, CATEGORIES, CATEGORY_NAMES
from app.core.session_manager import session_manager

__all__ = ['PromptTemplates', 'CATEGORIES', 'CATEGORY_NAMES', 'session_manager']