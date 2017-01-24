import json
import webob

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
from pigs.models import Pig

#@csrf_exempt
#def index(request):
#    if request.method == 'POST':
#        return self.action(request)
#
#    if request.method == 'GET':
#        return self.list
#    return HttpResponse("pigs are here: ....")

#@csrf_exempt
#def create(request):
#    return HttpResponse("pigs created")

@csrf_exempt
def index(request):
    pig_controller = PigsController(request)
   # return HttpResponse("pigs are here: ....")
    if request.method == 'GET':
        return pig_controller.index(request)


@csrf_exempt
def detail(request):
    return HttpResponse("pigs created")
    
class PigsController(object): 

    _pig_keys = ['created_at', 'uuid', 'ear_tag','updated_at',
                'pig_type', 'location_id', 'manager_id']

    def __init__(self, args, **kwargs):
        pass

    def _format_pig(self, pig):
        pig_info = dict()
        for key in self._pig_keys:
            pig_info[key] = pig.get(key, None)

        return pig_info

    def index(self, req):
        pigs = Pig.objects.all()

        pigs_info = [self._format_pig(pig) for pig in pigs]
        content = json.dumps({'Pigs': pigs_info})
        response = HttpResponse(content=content)
        return response

    def create(self, req):
        pass
