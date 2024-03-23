# api_views.py
from rest_framework import generics
from .models import Item, Review
from .serializers import ItemSerializer, ReviewSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetailAPIView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'pk'

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'pk'


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Review
# from .serializers import ReviewSerializer

# @csrf_exempt
# @api_view(['POST'])
# def review_create_api_view(request):
#     serializer = ReviewSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=request.user)  # Assuming user is authenticated
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# @csrf_exempt
# @api_view(['GET'])
# def review_list_api_view(request):
#     reviews = Review.objects.all()
#     serializer = ReviewSerializer(reviews, many=True)
#     return Response(serializer.data)


@csrf_exempt
def review_create_api_view(request):
    if request.method == 'POST':
        # Extract review data from the POST request
        user = request.user
        item_id = request.POST.get('item_id')
        content = request.POST.get('content')

        # Check if all required fields are present
        if not (user and item_id and content):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            # Create a new review object and save it to the database
            review = Review.objects.create(user=user, item_id=item_id, content=content)
            return JsonResponse({'message': 'Review created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a JSON response with an error message for other HTTP methods
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)