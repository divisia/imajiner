from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView, ListView
from django.views import View
from .models import Narrative
from .forms import NarrativeWrite
import json
import uuid


class NarrativeViews:
    class Detail(DetailView):
        model = Narrative
        context_object_name = 'narrative'
        template_name = 'notebook/narrative/detail.html'

        def get_object(self):
            self.slug = self.kwargs['slug']
            self.narrative = Narrative.objects.get(slug=self.slug)
            return self.narrative
        
        def post(self, request, *args, **kwargs):
            action = request.POST['action']
            payload = json.loads(request.POST['payload'])
            if action == 'TAGDELTA':
                for slug, delta in payload.items():
                    self.tag_delta(slug, delta)
            return HttpResponse()
        

        def tag_delta(self, slug, amount=1):
            user = self.request.user
            if not user.is_authenticated:
                return False
            user.tags.delta(
                slug=slug,
                diff=amount,
                narrative=self.kwargs['slug']
            )

    class List(ListView):
        model = Narrative
        context_object_name = 'narratives'
        template_name = 'notebook/narrative/list.html'

        def get_queryset(self):
            return Narrative.objects.all()
    
    class Write(View):
        template_name = 'notebook/narrative/write.html'

        def get(self, request):
            form = NarrativeWrite()
            return render(self.request, self.template_name, context={'form':form})

        def post(self, request):

            form = NarrativeWrite(request.POST)
            action = request.POST.get('action', 'SUBMIT')
            count = int(request.POST.get('count', 1))
            

            if not form.is_valid():
                return render(self.request, self.template_name, context={'form':form})
            
            if action == 'SUBMIT':
                if count > 0:
                    uid = request.POST.get('uuid')
                    uid = uuid.UUID(bytes=bytes(uid[-16:].encode()))
                    narrative = Narrative.objects.get(uuid=uid)
                    form = NarrativeWrite(request.POST, instance=narrative)
                    narrative = form.save(commit=False)
                    narrative.sketch = False
                    narrative.save()
                
                else:
                    uid = request.POST.get('uuid')
                    uid = uuid.UUID(bytes=bytes(uid[-16:].encode()))
                    form = NarrativeWrite(request.POST)
                    narrative = form.save(commit=False)
                    narrative.uuid = uid
                    narrative.sketch = False
                    narrative.save()


                form.save()
                return HttpResponse('Kaydettim')
            
            elif action == 'AUTOSAVE':
                
                if count > 0:
                    uid = request.POST.get('uuid')
                    uid = uuid.UUID(bytes=bytes(uid[-16:].encode()))
                    narrative = Narrative.objects.get(uuid=uid)
                    form = NarrativeWrite(request.POST, instance=narrative)
                    if not narrative.sketch:
                        raise Exception('Wait a second!')
                    form.save()
                else:
                    uid = request.POST.get('uuid')
                    uid = uuid.UUID(bytes=bytes(uid[-16:].encode()))
                    form = NarrativeWrite(request.POST)
                    narrative = form.save(commit=False)
                    narrative.uuid = uid
                    narrative.sketch = True
                    narrative.save()
                return HttpResponse('skec')
            else:
                return HttpResponse('Unknown')


            """form = NarrativeWrite(request.POST)
            if not form.is_valid():
                return HttpResponse("I've never met this man in my life")
            action = request.POST.get('action', '')
            subsequent = request.POST.get('subsequent', False)
            narrative = form.save(commit=False)
            narrative.generate_slug()
            print("incomin", narrative, "checkn")
            qs = Narrative.objects.filter(slug=narrative.slug)
            if qs.exists():
                print("oh found")
                narrative = NarrativeWrite(request.POST, instance=qs.first()).save(commit=False)
            if action == 'AUTOSAVEFORM':
                narrative.sketch = True
            narrative.save()
            return HttpResponse("tamam bebek kaydettim")"""
