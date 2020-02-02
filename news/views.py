from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Report, LoginForm


def user_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(
            request,
            'news/login.html',
            {
                'form':form
            }
        )
    elif request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('news:index'))
            else:
                messages.error(request, _("用户名或密码错误。"))
                return redirect(reverse('news:login'))
        else:
            messages.error(request, _("数据错误。"))
            return redirect(reverse('news:login'))
    else:
        return HttpResponseBadRequest


@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        source = request.GET.get('source')

        filter_kwargs = {}
        if source:
            filter_kwargs['source'] = source
        report_set = Report.objects.filter(**filter_kwargs).order_by("-datetime")

        paginator = Paginator(report_set, 20)
        page = request.GET.get('page')
        reports = paginator.get_page(page)

        admin_url = '/' + settings.ADMIN_URL + '/'

        if page is None:
            page = '1'
        return render(
            request,
            'news/index.html',
            {
                'reports': reports,
                'page': page,
                'source': source,
                'admin_url': admin_url,
            }
        )
    else:
        return HttpResponseBadRequest