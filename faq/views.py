from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import FAQ
from .serializers import FAQSerializer

@method_decorator(csrf_exempt, name='dispatch')
class FAQViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing FAQs.
    Supports multilingual content through the 'lang' query parameter.
    Uses caching to improve performance.
    """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        """Get queryset with optional caching."""
        lang = self.request.query_params.get('lang', 'en')
        cache_key = f'faq_list_{lang}'
        
        # Try to get from cache
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
        
        # Get fresh queryset and cache it
        queryset = FAQ.objects.all().order_by('-created_at')
        cache.set(cache_key, queryset, 60 * 5)  # Cache for 5 minutes
        return queryset

    def get_serializer_context(self):
        """Add request to serializer context for language handling."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        """Create a new FAQ."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'status': 'success',
                'message': 'FAQ created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Update an FAQ."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                'status': 'success',
                'message': 'FAQ updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete an FAQ and clear related cache."""
        instance = self.get_object()
        self.perform_destroy(instance)
        
        # Clear cache for all languages
        cache.delete_many(['faq_list_en', 'faq_list_hi', 'faq_list_bn'])
        
        return Response({
            'status': 'success',
            'message': 'FAQ deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """Get a single FAQ with language support."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def list(self, request, *args, **kwargs):
        """List all FAQs with translations."""
        try:
            queryset = self.get_queryset()
            # Add debug information
            print(f"Total FAQs in database: {queryset.count()}")
            print(f"Language requested: {request.query_params.get('lang', 'en')}")
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
