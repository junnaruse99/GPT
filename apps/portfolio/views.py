from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import openai
from rest_framework.decorators import api_view
import traceback
from apps.portfolio.serializers import MessageSerializer
from portfolio.models import Message
from django.core import serializers
import json
import uuid
from datetime import datetime,timezone
import os
import environ

env = environ.Env()
environ.Env.read_env()

openai.api_key = env('OPENAI_KEY')

RATE_LIMIT = int(env('RATE_LIMIT'))

class RateLimitExceeded(Exception):
    def __init__(self, message="Rate limit exceeded", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        
def index(request):
    return HttpResponse("Hello, world. You're at the portfolio index.")
  
@api_view(['GET', 'POST', 'DELETE'])
def message(request):
    try:
        if request.method == 'GET':
            return getMessage(request)
        elif request.method == 'POST':
            return createMessage(request)
        elif request.method == 'DELETE':
            return deleteMessage(request)
    except RateLimitExceeded as ex:
        return HttpResponse(content=ex, status="429")
    except Exception as ex:
        print(traceback.format_exc())
        return HttpResponse(content="Unexpected error", status="400")
        
    return HttpResponse(content="Method does not exists", status="400")

def getMessage(request):
    sessionId = request.GET.get('sessionId')
    query = Message.objects.filter(sessionId=sessionId).order_by("createdOn")
    data = MessageSerializer(query, many=True).data
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", status="200")

def createMessage(request):
    data = json.loads(request.body)
    prompt = data['prompt']
    if ('sessionId' in data):
        sessionId = data['sessionId']
    else:
        sessionId = None
    response = get_completion(prompt, sessionId)
    return HttpResponse(content=response, status="200", content_type='application/json')

def deleteMessage(request):
    return HttpResponse(status="200")

def get_completion(prompt, sessionId):
    # Get the current UTC date
    current_date_utc = datetime.now(timezone.utc).date()

    previousMessages = []
    if sessionId:
        previousMessages = Message.objects.filter(sessionId=sessionId)
        
    if (len(previousMessages.filter(createdOn__date=current_date_utc)) > RATE_LIMIT):
        raise RateLimitExceeded("Rate limit exceeded")
    
    sessionId = sessionId or uuid.uuid4()
        
    module_dir = os.path.dirname(__file__)  # get current directory
    promptFile_path = os.path.join(module_dir, 'systemPrompt.txt')

    f = open(promptFile_path, "r")
    
    messages = [{"role": "system", "content": "{}".format(f.read())}]
    for item in previousMessages:
        description = item.description
        response = item.response
        
        user_prompt = {"role": "user", "content": description}
        assistant_prompt = {"role": "assistant", "content": response}
        
        messages.append(user_prompt)
        messages.append(assistant_prompt)

    messages.append({"role": "user", "content": "{}".format(prompt)})
    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    response = query.choices[0].message.content
        
    message = Message(sessionId=sessionId, createdOn=datetime.now(timezone.utc), description=prompt, response=response)
    message.save()
    
    return json.dumps(MessageSerializer(message).data, ensure_ascii=False)