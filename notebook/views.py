from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView, ListView
from django.views import View
from .models import Narrative
from .forms import NarrativeWrite
import json
import uuid


class NarrativeView:
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
        paginate_by = 3
        ordering = ('created_at',)

        def get_queryset(self):
            return Narrative.objects.filter(sketch=False, author__isnull=False).order_by('-created_at')

class NarrativeFactory:
    class New(View):
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
                    narrative.author = request.user
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
                    narrative.author = request.user
                    narrative.save()
                return HttpResponse('skec')
            else:
                return HttpResponse('Unknown')


    class Write(View):
        template_name = 'notebook/narrative/folder.html'
        def get(self, request):
            if not request.user.is_authenticated:
                return HttpResponse("Prohibited", status_code=403)
            sketches = Narrative.objects.filter(sketch=True, author=request.user)
            return render(request, self.template_name, {
                'sketches': sketches,
                'no_sketch': not sketches.exists(),
            })
    
    class Sketch(DetailView):

        template_name = 'notebook/narrative/write.html'
        
        def get(self, request, slug):
            narrative = Narrative.objects.get(slug=slug)
            form = NarrativeWrite(instance=narrative)
            return render(request, self.template_name, {'form': form})

        def post(self, request, slug):
            narrative = Narrative.objects.get(slug=slug)
            form = NarrativeWrite(request.POST, instance=narrative)
            if not form.is_valid():
                print(form.errors)
            action = request.POST.get('action', '')
            narrative = form.save(commit=False)
            submitted = action == 'SUBMIT'
            if submitted:
                narrative.sketch = False

            narrative.save(alter_slug=submitted)
            return HttpResponse()
        
