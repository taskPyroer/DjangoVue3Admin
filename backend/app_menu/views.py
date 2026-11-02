from django.db.models import F

from app_menu.models import Menu
from app_menu.serializer import MenuSerializer
from utils.json_response import SuccessResponse, DetailResponse
from utils.viewset import CustomModelViewSet


class MenuViewSet(CustomModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filterset_fields = ['status']
    search_fields = ['menu_name']

    def menu_tree(self, request):
        """
        界面菜单树型接口（单次SQL查询 + 内存O(N)快速建树，彻底拔除递归查库）
        """
        menus = list(Menu.objects.exclude(status='1').order_by('sort', 'id'))
        serializer_data = MenuSerializer(menus, many=True, context={'request': request}).data

        children_map = {}
        for item in serializer_data:
            p_id = item.get('parent')
            children_map.setdefault(p_id, []).append(item)

        for item in serializer_data:
            children = children_map.get(item['id'])
            if children:
                item['children'] = children

        tree_data = children_map.get(None, [])
        return SuccessResponse(data=tree_data, msg="获取成功")

    def menu_tree_simple(self, request):
        """
        界面菜单树型接口简单版本（单次SQL查询 + 内存O(N)线性建树）
        """
        queryset = list(
            Menu.objects.exclude(status='1')
            .order_by('sort', 'id')
            .values(menuId=F('id'), parentId=F("parent_id"), menuName=F("menu_name"))
        )

        children_map = {}
        for item in queryset:
            p_id = item.get("parentId")
            children_map.setdefault(p_id, []).append(item)

        for item in queryset:
            children = children_map.get(item["menuId"])
            if children:
                item["children"] = children

        tree_data = children_map.get(None, [])
        return DetailResponse(data=tree_data, msg="获取成功")