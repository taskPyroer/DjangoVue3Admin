
# Create your views here.
from app_dept.models import Dept
from app_dept.serializers import DeptSerializer, DeptTreeSerializer, DeptCreateUpdateSerializer
from utils.json_response import DetailResponse
from utils.viewset import CustomModelViewSet


class DeptViewSet(CustomModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    create_serializer_class = DeptCreateUpdateSerializer
    update_serializer_class = DeptCreateUpdateSerializer
    filterset_fields = ['status']
    search_fields = ['dept_name', 'dept_key', 'phone', 'email']

    def dept_tree(self, request):
        """
        部门管理树型接口
        :param request:
        :return:
        """
        queryset = Dept.objects.exclude(status='1').filter(parent=None)
        serializer = DeptTreeSerializer(queryset, many=True)
        return DetailResponse(data=serializer.data, msg="获取成功")
