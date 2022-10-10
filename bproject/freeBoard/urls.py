from django.urls import path,include
from . import views

app_name="freeBoard"
urlpatterns = [
    path('<int:nowpage>/<str:category>/<str:sword>/fboardList',views.fboardList,name="fboardList"),
    path('<int:nowpage>/<str:category>/<str:sword>/fboardWrite',views.fboardWrite,name="fboardWrite"),
    path('<int:nowpage>/<str:category>/<str:sword>/<str:b_no>/fboardView',views.fboardView,name="fboardView"),
    path('<int:nowpage>/<str:category>/<str:sword>/<str:b_no>/fboardUpdate',views.fboardUpdate,name="fboardUpdate"),
    path('<int:nowpage>/<str:category>/<str:sword>/<str:b_no>/fboardDelete',views.fboardDelete,name="fboardDelete"),
    path('<int:nowpage>/<str:category>/<str:sword>/<str:b_no>/fboardReply',views.fboardReply,name="fboardReply"),
    # event
    path('event/',views.event,name="event"),
    path('<str:b_no>/eventView/',views.eventView,name="eventView"),
    # ajax event
    path('commList/',views.commList,name="commList"),
    path('commWrite/',views.commWrite,name="commWrite"),
    path('commUpdate/',views.commUpdate,name="commUpdate"),
    path('commDelete/',views.commDelete,name="commDelete"),
    path('commPost/',views.commPost,name="commPost"),
    
    # 공공데이터
    path('publicList/',views.publicList,name="publicList"),
    
]