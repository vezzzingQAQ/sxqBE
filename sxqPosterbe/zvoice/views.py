from django.http import JsonResponse
from zvoice.models import Student
import jwt

JWTSALT = "321fgergs1&iX0^dG0$gN4[cJ3`iG"

# Create your views here.


def error_handler(error):
    print(error)
    return JsonResponse({
        "state": 9
    })


def getStudentView(request):
    global JWTSALT
    # 校验学生身份并返回JWT
    try:
        # 初始化返还参数
        return_state = 9
        return_msg = ""
        return_jwt = ""
        return_name = ""
        return_id = -1
        return_class = ""
        if request.method == 'POST':
            current_name = request.POST.get('name', None)
            current_cid = request.POST.get('cid', None)
            # 校验学生身份
            if current_name and current_cid:
                current_student = Student.objects.filter(
                    name=current_name, cid=current_cid)
                if current_student and len(current_student) == 1:
                    current_student = current_student[0]
                    # 构造JWT
                    headers = {
                        'typ': 'jwt',
                        'alg': 'HS256'
                    }
                    payload = {
                        'id': current_student.id,
                        'name': current_student.name,
                        'c_class': current_student.c_class,
                    }
                    jwt_result = jwt.encode(payload=payload, key=JWTSALT,
                                            algorithm="HS256", headers=headers)
                    # 返还参数赋值
                    return_state = 1
                    return_msg = "success"
                    return_jwt = jwt_result
                    return_name = current_student.name
                    return_id = current_student.id
                    return_class = current_student.c_class
                else:
                    return_state = 2
                    return_msg = "auth fail"
            else:
                return_state = 2
                return_msg = "auth fail"
        else:
            return_state = 3
            return_msg = "error method"
        return JsonResponse({
            "state": return_state,
            "content": {
                "msg": return_msg,
                "jwt": return_jwt,
                "name": return_name,
                "id": return_id,
                "class": return_class
            }
        })
    except Exception as e:
        return error_handler(e)


def _checkJWT(current_jwt):
    global JWTSALT
    # 检查jwt是否被篡改
    try:
        jwt.decode(current_jwt, JWTSALT, algorithms="HS256")
        return True
    except:
        return False


def _decodeJWT(current_jwt):
    global JWTSALT
    # 解码jwt
    if(_checkJWT(current_jwt)):
        return jwt.decode(current_jwt, JWTSALT, algorithms="HS256")
    else:
        return False


def setVoiceView(request):
    global JWTSALT
    # 上传音量到数据库
    try:
        # 初始化返还参数
        return_state = 9
        return_msg = ""
        return_voice = -1
        return_name = ""
        return_id = -1
        return_class = ""
        if request.method == 'POST':
            current_jwt = request.POST.get('jwt', None)
            current_voice = request.POST.get('voice', None)
            # 校验JWT
            if(_checkJWT(current_jwt)):
                # 合法JWT
                temp_jwt = _decodeJWT(current_jwt)
                current_id = temp_jwt['id']
                current_name = temp_jwt['name']
                current_c_class = temp_jwt['c_class']
                # 获取对应的学生
                current_student = Student.objects.filter(
                    name=current_name, id=current_id, c_class=current_c_class)
                if current_student and len(current_student) == 1:
                    current_student = current_student[0]
                    current_student.voice = current_voice
                    # 更新最高纪录
                    if(int(current_voice) > int(current_student.record)):
                        current_student.record = current_voice
                    current_student.save()
                    # 返还参数赋值
                    return_state = 1
                    return_msg = "success"
                    return_voice = current_voice
                    return_name = current_name
                    return_id = current_id
                    return_class = current_c_class
            else:
                # 校验不通过
                return_state = 2
                return_msg = "auth fail"
        else:
            return_state = 3
            return_msg = "error method"
        return JsonResponse({
            "state": return_state,
            "content": {
                "msg": return_msg,
                "voice": return_voice,
                "name": return_name,
                "id": return_id,
                "class": return_class
            }
        })
    except Exception as e:
        return error_handler(e)


def getVoiceByClassView(request):
    # 通过班级获取声音数据集
    # 初始化返还参数
    return_state = 9
    return_msg = ""
    return_class = ""
    return_voice_list = []
    if request.method == 'POST':
        current_class = request.POST.get('class', None)
        # 校验JWT
        if current_class:
            current_students = Student.objects.filter(c_class=current_class)
            if current_students:
                for student in current_students:
                    temp_voice = {
                        "classid": student.c_class_id,
                        "name": student.name,
                        "voice": student.voice,
                        "record": student.record
                    }
                    return_voice_list.append(temp_voice)
                return_state = 1
                return_msg = "success"
                return_class = current_class
            else:
                return_state = 2
                return_msg = "no data"
    else:
        return_state = 3
        return_msg = "method error"
    return JsonResponse({
        "state": return_state,
        "content": {
            "msg": return_msg,
            "class": return_class,
            "voice_list": return_voice_list
        }
    })

def testErr(request):
    # 测试错误处理
    raise Exception("test error")