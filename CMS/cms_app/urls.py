from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView, GenPodDashboard, SubPodDashboard, BrigadDashboard, QADashboard
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('gen_pod_dashboard/', GenPodDashboard.as_view(), name='gen_pod_dashboard'),
    path('sub_pod_dashboard/', SubPodDashboard.as_view(), name='sub_pod_dashboard'),
    path('brigad_dashboard/', BrigadDashboard.as_view(), name='brigad_dashboard'),
    path('qa_dashboard/', QADashboard.as_view(), name='qa_dashboard'),
]
