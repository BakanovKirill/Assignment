from annoying.decorators import render_to
from models import Event


@render_to('index.html')
def index(request):
    data = {}
    event = Event.objects.all().select_related('fee').prefetch_related('product_items')
    if event.exists():
        event = event[0]
        items = event.product_items.all().select_related('product')
        data['event'] = event
        data['items'] = items
    return data