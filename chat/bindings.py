from channels_framework.bindings import ResourceBinding

from .models import Thread
from .serializers import ThreadSerializer

class ThreadBinding(ResourceBinding):

    model = Thread
    stream = "threads"
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()
