from django.http import HttpResponse, HttpRequest
import io
import cv2
import base64 
import numpy as np
from PIL import Image
import json
import psycopg2
from .models import Object
from .algorithms import algorithms
from django.http import JsonResponse
# import .algorithms
# from django.views.decorators.csrf import csrf_protect
ALGORITHMS = {
    "features":{
        0: "naive",
        1: "lbp",
        2: "BGR_1_1",
        3: "BGR_1_2",
        4: "BGR_2_1",
        5: "BGR_2_2",
        6: "HSV_1_1",
        7: "HSV_1_2",
        8: "HSV_2_1",
        9: "HSV_2_2",
    },
    "distances":{
        0: "l2_distance",
        1: "histogram_intersection",
    }
}
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# @csrf_protect
def retrieval_insert(request):
    if request.method=="POST":
        data_dict = json.loads(request.body)
        new_id = data_dict['id']
        new_img = data_dict['image']
        new_obj_feature = dict()
        for key in ALGORITHMS['features'].keys():
            method = getattr(algorithms, ALGORITHMS['features'][key])
            method_result = method(toRGB(stringToImage(new_img)))
            if isinstance(method_result, dict):
                new_obj_feature.update(method_result)
            else:
                new_obj_feature[ALGORITHMS["features"][key]] = method_result
        # import ipdb; ipdb.set_trace()
        new_obj = Object.objects.create(object_id = new_id, object_img = new_img, features =new_obj_feature )
        new_obj.save()
        # import ipdb; ipdb.set_trace()
        return HttpResponse("Import image successfully!")

def retrieval_get(request):
    if request.method=="POST":
        try:
            # import ipdb; ipdb.set_trace()
            if request.body ==b'':
                return HttpResponse("You have inserted empty body!")
            data_dict = json.loads(request.body)
            list_object = Object.objects.values_list('object_id',  'features', 'object_img')
            distance_method = getattr(algorithms, ALGORITHMS['distances'][data_dict['distance']])
            feature_method = getattr(algorithms, ALGORITHMS['features'][data_dict['feature']])
            img_feature = feature_method(toRGB(stringToImage(data_dict['image'])))
            list_object = [[element[0], distance_method(img_feature, element[1][ALGORITHMS['features'][data_dict['feature']]]), element[2]] for element in list_object]
            list_object.sort(key=lambda x: x[1])
            list_object = list_object[:min(data_dict['rank'], len(list_object))]
            # import ipdb; ipdb.set_trace()
        # return HttpResponse("Import image successfully!"
            result = {
                'info': 'Retrieval successfully!',
                'data': list_object,
            }
            return JsonResponse(result)
        except Exception as e:
            result = {
                'info': 'Retrieval failed!',
                'data': [],
                'error': e
            }
            return JsonResponse(result)