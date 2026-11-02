
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
        部门管理树型接口（单次SQL查询 + 内存O(N)线性建树，彻底拔除递归查库）
        """
        depts = list(Dept.objects.exclude(status='1').order_by('sort', 'id'))
        serializer_data = DeptSerializer(depts, many=True, context={'request': request}).data

        children_map = {}
        for item in serializer_data:
            p_id = item.get('parent')
            children_map.setdefault(p_id, []).append(item)

        for item in serializer_data:
            children = children_map.get(item['id'])
            if children:
                item['children'] = children

        tree_data = children_map.get(None, [])
        return DetailResponse(data=tree_data, msg="获取成功")
