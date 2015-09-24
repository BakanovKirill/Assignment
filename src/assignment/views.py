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
    events = Event.objects.all().prefetch_related('product_items').select_related('fee__currency')
    if request.method == 'POST':
        try:
            event = events.get(pk=request.POST.get('id',0))
        except ObjectDoesNotExist:
            raise Http404
        total = calculate_total_fast(event).quantize(Decimal('0.01'))
        # We could also check if the total is already saved, but in this simple case there is no handlers
        # for Product change events to clear total. So we calculate and save it each time.
        # To go another way i'd use post_save() signal on ProductItem
        event.total = total
        event.save()
        return JsonResponse({'total': total})
    data['events'] = events

    return data