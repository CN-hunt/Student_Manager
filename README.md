# 基于Django的学生信息管理
一个功能完整的双语（简体中文/日本語）学生管理系统，专注于展示 **Django 国际化 (i18n) 与本地化 (l10n)** 的最佳实践与完整实现流程。

🌐 **在线演示 (Live Demo):**: [(部署中)点击此处访问部署在 PythonAnywhere 上的应用](https://xn--6qqv7i14ofosyrb.pythonanywhere.com/)

------

##  项目特色

- **核心焦点**: 并非一个功能繁杂的业务系统，而是一个**技术展示项目 (Showcase Project)**，演示 Django i18n/l10n实现 。
- **无缝语言切换**: 实现了前后端完全国际化，支持简体中文与日本語之间的即时、无缝切换。
- **标准技术栈**: 使用 Django 全栈开发，包含模型设计、表单验证、视图逻辑、模板渲染及用户认证。
- **响应式界面**: 基于 Bootstrap 3 构建，适配桌面与移动设备。
- **开箱即用**: 结构清晰，代码注释完整。

## 🛠️ 技术栈

- **后端框架**: [Django](https://www.djangoproject.com/)
- **前端框架**: [Bootstrap 3](https://getbootstrap.com/docs/3.3/)
- **数据库**:  MySQL (生产)
- **国际化**: Django i18n & l10n
- **部署平台**: PythonAnywhere

##  项目截图

| 中文界面                                 | 日文界面                                  |
| :--------------------------------------- | :---------------------------------------- |
| ![](./cn.png) | ![](./jap.png) |
| *学生列表页（中文）*                     | *学生列表页（日本語）*                    |

## 快速开始

### 前提条件

确保你的系统已安装：

- Python 3.8+
- Git
- Pip

### 安装与运行

1. **克隆项目**

   bash

   ```
   git clone https://github.com/你的用户名/你的仓库名.git
   cd 你的仓库名
   ```

2. **创建虚拟环境并安装依赖**

   bash

   ```
   # 创建虚拟环境 (Windows)
   python -m venv venv
   # 激活虚拟环境 (Windows)
   .\venv\Scripts\activate
   # 安装依赖
   pip install -r requirements.txt
   ```

3. **配置数据库并运行迁移**

   bash

   ```
   python manage.py migrate
   ```

4. **创建超级用户（可选，用于访问Django Admin后台）**

   bash

   ```
   python manage.py createsuperuser
   ```

5. **收集静态文件**

   bash

   ```
   python manage.py collectstatic
   ```

6. **启动开发服务器**

   bash

   ```
   python manage.py runserver
   ```

   在浏览器中访问 `http://127.0.0.1:8000` 即可查看项目。

### 🔧 生成翻译文件（供开发者参考）

本项目翻译文件已编译完成。如需添加新翻译或修改，请遵循以下步骤：

bash

```python
# 1. 在代码和模板中标记新字符串（使用 _() 和 {% trans %}）
# 2. 生成消息文件
django-admin makemessages -l ja  # 生成日文
# django-admin makemessages -l zh_Hans  # 如需生成中文
# 3. 编辑 locale/ja/LC_MESSAGES/django.po 文件，填写 msgstr
# 4. 编译消息文件
django-admin compilemessages
```

## 👨‍💻 作者

**一个过劳的普通本科在校生**

- GitHub: [@CN_Sakura]
- 邮箱: xiao_fei_xiang@qq.com
- 技能: Python / Django / 日本語 (N2)/Web Crawling(request/xpath/)/……


