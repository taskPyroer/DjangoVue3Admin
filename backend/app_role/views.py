
# Create your views here.
from casbin_adapter.enforcer import enforcer
from django.db import transaction

from app_role.models import Role
from app_role.serializers import RoleSerializer, RoleCreateSerializer
from utils.json_response import DetailResponse, ErrorResponse
from utils.viewset import CustomModelViewSet


class RoleViewSet(CustomModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateSerializer
    update_serializer_class = RoleCreateSerializer
    filterset_fields = ['status']
    search_fields = ['role_name', 'role_key']

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        重写删除
        """
        instances = self.get_object_list()
        try:
            with transaction.atomic():
                # 需要删除casbin_rule权限表的数据
                for instance in instances:
                    sub = instance.role_key
                    enforcer.remove_filtered_policy(0, sub)
                self.perform_destroy(instances)
                return DetailResponse(data=[], msg="删除成功")
        except Exception as e:
            return ErrorResponse(data=[], msg="删除失败: {}".format(str(e)))

    def retrieve(self, request, *args, **kwargs):
        """
        重写单次查询
        """
        instance = self.get_object()
        menus = instance.menu.values('id', 'parent')
        cleaned_menus = []

        # 过滤掉已经在parent字段中出现过的id
        menu_parents = [m['parent'] for m in menus]
        for menu in menus:
            if menu['id'] not in menu_parents:
                cleaned_menus.append(menu)

        menu_ids = [menu['id'] for menu in cleaned_menus]

        depts = instance.dept.values('id', 'parent')
        cleaned_depts = []

        # 过滤掉已经在parent字段中出现过的id
        dept_parents = [d['parent'] for d in depts]
        for dept in depts:
            if dept['id'] not in dept_parents:
                cleaned_depts.append(dept)

        dept_ids = [dept['id'] for dept in cleaned_depts]

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        data['menu'] = menu_ids
        data['dept'] = dept_ids

        return DetailResponse(data={'data': data}, msg="获取成功")


    def get_policy_path_role(self, request, *args, **kwargs):
        """
        获取当前角色权限的API
        """
        instance = self.get_object()
        sub = instance.role_key
        filtered_policy = enforcer.get_filtered_policy(0, sub)
        if filtered_policy:
            data = [{'role_key': fp[0], 'path': fp[1], 'method': fp[2]} for fp in filtered_policy]
            return DetailResponse(data=data, msg="获取策略中的所有授权规则")
        else:
            return ErrorResponse(data=[], msg="没有该角色权限存在")

    def get_all_roles(self, request, *args, **kwargs):
        """
        获取角色表里所有的角色
        """
        roles = Role.objects.values('role_name', 'id').filter(status='0').all()
        return DetailResponse(data={
            'roles': roles,
        }, msg="获取成功")