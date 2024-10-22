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
        check_complete = False,
        archive = False
    )

    new_tod.save()

    return {'new_truth_or_dare': new_tod.json_response()}

@route_get(BASE_URL + 'all')
def all_tod(args):
    tods_list = []

    for tod in TOD.objects.filter(archive = False):
        tods_list.append(tod.json_response())

    return {'all_truths_or_dares': tods_list}

@route_get(BASE_URL + 'one', args={'id': int})
def one_tod(args):
    
    if TOD.objects.filter(id=args['id']).exists():
        one_tod = TOD.objects.get(id=args['id'])

        return {'one_truth_or_dare': one_tod.json_response()}

    else:
        return {'error': 'No truth or dare exists'}

@route_get(BASE_URL + 'random')
def random_tod(args):
    
    random_tod = TOD.objects.filter(archive = False).order_by('?').first()
    return {'random_truth_or_dare': random_tod.json_response()}

@route_post(BASE_URL + 'change_complete', args={'id':int})
def complete_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        complete_tod = TOD.objects.get(id=args['id'])

        complete_tod.change_complete()

        return {'completed_truth_or_dare': complete_tod.json_response()}

    else: 
        return {'error': 'No truth or dare exists'}

@route_get(BASE_URL + 'reject', args={'id':int})
def reject_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        reject_tod = TOD.objects.filter(archive = False).exclude(id=args['id']).order_by('?').first()

        return {'another_truth_or_dare': reject_tod.json_response()}

    else:
        return {'error': 'No truth or dare exists'}

@route_post(BASE_URL + 'change_archive', args={'id':int})
def archive_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        archive_tod = TOD.objects.get(id=args['id'])

        archive_tod.change_archive()

        return {'archived_tod': archive_tod.json_response()}

    else: 
        return {'error': 'No truth or dare exists'}

@route_get(BASE_URL + 'all/truth')
def all_truths(args):
    truth_list = []
    if TOD.objects.filter(truth = True).exists():

        for tods in TOD.objects.filter(truth = True).filter(archive = False):
            truth_list.append(tods.json_response())
            
        return {'all_truths': truth_list}

    else:
        return {'error': 'No truth statements found'}

@route_get(BASE_URL + 'all/dare')
def all_dares(args):
    dare_list = []
    if TOD.objects.filter(dare = True).exists():

        for tods in TOD.objects.filter(dare = True).filter(archive = False):
            dare_list.append(tods.json_response())
            
        return {'all_dares': dare_list}

    else:
        return {'error': 'No dare statements found'}

@route_get(BASE_URL + 'search', args={'keyword':str})
def search_tods(args):
    search_list = []
    if TOD.objects.filter(statement__contains = args['keyword']).exists():
        for search in TOD.objects.filter(statement__contains = args['keyword']).filter(archive = False):
            search_list.append(search.json_response())

        return {'search_list': search_list}

    else:
        return {'search_list': 'No truth or dare exists'}
