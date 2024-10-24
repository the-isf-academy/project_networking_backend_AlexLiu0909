# views.py

from banjo.urls import route_get, route_post
from .models import TOD
from settings import BASE_URL

# This route allows users to add new statements to the database.
@route_post(BASE_URL + 'new', args={'statement':str, 'truth':bool, 'dare':bool})
def new_tod(args):
    new_tod = TOD(
        statement = args['statement'],
        truth = args['truth'],
        dare = args['dare'],
        must_complete = False,
        check_complete = False,
        reject = False
    )

    new_tod.save()

    return {'new_truth_or_dare': new_tod.json_response()}

# This route allows users to view all of the statements in the database.
@route_get(BASE_URL + 'all', args={'must_complete': bool})
def all_tod(args):
    tods_list = []

    if TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']):

        for tod in TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']):
            tods_list.append(tod.json_response())

        return {'all_truths_or_dares': tods_list}

    else: 
        return {'error': 'No truth or dare exists'}

# This route allows users to view one specific statements from the database.
@route_get(BASE_URL + 'one', args={'id': int, 'must_complete': bool})
def one_tod(args):
    
    if TOD.objects.filter(must_complete = args['must_complete']).filter(id=args['id']).exists():
        one_tod = TOD.objects.filter(must_complete = args['must_complete']).get(id=args['id'])

        return {'one_truth_or_dare': one_tod.json_response()}

    else:
        return {'error': 'No truth or dare exists'}

# This route selects a random statement from the database for the user to view.
@route_get(BASE_URL + 'random', args={'must_complete': bool})
def random_tod(args):
    
    if TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']):
        random_tod = TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']).order_by('?').first()
        return {'random_truth_or_dare': random_tod.json_response()}

    else: 
        return {'error': 'No truth or dare exists'}

# This route modifies the 'check_complete' field of a chosen statement for the user, marking the completion status of the statement.
@route_post(BASE_URL + 'change_complete', args={'id':int})
def complete_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        complete_tod = TOD.objects.get(id=args['id'])

        complete_tod.change_complete()
        complete_tod.reset_must_complete() # Since the statement is complete, here it sets the 'must_complete' field back to false, indicating the completion of the statement and that the user can move on.

        return {'completed_truth_or_dare': complete_tod.json_response()}

    else: 
        return {'error': 'No truth or dare exists'}

# This route allows the user to reject and hide a certain statement that is presented to them through its id, and generates another statement from the database for the user. However, it also changes the 'must_complete' field of the newly selected statement from false to true, indicating that the user must respond to the statement before continuing the game.
@route_post(BASE_URL + 'reject', args={'id':int})
def reject_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        reject_tod = TOD.objects.get(id=args['id'])

        reject_tod.change_reject()

        switch_tod = TOD.objects.filter(reject = False).order_by('?').first()
        switch_tod.change_must_complete() # Sets this statement to mandatory by changing the 'must_complete' field from false to true, meaning that the user has to respond to the statement before moving on. 
        return {'another_must_do_truth_or_dare': switch_tod.json_response()}

    else: 
        return {'error': 'No truth or dare exists'}

# This route filters statements that are categorized as 'truth' for the user to view.
@route_get(BASE_URL + 'all/truth', args={'must_complete': bool})
def all_truths(args):
    truth_list = []
    if TOD.objects.filter(truth = True).filter(must_complete = args['must_complete']).exists():

        for tods in TOD.objects.filter(truth = True).filter(reject = False).filter(must_complete = args['must_complete']):
            truth_list.append(tods.json_response())
            
        return {'all_truths': truth_list}

    else:
        return {'error': 'No truth statements found'}

# This route filters statements that are categorized as 'dare' for the user to view.
@route_get(BASE_URL + 'all/dare', args={'must_complete': bool})
def all_dares(args):
    dare_list = []
    if TOD.objects.filter(dare = True).filter(must_complete = args['must_complete']).exists():

        for tods in TOD.objects.filter(dare = True).filter(reject = False).filter(must_complete = args['must_complete']):
            dare_list.append(tods.json_response())
            
        return {'all_dares': dare_list}

    else:
        return {'error': 'No dare statements found'}

# This route searches in the database for statements that contain the user's specified keyword.
@route_get(BASE_URL + 'search', args={'keyword':str, 'must_complete': bool})
def search_tods(args):
    search_list = []
    if TOD.objects.filter(statement__contains = args['keyword']).filter(reject = False).filter(must_complete = args['must_complete']).exists():
        for search in TOD.objects.filter(statement__contains = args['keyword']).filter(reject = False).filter(must_complete = args['must_complete']):
            search_list.append(search.json_response())

        return {'search_list': search_list}

    else:
        return {'search_list': 'No truth or dare exists'}

# This route resets the game status, setting all fields of the completed and/or archived statements back to their original state, then returning a full list of all of the statements in the database.
@route_post(BASE_URL + 'reset_game')
def reset_tods(args):
    reset_list = []

    if TOD.objects.exists():

        for r_reject in TOD.objects.filter(reject = True): 
            r_reject.reset_change_reject() # Resets statements that are previously rejected/archived back to the original state.

        for r_must_complete in TOD.objects.filter(must_complete = True):
            r_must_complete.reset_must_complete() # Resets statements that are previouly set as mandatory back to the original state.

        for r_change_complete in TOD.objects.filter(check_complete = True):
            r_change_complete.reset_change_complete() # Resets statements that are previouly set as complete back to the original state.

        for reset_tod in TOD.objects.all():
            reset_list.append(reset_tod.json_response()) # Adds all of the statements (the reset ones and the normal ones) to a list and demonstrating that all of the statements have been reset.

        return {'reset_truths_or_dares': reset_list}

    else:
        return {'error': 'No truth or dare exists'}

