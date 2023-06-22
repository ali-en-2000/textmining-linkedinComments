from django.urls import path, include
from . import views
from crawler.views import post_list

urlpatterns = [
    path('add/', views.addPostView.as_view()),
    path('comments/', views.GetCommmentsView.as_view(), name='get_comments_by_url'),
    path('commentsMined/', views.GetCommmentsDataminedView.as_view(), name='get_commentsmined_by_url'),
    path('getcommentsMined/', views.GetCommmentsMindedView.as_view(), name='getall_commentsmined_by_url'),
    path('urls/', post_list, name='get_url'),
    path('delete/', views.deleteCommmentsView.as_view(), name='delete_comment'),

]