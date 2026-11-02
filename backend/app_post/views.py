from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponse

from app_post.models import Post
from app_post.serializers import PostSerializers, PostResource
from utils.json_response import DetailResponse
from utils.viewset import CustomModelViewSet

CACHE_KEY_ALL_POSTS = "all_active_posts"

class PostViewSet(CustomModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    filterset_fields = ["status"]
    search_fields = ["post_name", "post_code"]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.delete(CACHE_KEY_ALL_POSTS)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.delete(CACHE_KEY_ALL_POSTS)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.delete(CACHE_KEY_ALL_POSTS)

    def get_all_posts(self, request, *args, **kwargs):
        """
        获取职位表里所有的职位（带缓存与规范排序）
        """
        posts = cache.get(CACHE_KEY_ALL_POSTS)
        if posts is None:
            posts = list(Post.objects.filter(status='0').order_by('sort', 'id').values('post_name', 'id'))
            cache.set(CACHE_KEY_ALL_POSTS, posts, 3600)

        return DetailResponse(data={
            'posts': posts,
        }, msg="获取成功")

    def export_to_excel(self, request):
        """
        导出表
        """
        post_resource = PostResource()
        dataset = post_resource.export()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        filename = f"post_{timestamp}.xls"
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response