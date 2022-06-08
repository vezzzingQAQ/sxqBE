from random import randint, random
from django.http import JsonResponse
from django.shortcuts import render
from zvoice.models import Student

# Create your views here.


def _printStudent(name, id, c_class, classid):
    return "name:"+name+" cid:"+id+" c_class:"+c_class+" c_class_id:"+classid+" -"


def addStudentView(request):
    # 初始化返还参数
    return_state = 9
    return_msg = "未知错误"
    if request.method == 'POST':
        current_name = request.POST.get('name', None)
        current_cid = request.POST.get('cid', None)
        current_class = request.POST.get('class', None)
        current_classid = request.POST.get('classid', None)
        p_isRandom = request.POST.get('isRandom', None)
        if current_name and current_cid and current_class and current_classid:
            # 没有重复的话就新增
            if not Student.objects.filter(cid=current_cid):
                # 判断班内编号有没有重复
                if not Student.objects.filter(c_class=current_class, c_class_id=current_classid):
                    voiceData = 0
                    if p_isRandom:
                        voiceData = randint(0, 1000)
                    current_student = Student(
                        name=current_name,
                        cid=current_cid,
                        c_class=current_class,
                        c_class_id=current_classid,
                        voice=voiceData,
                        record=voiceData
                    )
                    current_student.save()
                    return_state = 1
                    return_msg = "success"
                else:
                    return_msg = _printStudent(
                        current_name, current_cid, current_class, current_classid)+"班内编号重复"
            else:
                return_msg = _printStudent(
                    current_name, current_cid, current_class, current_classid)+"学号已存在"
        else:
            return_msg = _printStudent(
                current_name, current_cid, current_class, current_classid)+"参数不全"
    else:
        return_msg = "请求方法错误"
    return JsonResponse({
        "state": return_state,
        "content": {
            "msg": return_msg
        }
    })
