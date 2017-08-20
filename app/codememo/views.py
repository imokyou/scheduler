# coding=utf8
import traceback
from django.views.decorators.csrf import csrf_exempt
from config import errors
from lib import utils
from dbmodel.models import CodeMemo


@csrf_exempt
def test(request):
    return utils.NormalResp()


@csrf_exempt
def get_codes(request):
    try:
        p = request.GET.get('p', 1)
        n = request.GET.get('n', 7)

        q = CodeMemo.objects
        results = q.all()[n*(p-1): n*p]
        data = []
        for r in results:
            info = {
                'id': r.id,
                'ctype': r.ctype,
                'description': r.description,
                'content': r.content,
                'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': ''
            }
            try:
                info['updated_at'] = r.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
            data.append(info)
        return utils.NormalResp(data)
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


@csrf_exempt
def add_codememo(request):
    try:
        ctype = request.POST.get('ctype', '')
        description = request.POST.get('description', '')
        content = request.POST.get('content', '')
        if not ctype or not description or not content:
            return utils.ErrResp(errors.ArgMis)

        s = CodeMemo(
            ctype=ctype,
            description=description,
            content=content
        )
        s.save()
        return utils.NormalResp({'id': s.id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


@csrf_exempt
def update_codememo(request, id):
    try:
        try:
            code = CodeMemo.objects.get(id=id)
        except:
            return utils.ErrResp(errors.DataNotExists)

        code.ctype = request.POST.get('ctype', code.ctype)
        code.description = request.POST.get('description', code.description)
        code.content = request.POST.get('content', code.content)
        code.save()
        return utils.NormalResp({'id': code.id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)


@csrf_exempt
def delete_codememo(request, id):
    try:
        try:
            code = CodeMemo.objects.get(id=id)
        except:
            return utils.ErrResp(errors.DataNotExists)
        code.delete()
        return utils.NormalResp({'id': code.id})
    except:
        traceback.print_exc()
        return utils.ErrResp(errors.SthWrong)
