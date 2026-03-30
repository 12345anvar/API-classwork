"""
/posts/ -> GET
/post/1/ -> GET
/post/1/ -> PUT
/post/1/ -> DELETE
/posts/ -> POST
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.serializers import PostModelSerializer
from rest_framework import generics
from .serializers import RegisterSerializer, PostSerializer
from .models import Post
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'PUT'])
def posts_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostModelSerializer(posts, many=True)
        return Response(data=serializer.data, status=200)
    elif request.method == 'POST':
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)
        return Response(data=serializer.errors, status=400)
    else:
        return Response(status=405)

@api_view(['GET', 'PUT', 'DELETE'])
def posts_detail(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if not post:
        return Response(status=404)
    if request.method == 'GET':
        serializer = PostModelSerializer(post)
        return Response(data=serializer.data, status=200)
    elif request.method == 'PUT':
        serializer = PostModelSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=400)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=204)
    else:
        return Response(status=405)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class PostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)