from django.utils import timezone

from django.http import HttpResponse

# Create your views here.

from app_post.models import Post
from app_post.serializers import PostSerializers, PostResource
from utils.json_response import DetailResponse
from utils.viewset import CustomModelViewSet


class PostViewSet(CustomModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    filterset_fields = ["status"]
    search_fields = ["post_name", "post_code"]

    def get_all_posts(self, request, *args, **kwargs):
        """
        获取职位表里所有的职位
        """
        posts = Post.objects.values('post_name', 'id').filter(status='0').all()
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