from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse

from annoying.decorators import render_to

from assignment.models import Event
from assignment.utils import calculate_total_fast


@render_to('index.html')
def index(request):
    data = {

    }
    events = Event.objects.all().prefetch_related('product_items')
    if request.method == 'POST':
        try:
            event = events.get(pk=request.POST.get('id',0))
        except ObjectDoesNotExist:
            raise Http404
        total = calculate_total_fast(event).quantize(Decimal('0.01'))
        event.total = total
        event.save()
        #calculate_total_simple(event)
        return JsonResponse({'total': total})
    data['events'] = events

    return data