# App Example - 示例模块

## 功能说明

这是一个简单的示例模块，展示了Django Vue3 Admin项目的基础增删改查开发模式。

## 模型字段

### Example 模型

- `title`: 标题（必填，最大100字符）
- `content`: 内容（可选，文本字段）
- `category`: 分类（可选，最大50字符）
- `status`: 状态（0-正常，1-停用）

## API 接口

### 基础CRUD接口

- `GET /system/example/` - 获取示例列表
- `POST /system/example/` - 创建示例
- `GET /system/example/{id}/` - 获取示例详情
- `PUT /system/example/{id}/` - 更新示例
- `DELETE /system/example/{id}/` - 删除示例

### 查询参数

- `status`: 按状态过滤
- `category`: 按分类过滤
- `search`: 搜索标题、内容
- `ordering`: 按创建时间排序

## 使用示例

### 创建示例

```json
POST /system/example/
{
    "title": "示例标题",
    "content": "这是示例内容",
    "category": "技术",
    "status": "0"
}
```

### 获取列表

```json
GET /system/example/?status=0&category=技术
{
    "code": 2000,
    "msg": "获取成功",
    "data": {
        "results": [
            {
                "id": 1,
                "title": "示例标题",
                "content": "这是示例内容",
                "category": "技术",
                "status": "0",
                "create_datetime": "2023-12-20T10:00:00Z"
            }
        ]
    }
}
```

## 数据库迁移

创建模型后需要执行数据库迁移：

```bash
python manage.py makemigrations app_example
python manage.py migrate
```
