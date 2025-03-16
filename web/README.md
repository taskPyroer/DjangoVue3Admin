# PaoDjangoAdmin

<div align="center"><h3 align="center">PaoDjangoAdmin</h3></div>
<div align="center"><h3 align="center">基于Go前后端分离架构，代码精简，开箱即用，前端紧随前沿 Vue3.0 + TypeScript + vite3 + Element-plus技术</h3></div>


## 🌈平台简介

* 对前后端进行了大部分功能的封装，使用起来更加简洁，功能逻辑清晰，能快速上手学习，并用在生产中。
* 后端采用Django进行开发
* 完善的权限认证系统：完善的权限认证系统，包含，菜单按钮权限，api权限，部门权限。

## 🏭在线体验

演示地址： 帐号：admin 密码：123456  


**> 未来会补充文档和视频，方便友友们使用！**

## 🚧系统截图

更多功能请访问系统体验

## 联系我们

## ⚡ 内置功能

- <span class="tag done-tag">✔</span> **`用户管理`** - _用户是系统操作者，该功能主要完成系统用户配置。._
- <span class="tag done-tag">✔</span> **`部门管理`** - _配置系统组织机构（公司、部门、小组），树结构展现支持数据权限。_
- <span class="tag done-tag">✔</span> **`岗位管理`** - _配置系统用户所属担任职务。_
- <span class="tag done-tag">✔</span> **`菜单管理`** - _配置系统菜单，操作权限，按钮权限标识等。_
- <span class="tag done-tag">✔</span> **`角色管理`** - _角色菜单,API权限分配、设置角色按机构进行数据范围权限划分。_
- <span class="tag done-tag">✔</span> **`字典管理`** - _对系统中经常使用的一些较为固定的数据进行维护。_
- <span class="tag done-tag">✔</span> **`参数管理`** - _对系统动态配置常用参数。_
- <span class="tag done-tag">✔</span> **`通知公告`** - _系统通知公告信息发布维护_
- <span class="tag done-tag">✔</span> **`日志系统`** - _记录日志，更直观浏览_
- <span class="tag done-tag">✔</span> **`系统接口`** - _根据业务代码自动生成相关的api接口文档。_
- <span class="tag done-tag">✔</span> **`服务监控`** - _监视当前系统CPU、内存、磁盘、堆栈等相关信息。_
- <span class="tag done-tag">✔</span> **`代码生成`** - _可直接通过框架生成前后端基础业务代码（go、vue），减少开发时间。_
- <span class="tag done-tag">✔</span> **`组态大屏设计器`** - _通过拖拉拽直接生成组态、大屏。_
- <span class="tag done-tag">✔</span> **`规则链设计`** - _物联网规则链过滤_
- <span class="tag done-tag">✔</span> **`报表设计`** - _数据报表设计_
- <span class="tag done-tag">✔</span> **`产品管理`** - _设备的产品管理_
- <span class="tag done-tag">✔</span> **`设备管理`** - _设备的管理_


---
前端工程结构
---

```
├── src
│   ├── api                  # Api ajax 等
│   ├── assets               # 本地静态资源
│   ├── i18n                 # 国际化
│   ├── components           # 业务通用组件
│   ├── layout               # layout
│   ├── theme                # css主题样式
│   ├── router               # Vue-Router
│   ├── store                # Vuex
│   ├── utils                # 工具库
│   ├── views                # 业务页面入口和常用模板
│   ├── App.vue              # Vue 模板入口
│   └── main.ts              # Vue 入口 TS
├── README.md
└── package.json
```

## 后端工程结构

|     目录     | 功能                                   |
|:----------:|:-------------------------------------|
|  `deploy`  | 部署文件，本项目部署是利用`K3S`进行部署的，因此里面的文档为部署文档 |
|   `apps`   | 基本功能,所有功能模块全在这里面                     |
|  `iothub`  | 设备接入层，设备数据上报在这里处理，使用emqx的hook模式      |
| `resource` | 项目启动或生成的资源文件存放目录。                    |
|   `pkg`    | 所有开发过程中的全局通用代码。                      |
| `uploads`  | 存储上传的文件的地方                           |

更多功能请访问系统。


## ❤特别鸣谢

* 感谢[VUE-NEXT-ADMIN](https://gitee.com/lyt-top/vue-next-admin)
