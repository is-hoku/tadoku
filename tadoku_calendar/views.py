import datetime
from django.shortcuts import redirect, render
from django.views import generic
from .forms import SimpleScheduleForm
from .models import Schedule
from . import mixins
from django.contrib import messages
from django.urls import reverse_lazy, reverse
# import matplotlib.pyplot as plt
# import numpy as np
import os
import io
from django.http import HttpResponse
from django.db.models import Sum
from django.core.files import File
# from django.contrib.auth.mixins import LoginRequiredMixin


class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'tadoku_calendar/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        # if os.path.exists('tadoku_calendar/static/images/graph.svg')==True:
        #     os.remove('tadoku_calendar/static/images/graph.svg')
        if self.request.user.is_authenticated:
            if Schedule.objects.filter(user=self.request.user).exists()==True:
                queryset = Schedule.objects.filter(user=self.request.user).values('pk', 'date', 'word_cnt')
                # model_count = queryset.count()
                # context['mojisu'] = queryset
                # context['modelkazu'] = model_count
                querylist = []
                for i in queryset:
                    querylist.append(i)
                context['lis'] = querylist

                sum_word = Schedule.objects.filter(user=self.request.user).aggregate(word=Sum('word_cnt'))
                context['sum'] = sum_word['word']
            else:
                context['sum'] = 0
            # context['year_month'] = list(self.kwargs['year'], self.kwargs['month'])
            return context
        else:
            context['sum'] = 0
            return context



class AddView(generic.CreateView, mixins.MonthCalendarMixin):
    template_name = 'tadoku_calendar/forms.html'
    model = Schedule
    fields = ['date', 'title', 'series', 'level', 'word_cnt', 'evaluation', 'coment']
    success_url  = '/tadoku'
    form = SimpleScheduleForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context
    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(AddView, self).form_valid(form)

    
class DeleteView(generic.DeleteView, mixins.MonthCalendarMixin):
    model = Schedule
    template_name = 'tadoku_calendar/delete.html'
    success_url = '/tadoku'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context
    
class ChangeView(generic.UpdateView, mixins.MonthCalendarMixin):
    template_name = 'tadoku_calendar/forms.html'
    model = Schedule
    fields = ['date', 'title', 'series', 'level', 'word_cnt', 'evaluation', 'coment']
    success_url  = '/tadoku'
    form = SimpleScheduleForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class DetailView(generic.DetailView, mixins.MonthCalendarMixin):
    template_name = 'tadoku_calendar/detail.html'
    model = Schedule
    fields = ['date', 'title', 'series', 'level', 'word_cnt', 'evaluation', 'coment']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context



class GraphView(mixins.MonthCalendarMixin, generic.TemplateView):
    """グラフと統計情報を表示する"""
    template_name = 'tadoku_calendar/graph.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        b_year = self.get_month_calendar()

        if self.request.user.is_authenticated:
            if Schedule.objects.filter(date__year=self.kwargs['year'], date__month=self.kwargs['month'], user=self.request.user).exists()==True:
                date_list = Schedule.objects.filter(date__year=self.kwargs['year'], date__month=self.kwargs['month'], user=self.request.user).values_list('date', flat=True)
                word_cnt_list = Schedule.objects.filter(date__year=self.kwargs['year'], date__month=self.kwargs['month'], user=self.request.user).values_list('word_cnt', flat=True)

                datelist = []
                for j in date_list:
                    datelist.append(j.day)
                # datelist.sort()
                
                context['dlis'] = datelist
                context['wordlis'] = list(word_cnt_list)
                context['max'] = max(word_cnt_list)
                context['step'] = round(max(word_cnt_list)//len(word_cnt_list))*3
                sum_word = Schedule.objects.filter(date__year=self.kwargs['year'], date__month=self.kwargs['month'], user=self.request.user).values_list('word_cnt', flat=True).aggregate(word=Sum('word_cnt'))
                sum_word_b = Schedule.objects.filter(date__year=b_year['month_previous'].year, date__month=b_year['month_previous'].month, user=self.request.user).values_list('word_cnt', flat=True).aggregate(word=Sum('word_cnt'))
                context['sum'] = sum_word['word']
                if Schedule.objects.filter(date__year=b_year['month_previous'].year, date__month=b_year['month_previous'].month, user=self.request.user).exists() == True:
                    sum_word_b = Schedule.objects.filter(date__year=b_year['month_previous'].year, date__month=b_year['month_previous'].month, user=self.request.user).values_list('word_cnt', flat=True).aggregate(word=Sum('word_cnt'))
                else:
                    sum_word_b['word'] = 0
                context['sumb'] = sum_word['word'] - sum_word_b['word']

                context['books'] = Schedule.objects.filter(date__year=self.kwargs['year'], date__month=self.kwargs['month'], user=self.request.user).count()
                context['total_w'] = Schedule.objects.filter(user=self.request.user).aggregate(word=Sum('word_cnt'))['word']
                context['total_b'] = Schedule.objects.filter(user=self.request.user).count()
            
            else:
                context['dlis'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
                context['wordlis'] = [0]*31
                context['max'] = 10000
                context['step'] = 1000
                context['sum'] = 0
                if Schedule.objects.filter(date__year=b_year['month_previous'].year, date__month=b_year['month_previous'].month, user=self.request.user).exists() == True:
                    sum_word_b = Schedule.objects.filter(date__year=b_year['month_previous'].year, date__month=b_year['month_previous'].month, user=self.request.user).values_list('word_cnt', flat=True).aggregate(word=Sum('word_cnt'))
                else:
                    sum_word_b = {'word': 0}
                context['sumb'] = 0 - sum_word_b['word']

                context['books'] = 0
                if Schedule.objects.filter(user=self.request.user).exists()==True:
                    context['total_w'] = Schedule.objects.filter(user=self.request.user).aggregate(word=Sum('word_cnt'))['word']
                else:
                    context['total_w'] = 0
                
                if Schedule.objects.filter(user=self.request.user).exists()==True:
                    context['total_b'] = Schedule.objects.filter(user=self.request.user).count()
                else:
                    context['total_b'] = 0
                # context['total_w'] = Schedule.objects.all().aggregate(word=Sum('word_cnt'))['word']

            return context

        else:
            context['dlis'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
            context['wordlis'] = [0]*31
            context['max'] = 10000
            context['step'] = 1000
            context['sum'] = 0
            context['sumb'] = 0
            context['books'] = 0
            context['total_w'] = 0
            context['total_b'] = 0

            return context

class HelpView(mixins.MonthCalendarMixin, generic.TemplateView):
    template_name = 'tadoku_calendar/help.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context