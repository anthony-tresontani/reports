from django.conf.urls.defaults import patterns, include, url
from report_tracking.views import ReportTrackingDetailView, ReportTrackingView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boot.views.home', name='home'),
     url(r'^reports/', ReportTrackingView.as_view(), name="report-lists"),
     url(r'^report/(?P<pk>\d+)/$', ReportTrackingDetailView.as_view(), name="report-download"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
