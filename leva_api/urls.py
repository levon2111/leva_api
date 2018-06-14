from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from apps.core.urls import generate_url
from apps.users.views import UsersViewSet, CreateSyndicateViewSet, UpdateSyndicateViewSet, GetUserSyndicates, \
    SyndicateMemberViewSet

schema_view = get_swagger_view(title='Leva API')

router = DefaultRouter()
router.register(r'users', UsersViewSet, base_name='users')
router.register(r'create-syndicate', CreateSyndicateViewSet, base_name='create-syndicate')
router.register(r'update-syndicate', UpdateSyndicateViewSet, base_name='update-syndicate')
router.register(r'get-syndicate', GetUserSyndicates, base_name='get-syndicate')
router.register(r'syndicate-member', SyndicateMemberViewSet, base_name='syndicate-member')

urlpatterns = [
    url(r'^$', schema_view),
    generate_url('auth-users/', include(('apps.users.urls', 'auth-users'), namespace='auth-users')),
    generate_url('core/', include(('apps.core.urls', 'core'), namespace='core')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
