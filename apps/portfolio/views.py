from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import openai

openai.api_key = 'YOUR_API_KEY'

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_completion(prompt):
    print(prompt)
    query = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
  
    response = query.choices[0].text
    print(response)
    return response
  
  
def query_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        return JsonResponse({'response': response})
    return render(request, 'index.html')