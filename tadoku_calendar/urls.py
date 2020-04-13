from django.urls import path
from . import views


app_name = 'tadoku_calendar'
urlpatterns = [
    path('', views.MonthCalendar.as_view(), name='month'),
    path('<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('schedule_add/', views.AddView.as_view(), name='add'),
    path('schedule_delete/<int:pk>', views.DeleteView.as_view(), name='delete'),
    path('schedule_change/<int:pk>', views.ChangeView.as_view(), name='change'),
    path('schedule_detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('graph/<int:year>/<int:month>/', views.GraphView.as_view(), name='graph'),
    path('help/', views.HelpView.as_view(), name='help'),
]