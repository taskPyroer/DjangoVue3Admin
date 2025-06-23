# Create your views here.
from app_example.models import Example
from app_example.serializers import ExampleSerializer, ExampleCreateUpdateSerializer
from utils.viewset import CustomModelViewSet


class ExampleViewSet(CustomModelViewSet):
    """
    示例管理视图集 - 基础增删改查
    """
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    create_serializer_class = ExampleCreateUpdateSerializer
    update_serializer_class = ExampleCreateUpdateSerializer
    filterset_fields = ['status', 'category']
    search_fields = ['title', 'content']
    ordering = ['-create_datetime']
