from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app_menu.models import Menu
from app_menu.serializer import  MenuSerializer
from app_user.models import Users
from app_user.serializers import UserSerializer, UserCreateSerializer, UserInfoUpdateSerializer, UserResource
from utils.json_response import DetailResponse, ErrorResponse
from utils.viewset import CustomModelViewSet


class UserViewSet(CustomModelViewSet):
    queryset = Users.objects.exclude(is_delete=1).all()
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    # update_serializer_class = UserInfoUpdateSerializer
    update_serializer_class = UserCreateSerializer
    filterset_fields = ['status', 'phone', 'role', 'dept']
    search_fields = ["username", "nickname"]

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def auth(self, request):
        """
        获取用户权限信息
        """
        user = request.user

        result = {}
        result['user'] = {
            "userId": user.id,
            "username": user.username,
            "nickName": user.nickname,
            "phone": user.phone,
            "gender": user.gender,
            "email": user.email,
            "avatar": user.avatar,
            "dept": user.dept_id,
            "remark": user.remark,
            "is_superuser": user.is_superuser,
        }
        role = getattr(user, 'role')
        role_info = role.values('id', 'role_name', 'role_key')
        if role_info:
            result['role'] = role_info[0]
        else:
            return ErrorResponse(code=4003, msg="该用户没有设定角色，请联系管理员分配角色")
        # 获取对应的menus
        is_superuser = request.user.is_superuser
        is_admin = request.user.role.values_list('admin', flat=True)
        if is_superuser or True in is_admin:
            queryset = Menu.objects.filter(status='0').all()
        else:
            menu_id_list = request.user.role.values_list('menu', flat=True)
            queryset = Menu.objects.filter(status='0', id__in=menu_id_list)

        menu_serializers = MenuSerializer(queryset, many=True).data

        permissions = []
        menus = []
        for menu_serializer in menu_serializers:
            is_hide = menu_serializer['is_hide']
            is_keep_alive = menu_serializer['is_keep_alive']
            is_affix = menu_serializer['is_affix']
            is_iframe = menu_serializer['is_iframe']
            permission = menu_serializer['permission']
            menu_type = menu_serializer['menu_type']
            menu = {
                "id": menu_serializer['id'],
                "parent_id": menu_serializer['parent'],
                "name": menu_serializer['path'],
                "path": menu_serializer['path'],
                "redirect": '',
                "component": menu_serializer['component'],
                "meta": {
                    "title": menu_serializer['menu_name'],
                    "isLink": menu_serializer['is_link'],
                    "isHide": False if is_hide == '0' else True,
                    "isKeepAlive": False if is_keep_alive == '1' else True,
                    "isAffix": False if is_affix == '1' else True,
                    "isIframe": False if is_iframe == '1' else True,
                    "auth": [] if permission == '' else [permission],
                    "icon": menu_serializer['icon']
                },
                'children': []
            }
            if menu_type != 'F':
                menus.append(menu)
            if menu_type in ['F', 'C']:
                permissions.append(permission)

        res_p = []
        # 创建数据字典
        data_dict = {item["id"]: item for item in menus}

        # 遍历数据，找出最高级节点（parent_id为None）
        for item in menus:
            if item["parent_id"] is None:
                res_p.append(item)

        # 递归构建树形结构
        def build_tree(node, data_dict):
            node["children"] = [
                build_tree(data_dict[child_id], data_dict)
                for child_id in data_dict
                if data_dict[child_id]["parent_id"] == node["id"]
            ]
            return node

        # 构建树形结构
        for item in res_p:
            build_tree(item, data_dict)

        result['menus'] = res_p
        result['permissions'] = permissions
        return DetailResponse(data=result, msg="获取成功")

    def user_info(self, request):
        """
        获取当前用户信息
        """
        user = request.user
        result = {
            "nickname": user.nickname,
            "phone": user.phone,
            "gender": user.gender,
            "email": user.email
        }
        return DetailResponse(data=result, msg="获取成功")

    def update_user_info(self, request):
        """
        修改当前用户信息
        """
        user = request.user
        Users.objects.filter(id=user.id).update(**request.data)
        return DetailResponse(data=None, msg="修改成功")

    def export_to_excel(self, request):
        """
        用户表导出
        """
        user_resource = UserResource()
        dataset = user_resource.export()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        filename = f"user_{timestamp}.xls"
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response