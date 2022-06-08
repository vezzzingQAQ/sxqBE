# 中间件
# 2021.8.22
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# 异常测试
import traceback
# 发送邮件
from django.core import mail
# 引入自定义收件人
from django.conf import settings


# 捕获异常并发送邮件
class ExceptionMW(MiddlewareMixin):
    def process_exception(self, request, exception):
        texttemp = ""
        texttemp += "error:"+str(exception)+"\n"
        texttemp += "error_ip:"+str(request.META["REMOTE_ADDR"])+"\n"
        texttemp += "error_path:"+str(request.path_info)+"\n"
        texttemp += "error_detail:"+str(traceback.format_exc())+"\n"
        mail.send_mail(subject="sxq报错>v(っ °Д °;)っ", message=texttemp,
                       from_email="1932966162@qq.com", recipient_list=settings.MY_EMAIL)
        print("err")
        return JsonResponse({
            "state": 9
        })


# 打印IP信息
class LogIp(MiddlewareMixin):
    def process_request(self, request):
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")
        print("ip : ", ip)
        print(request.META)
