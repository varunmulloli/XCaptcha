from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('captcha.views',
    url(r'image/(?P<key>\w+)/$','captcha_image',name='captcha-image'),
)
