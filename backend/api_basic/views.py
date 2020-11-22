from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.status import HTTP_404_NOT_FOUND
from .serializers import TrendingTweetsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from backend import generateHashTags
from predictor import process
import json
import threading



regenerate = False



class TrendingTweetsView(APIView):
    
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = TrendingTweetsSerializer(data=request.data)
        if serializer.is_valid():
            global regenerate
            serializer.save()
            region = serializer.data['region']
            if regenerate:
                regenerate = False
               # timerObject = Timer(30, timeout_callback)
                generateHashTags(region)
            cluster_dict = process()
            file_name = "twitter_"+region+"_trend.json"
            #f = open(file_name)
            #data = json.load(f)
            #f.close()
            
            #data.append(cluster_dict)
            return Response(cluster_dict, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

