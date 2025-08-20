from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class authMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 首先排除用户不需要登录就可以访问的界面
        # request.path = '/' 获取用户当前请求的URL
        if request.path_info == '/index/login/':
            return
        # 读取当前用户的登录信息session信息，如果有就是登陆过，可以放行
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 没登陆过则返回登录界面
        return redirect('/index/login/')

