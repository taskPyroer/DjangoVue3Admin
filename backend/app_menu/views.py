from django.db.models import F

from app_menu.models import Menu
from app_menu.serializer import MenuSerializer, MenuTreeSerializer
from utils.json_response import SuccessResponse, DetailResponse
from utils.viewset import CustomModelViewSet


class MenuViewSet(CustomModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filterset_fields = ['status']
    search_fields = ['menu_name']

    def menu_tree(self, request):
        """
        界面菜单树型接口
        :param request:
        :return:
        """
        queryset = Menu.objects.exclude(status='1').filter(parent=None)
        serializer = MenuTreeSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def menu_tree_simple(self, request):
        """
        界面菜单树型接口简单版本
        :param request:
        :return:
        """
        queryset = Menu.objects.exclude(status='1').values(menuId=F('id'), parentId=F("parent_id"), menuName=F("menu_name"))

        menus = []
        # 创建数据字典
        data_dict = {item["menuId"]: item for item in queryset}
        # 遍历数据，找出最高级节点（parent_id为None）
        for item in queryset:
            if item["parentId"] is None:
                menus.append(item)

        # 递归构建树形结构
        def build_tree(node, data_dict):
            node["children"] = [
                build_tree(data_dict[child_id], data_dict)
                for child_id in data_dict
                if data_dict[child_id]["parentId"] == node["menuId"]
            ]
            return node

        # 构建树形结构
        for item in menus:
            build_tree(item, data_dict)

        return DetailResponse(data=menus, msg="获取成功")