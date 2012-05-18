from django.views.generic import ListView
from report_tracking.models import ReportTracking

# Create your views here.
class ReportTrackingView(ListView):
    model = ReportTracking

    def post(self, request):
        return self.get(request)
