from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from .forms import SignupForm
from tadoku_calendar import mixins
from .models import CustomUser
from tadoku_calendar.models import Schedule
from django.db.models import Sum
# Create your views here.

class Login(LoginView, mixins.MonthCalendarMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class Logout(LogoutView, mixins.MonthCalendarMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class Password(PasswordChangeView, mixins.MonthCalendarMixin):
    success_url = reverse_lazy('accounts:password_change_done')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class PasswordDone(PasswordChangeDoneView, mixins.MonthCalendarMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class SignupView(CreateView, mixins.MonthCalendarMixin):
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class UserProfile(TemplateView, mixins.MonthCalendarMixin):
    template_name = 'registration/profile.html'
    # model = CustomUser
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        

        if self.request.user.is_authenticated:
            if Schedule.objects.filter(user=self.request.user).exists()==True:
                total = Schedule.objects.filter(user=self.request.user).aggregate(word=Sum('word_cnt'))['word']
                context['total'] = total
                if total <= 10000:
                    context['rank'] = 'gray'
                elif total <= 30000:
                    context['rank'] = 'brown'
                elif total <= 100000:
                    context['rank'] = 'green'
                elif total <= 300000:
                    context['rank'] = 'skyblue'
                elif total <= 1000000:
                    context['rank'] = 'blue'
                elif total <= 3000000:
                    context['rank'] = 'yellow'
                elif total <= 5000000:
                    context['rank'] = 'orange'
                else:
                    context['rank'] = 'red'

            else:
                context['total'] = 0
                context['rank'] = 'white'

        return context


class UserEditView(UpdateView, mixins.MonthCalendarMixin):
    form = SignupForm
    model = CustomUser
    success_url = reverse_lazy('accounts:profile')
    template_name = 'registration/signup.html'
    fields = ['username', 'email']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class RePassword(PasswordResetView, mixins.MonthCalendarMixin):
    success_url = reverse_lazy('password_reset_done')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class RePasswordDone(PasswordResetView, mixins.MonthCalendarMixin):
    template_name = 'registration/password_reset_done.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class RePasswordConfirm(PasswordResetConfirmView, mixins.MonthCalendarMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class RePasswordComp(PasswordResetCompleteView, mixins.MonthCalendarMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class UserDelete(DeleteView, mixins.MonthCalendarMixin):
    model = CustomUser
    template_name = 'registration/delete.html'
    success_url = '/tadoku'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)

        return context