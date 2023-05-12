from django.http import JsonResponse

from rest_framework.decorators import api_view

from .models import Post
from .serializers import PostSerializer


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse({'data': serializer.data})