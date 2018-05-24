from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from CouncilTag.api import views

urlpatterns = [
    url(r'^agendas/$',views.AgendaView.as_view()),
    url(r'^tags/$', views.TagView.as_view()),
    url(r'^login/$',views.login_user),
    url(r'^signup/$', views.signup_user),
    url(r'^feed/$', views.UserFeed.as_view()),
    url(r'^tag/(?P<tag_name>[a-zA-Z _]+)/agenda/items', views.get_agendaitem_by_tag),
    url(r'^user/add/tag/$', views.add_tag_to_user),
    url(r'^user/del/tag/$', views.del_tag_from_user),
    url(r'^add/message/$', views.add_message),
]

urlpatterns = format_suffix_patterns(urlpatterns)