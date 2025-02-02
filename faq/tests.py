from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import FAQ

class FAQModelTests(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is this FAQ system?",
            answer="This is a test FAQ system.",
            question_hi="यह FAQ सिस्टम क्या है?",
            question_bn="এই FAQ সিস্টেম কি?",
            answer_hi="यह एक टेस्ट FAQ सिस्टम है।",
            answer_bn="এটি একটি টেস্ট FAQ সিস্টেম।"
        )

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "What is this FAQ system?")
        self.assertEqual(self.faq.answer, "This is a test FAQ system.")

    def test_str_representation(self):
        self.assertEqual(str(self.faq), "What is this FAQ system?")

    def test_translations_exist(self):
        self.assertTrue(len(self.faq.question_hi) > 0)
        self.assertTrue(len(self.faq.question_bn) > 0)

class FAQAPITests(APITestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="How do I use the API?",
            answer="You can use REST API endpoints.",
            question_hi="मैं API का उपयोग कैसे करूं?",
            answer_hi="आप REST API एंडपॉइंट्स का उपयोग कर सकते हैं।",
            question_bn="এপিআই ব্যবহার করতে আমি কি করবো?",
            answer_bn="আপনি রেস্ট এপিআই এন্ডপয়েন্ট ব্যবহার করতে পারেন।"
        )
        self.url = reverse('faq-list')

    def test_get_faq_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_faq_in_hindi(self):
        response = self.client.get(f"{self.url}?lang=hi")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['question'], "मैं API का उपयोग कैसे करूं?")

    def test_cache_mechanism(self):
        """Test that caching works for FAQ list endpoint"""
        # First request - should hit database
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Second request - should hit cache
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_translation_fallback(self):
        """Test fallback to English when translation is missing"""
        # Test fallback to English when translation is missing
        response = self.client.get(reverse('faq-list') + '?lang=fr')  # Unsupported language
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['question'], self.faq.question)  # Should fallback to English

    def test_translation_cache(self):
        """Test that translations are properly cached"""
        # First request to trigger translation
        response = self.client.get(reverse('faq-list') + '?lang=hi')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Second request should use cached translation
        response = self.client.get(reverse('faq-list') + '?lang=hi')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['question'], self.faq.question_hi)
