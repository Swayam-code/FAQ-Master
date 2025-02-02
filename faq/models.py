from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
import html
import re

class FAQ(models.Model):
    """
    FAQ model with multilingual support for questions and answers.
    Supports Hindi and Bengali translations.
    """
    # Primary fields (English)
    question = models.TextField(help_text="Question in English")
    answer = RichTextField(help_text="Answer in English")
    
    # Hindi translations
    question_hi = models.TextField(blank=True, help_text="Question in Hindi")
    answer_hi = RichTextField(blank=True, help_text="Answer in Hindi")
    
    # Bengali translations
    question_bn = models.TextField(blank=True, help_text="Question in Bengali")
    answer_bn = RichTextField(blank=True, help_text="Answer in Bengali")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

    def clean_html(self, text):
        """Remove HTML tags and decode HTML entities."""
        if not text:
            return ""
        # First decode HTML entities
        text = html.unescape(text)
        # Then remove HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def get_question(self, lang='en'):
        """Get the question in the specified language."""
        if lang == 'hi':
            return self.question_hi or self.question
        elif lang == 'bn':
            return self.question_bn or self.question
        return self.question

    def get_answer(self, lang='en'):
        """Get the answer in the specified language."""
        if lang == 'hi':
            return self.answer_hi or self.answer
        elif lang == 'bn':
            return self.answer_bn or self.answer
        return self.answer

    def save(self, *args, **kwargs):
        """Override save to handle cache clearing."""
        is_new = self.pk is None
        
        # First save to get the ID if new
        super().save(*args, **kwargs)
        
        # Clear cache keys related to this FAQ
        cache_keys = [
            'faq_list_en', 'faq_list_hi', 'faq_list_bn',
            f'faq_{self.pk}_q_en', f'faq_{self.pk}_q_hi', f'faq_{self.pk}_q_bn',
            f'faq_{self.pk}_a_en', f'faq_{self.pk}_a_hi', f'faq_{self.pk}_a_bn'
        ]
        cache.delete_many(cache_keys)
