from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from .models import Report, LoginForm, FilterForm


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
        return HttpResponseBadRequest()


@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        source = request.GET.get('source', default='')

        filter_kwargs = {}
        filter_form = FilterForm(request.GET)
        if filter_form.is_valid():
            for k, v in filter_form.cleaned_data.items():
                if v:
                    filter_kwargs[k] = v
        else:
            messages.error(request, _("筛选条件填写错误。"))
        
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
                'filter_form': filter_form,
            }
        )
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/login/')
def detail(request, pk):
    if request.method == 'GET':
        report = get_object_or_404(Report, pk=pk)
        return render(
            request,
            'news/detail.html',
            {
                'report': report,
            }
        )
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/login/')
@permission_required('news.delete_report')
def delete(request, pk):
    if request.method == 'GET':
        # flag
        is_result = False
        report = get_object_or_404(Report, pk=pk)
        return render(
            request,
            'news/delete.html',
            {
                'report': report,
                'is_result': is_result,
            }
        )
    elif request.method == 'POST':
        report = get_object_or_404(Report, pk=pk)
        report.delete()
        is_result = True
        return render(
            request,
            'news/delete.html',
            {
                'report': report,
                'is_result': is_result,
            }
        )
    else:
        return HttpResponseBadRequest()