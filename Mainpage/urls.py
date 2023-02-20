from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.Homepage,name="Homepage"),
    path('upload_file/',views.UploadFile,name="UploadFile"),
    path('HandlePassword/',views.HandlePassword,name="HandlePassword"),
    path('LinkScript/',views.LinkScript,name="LinkScript"),
    path('about/',views.Aboutpage,name="Aboutpage"),
    path('profile/',views.ProfilePage,name="ProfilePage"),
    path('edit/',views.EditProfile,name="EditProfile"),
    path('logout/',views.logout_page,name="logout_page"),
    path('editpage/',views.editpage,name="editpage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)