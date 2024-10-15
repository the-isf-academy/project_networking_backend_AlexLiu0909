# views.py

from banjo.urls import route_get, route_post
from .models import TOD
from settings import BASE_URL

@route_post(BASE_URL + 'new', args={'statement':str, 'truth':bool, 'dare':bool})
def new_tod(args):
    new_tod = TOD(
        statement = args['statement'],
        truth = args['truth'],
        dare = args['dare'],
    )

    new_tod.save()

    return {'truth_or_dare': new_tod.json_response()}

@route_get(BASE_URL + 'all')
def all_tod(args):
    # if TOD.objects.exists():
    tods_list = []

    for tod in TOD.objects.all():
        tods_list.append(tod.json_response())

    return {'truth_or_dare': tods_list}

    # else:
    #     return{'error': 'No truth or dare exists'}

# @route_get(BASE_URL + 'reject', args={'id':int, 'truth':bool, 'dare':bool})
# def reject_tod(args):
    
