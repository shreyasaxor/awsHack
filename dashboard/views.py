from __future__ import unicode_literals

from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView,View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .utility import pushTos3, reads3, VoicetoText

import pandas as pd
from .vector import text_to_vector, get_cosine
import spacy

@method_decorator(csrf_exempt, name='dispatch')
class SaveFile(View):
    # parser_classes = (MultiPartParser, )

    def get(self,request,*args,**kwargs):
        """get method reterive all users"""
        return Response({"test":"Shreyas"})


    def post(self,request,*args,**kwargs):
        folder = 'media/'
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
            filename = fs.save(myfile.name, myfile)
            file_url = fs.url(filename)
            # pushTos3(file_url,filename)
            return JsonResponse({'foo':file_url,'name':filename})


save_file = SaveFile.as_view()





@method_decorator(csrf_exempt, name='dispatch')
class ConvertVoiceText(View):
    def get(self,request,filename,*args,**kwargs):
        # data = reads3(filename)
        # print(data)
        convert_media = 'media/'+filename
        text = VoicetoText(convert_media)
        print(text)
        return JsonResponse({'foo':text})


convert_voice = ConvertVoiceText.as_view()







@method_decorator(csrf_exempt, name='dispatch')
class GetTestCase(View):


    def get(self,request,*args,**kwargs):
        req = "create a log in page with user name and password"
        recommendation = {'testcase': []}
        test_cases = pd.read_csv('media/data/testcases.csv', header=None)

        for test_case in test_cases[0]:
            vector1 = text_to_vector(test_case)
            vector2 = text_to_vector(req)
            cosine = get_cosine(vector1, vector2)
            if (cosine > 0.1):
                recommendation['testcase'].append(test_case)
        return JsonResponse(recommendation)


get_test_case = GetTestCase.as_view()

from _collections import OrderedDict

@method_decorator(csrf_exempt, name='dispatch')
class GetMachineJson(View):

    def post(self,request,*args,**kwargs):
        import json
        data = request.body.decode('utf-8')
        print(data)
        data = json.loads(data)
        nlp = spacy.load('media/model_1')
        output = {}
        # Test your text
        test_text = data['text']
        doc = nlp(test_text)
        id = 1
        for ent in doc.ents:
            data = {'field': '', 'start_index': '', 'end_index': '', 'type': ''}
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
            data['field'] = ent.text
            data['start_index'] = ent.start_char
            data['end_index'] = ent.end_char
            data['type'] = ent.label_

            field_id = "field" + str(id)
            id = id + 1

            output[field_id] = data
        od = OrderedDict()
        unordered ={}
        for key,value in output.items():
            if value['type'] != 'button':
                od[key]=value
            else:
                unordered[key]=value


        for key,value in unordered.items():
                od[key]=value

        return JsonResponse(od,safe=False)

get_machine_json = GetMachineJson.as_view()








class DashBoard(APIView):
    def get(self,request,*args,**kwargs):
        return render(request,template_name='index.html')
dashboard = DashBoard.as_view()
