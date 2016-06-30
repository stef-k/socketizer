from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from mainsite import models
from mainsite.models import Domain


@method_decorator(login_required, name='dispatch')
class UserProfile(View):
    def get(self, request):
        domains = models.Domain.objects.filter(user=request.user)
        return render(request, 'userprofile.html', {'domains': domains})


@method_decorator(login_required, name='dispatch')
class DomainCreate(CreateView):
    model = models.Domain
    template_name = 'domain-add.html'
    success_url = 'profile'
    fields = ['domain']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.generate_key()
        obj.save()
        messages.success(self.request,
                         'You have successfuly added a new domain')
        return redirect('profile')


@method_decorator(login_required, name='dispatch')
class DomainUpdate(UpdateView):
    model = models.Domain
    template_name = 'domain-add.html'
    success_url = 'profile'
    fields = ['domain']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        messages.success(self.request,
                         'You have successfuly updated the domain')
        return redirect('profile')


@login_required
def regenerate_api_key(request, pk):

    obj = get_object_or_404(Domain, pk=pk)
    obj.generate_key()
    obj.save()
    messages.success(request,
                     "Domain's key changed")
    return redirect('profile')


@login_required
def domain_delete(request, pk):
    get_object_or_404(Domain, pk=pk).delete()
    messages.success(request, "Domain successfuly deleted.")
    return redirect('profile')
