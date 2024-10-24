# Project Networking



## API Overview
A **"Truth or Dare"** game is usually played within friend groups to encourage people to say things that they may not be willing to tell in a normal setting (truths) or to do something they may not normally do for other people's enjoyment (dare). 

This API hosts statements of *truths* and *dares* and is a helpful tool assisting friend groups to play and customize the game of **"Truth or Dare"**. In one round of the game using this API, you can be allocated a random truth or dare statement to answer or do, add new truths or dares to the database, and hide truth or dare statements that you don't like.

Potential uses of this API include a truth or dare game assistant, a punishment generator, a therapeutic activity tool, a workshop icebreaker, etc. 

### Features
1. Two players will be **randomly selected** out of all the users that are participating in the game. One of the pair is going to be the ***'questioner'***, the other one is going to be the ***'executant'***. 
2. The *executant* chooses whether to do a truth or a dare. Then the *questioner* can enter a statement that they want the *executant* to answer or act.
3. The *executant*, however, is able to choose between accepting or rejeting the statement. If they reject the statement, another truth or dare statement will be selected randomly from the database and presented to the *executant*. Then the person must respond to it this time. 
4. If the *executant* completes the statement, the *questioner* can select 'complete' ('true' for the `check_complete` field) to continue the game. But if the *executant* doesn't achieve what needs to be done, the *questioner* can select 'incomplete' ('false' for the `check_complete` field) to restart the game with the *executant* again (returning to feature 2). 
5. After a full round, the *executant* can add a truth or dare statement to the database/modify a truth or dare statement in the database.

### Server
Here is the [link](http://127.0.0.1:5000/TOD/all) to the server of this API that you can visit in your web browser. 

### Model

#### Fields
In the models.py file, there are 7 fields in total of different field data types in the **TOD** (meaning 'Truth or Dare') **class**. The `id` field is in the default setting of the API. 

```
class TOD(Model):
    statement = StringField()
    truth = BooleanField()
    dare = BooleanField()
    must_complete = BooleanField()
    check_complete = BooleanField()
    reject = BooleanField()
```

| **Field Name** | **Data Type** | **Description** |
|---|---|---|
| `id` | `IntegerField` | A unique identifier for each truth or dare statement, ensuring each entry can be distinctly retrieved or modified. |
| `statement` | `StringField` | The text of the truth or dare statement itself, holding the actual content that the user is going to interact with. |
| `truth` | `BooleanField` | A variable indicating whether the statement presented is a truth (true) or a dare (false), providing categorization of the content for the user. |
| `dare` | `BooleanField` | Similar to the 'truth' field, this variable indicates whether the statement presented is a dare (true) or a truth (false), providing categorization of the content for the user. To clarify, at least one of the `truth` or `dare` fields should be true for a statement. |
| `must_complete` | `BooleanField` | A field that sets the selected statement as mandatory for the user, meaning that the user must complete the chosen statement before moving on to use other routes for viewing other statements. If not completed, users are temporarily not allowed to view any truths or dares except for their own one that they are doing. |
| `check_complete` | `BooleanField` | A field that can be used to mark whether a statement has been answered or completed in a round of game, helping track user progress and ensuring that statements can be revisited or marked as done. If this variable is set as 'false', the executant must complete their truth or dare statement and can't view any other truths or dares until finished (`check_complete` set as 'true'). |
| `reject` | `BooleanField` | A variable that indicates if a statement has been set to hidden (true) or is still active/visible (false), allowing users to reject statements they don't want to answer or complete, without deleting them entirely from the database. |

#### Methods
In the models.py file, there are 8 methods in total in the **TOD** (meaning 'Truth or Dare') **class**.

```
def json_response(self):

    return{
        'id': self.id,
        'statement': self.statement,
        'truth': self.truth,
        'dare': self.dare,
        'must_complete': self.must_complete,
        'check_complete': self.check_complete,
        'reject': self.reject
    }

def change_statement(self, new_statement):
    self.statement = new_statement
    self.save()

def change_must_complete(self):
    self.must_complete = True
    self.save()

def reset_must_complete(self):
    self.must_complete = False
    self.save()

def change_complete(self):
    self.check_complete = True
    self.save()

def reset_change_complete(self):
    self.check_complete = False
    self.save()

def change_reject(self):
    self.reject = True
    self.save()
    
def reset_change_reject(self):
    self.reject = False
    self.save()
```

Here is a table summarizing the meaning and usage of each method.
| **Method Name** | **Parameter** | **Description** |
|---|---|---|
| `json_response` | / | This method generates a clearly-formatted JSON response for a specific truth or dare statement. It takes the `id` to identify the statement and the `truth` and `dare` boolean variables to indicate the type. This is useful for returning structured data to users, allowing them to easily access statement details and information. |
| `change_statement` | `new_statement` | This method allows users to update the text of an existing truth or dare statement. It takes `new_statement` as a parameter, which replaces the original statement. This enables users to edit statements flexibly, ensuring highly-customizable and up-to-date content in the database. |
| `change_must_complete` | / | This method modifies the `must_complete` field of a truth or dare statement from false to true. When this method is used, users must respond to their current chosen statement in order to continue the game. If they don't finish the statement and `must_complete` remains false, they can't use any other routes to view other statements in the database. |
| `reset_must_complete` | / | The opposite of `change_must_complete`, this method changes the `must_complete` field status of a statement from true back to false, sending the statement back to its original status and preparing for the next game. This method should be used after a full round of game when the player has completed their statement. |
| `change_complete` | / | This method switches the completion status of a statement from false to true. It can be used to mark whether the statement is answered or completed by the players, which is useful for tracking user interactions. |
| `reset_change_complete` | / | The opposite of `change_complete`, this method changes the `check_complete` field status of a statement from true back to false, sending the statement back to its original status and preparing for the next game. This method should be used after a full round of game when the player has completed their statement. |
| `change_reject` | / | This method updates the `reject` field status of a statement from false to true, indicating that a statement has been archived temporarily for the round of game. It allows users to effectively manage the visibility of truth or dare statements and avoid ones they don't want to see without deleting them from the database. |
| `reset_change_reject` | / | The opposite of `change_reject`, this method changes the `reject` field status of a statement from true back to false, sending the statement back to its original status and preparing for the next game. This method should be used after a full round of game when the player has completed their statement. |

### Endpoints
In the views.py file, there are 10 endpoints in total. 

#### 1. **`/new`**
```
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
```
> A success JSON response example: 
```
{
  "new_truth_or_dare": {
    "id": 9,
    "statement": "What happened when you cried last time?",
    "truth": true,
    "dare": false,
    "must_complete": false,
    "check_complete": false,
    "reject": false
  }
}
```

---

#### 2. **`/all`**
```
@route_get(BASE_URL + 'all', args={'must_complete': bool})
def all_tod(args):
    tods_list = []
    if TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']).exist():
        for tod in TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']):
            tods_list.append(tod.json_response())
        return {'all_truths_or_dares': tods_list}
    else: 
        return {'error': 'No truth or dare exists'}
```
> A success JSON response example (`must_complete` = False): 
```
{
  "all_truths_or_dares": [
    {
      "id": 1,
      "statement": "State five of your weird habits",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 2,
      "statement": "Text 'I won't be coming home tonight' to mom",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 3,
      "statement": "When was the last time you lied?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 4,
      "statement": "Keep 3 ice cubes in your mouth until they melt",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 5,
      "statement": "What’s the most embarrassing problem you’ve gone to the doctor for?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 6,
      "statement": "What is your biggest fear?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 7,
      "statement": "Eat a bite of a banana peel",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 8,
      "statement": "Show the most embarrassing photo on your phone",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 9,
      "statement": "What happened when you cried last time?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    }
  ]
}
```
> Another success JSON response example (`must_complete` = True):
```
{
  "all_truths_or_dares": [
    {
      "id": 1,
      "statement": "State five of your weird habits",
      "truth": true,
      "dare": false,
      "must_complete": true,
      "check_complete": false,
      "reject": false
    }
  ]
}
```

---

#### 3. **`/one`**
```
@route_get(BASE_URL + 'one', args={'id': int})
def one_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        one_tod = TOD.objects.get(id=args['id'])
        return {'one_truth_or_dare': one_tod.json_response()}
    else:
        return {'error': 'No truth or dare exists'}
```
> A success JSON response example: 
```
{
  "one_truth_or_dare": {
    "id": 1,
    "statement": "State five of your weird habits",
    "truth": true,
    "dare": false,
    "must_complete": false,
    "check_complete": false,
    "reject": false
  }
}
```

---

#### 4. **`/random`**
```
@route_get(BASE_URL + 'random', args={'must_complete': bool})
def random_tod(args):
    if TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']):
        random_tod = TOD.objects.filter(reject = False).filter(must_complete = args['must_complete']).order_by('?').first()
        return {'random_truth_or_dare': random_tod.json_response()}
    else: 
        return {'error': 'No truth or dare exists'}
```
> A success JSON response example (`must_complete` = False): 
```
{
  "random_truth_or_dare": {
    "id": 2,
    "statement": "Text 'I won't be coming home tonight' to mom",
    "truth": false,
    "dare": true,
    "must_complete": false,
    "check_complete": false,
    "reject": false
  }
}
```
> Another success JSON response example (`must_complete` = True): 
```
{
  "random_truth_or_dare": {
    "id": 6,
    "statement": "What is your biggest fear?",
    "truth": true,
    "dare": false,
    "must_complete": true,
    "check_complete": false,
    "reject": false
  }
}
```

---

#### 5. **`/change_complete`**
```
@route_post(BASE_URL + 'change_complete', args={'id':int})
def complete_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        complete_tod = TOD.objects.get(id=args['id'])
        complete_tod.change_complete()
        complete_tod.reset_must_complete()
        return {'completed_truth_or_dare': complete_tod.json_response()}
    else: 
        return {'error': 'No truth or dare exists'}
```
> A success JSON response example:
```
{
  "random_truth_or_dare": {
    "id": 2,
    "statement": "Text 'I won't be coming home tonight' to mom",
    "truth": false,
    "dare": true,
    "must_complete": false,
    "check_complete": false,
    "reject": false
  }
}
```

---

#### 6. **`/reject`**
```
@route_post(BASE_URL + 'reject', args={'id':int})
def reject_tod(args):
    if TOD.objects.filter(id=args['id']).exists():
        reject_tod = TOD.objects.get(id=args['id'])
        reject_tod.change_reject()
        switch_tod = TOD.objects.filter(reject = False).order_by('?').first()
        switch_tod.change_must_complete()
        return {'another_must_do_truth_or_dare': switch_tod.json_response()}
    else: 
        return {'error': 'No truth or dare exists'}
```
> A success JSON response example:
```
{
  "another_must_do_truth_or_dare": {
    "id": 5,
    "statement": "What’s the most embarrassing problem you’ve gone to the doctor for?",
    "truth": true,
    "dare": false,
    "must_complete": true,
    "check_complete": false,
    "reject": false
  }
}
```

---

#### 7. **`/all/truth`**
```
@route_get(BASE_URL + 'all/truth', args={'must_complete': bool})
def all_truths(args):
    truth_list = []
    if TOD.objects.filter(truth = True).filter(must_complete = args['must_complete']).exists():
        for tods in TOD.objects.filter(truth = True).filter(reject = False).filter(must_complete = args['must_complete']):
            truth_list.append(tods.json_response())
        return {'all_truths': truth_list}
    else:
        return {'error': 'No truth statements found'}
```
> A success JSON response example (`must_complete` = False):
```
{
  "all_truths": [
    {
      "id": 3,
      "statement": "When was the last time you lied?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 5,
      "statement": "What’s the most embarrassing problem you’ve gone to the doctor for?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 9,
      "statement": "What happened when you cried last time?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    }
  ]
}
```
> Another success JSON response example (`must_complete` = True): 
```
{
  "all_truths": [
    {
      "id": 6,
      "statement": "What is your biggest fear?",
      "truth": true,
      "dare": false,
      "must_complete": true,
      "check_complete": false,
      "reject": false
    }
  ]
}
```

---

#### 8. **`/all/dare`**
```
@route_get(BASE_URL + 'all/dare', args={'must_complete': bool})
def all_dares(args):
    dare_list = []
    if TOD.objects.filter(dare = True).filter(must_complete = args['must_complete']).exists():
        for tods in TOD.objects.filter(dare = True).filter(reject = False).filter(must_complete = args['must_complete']):
            dare_list.append(tods.json_response())
        return {'all_dares': dare_list}
    else:
        return {'error': 'No dare statements found'}
```
> A success JSON response example (`must_complete` = False):
```
{
  "all_dares": [
    {
      "id": 2,
      "statement": "Text 'I won't be coming home tonight' to mom",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 4,
      "statement": "Keep 3 ice cubes in your mouth until they melt",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 7,
      "statement": "Eat a bite of a banana peel",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 8,
      "statement": "Show the most embarrassing photo on your phone",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    }
  ]
}
```
> Another success JSON response example (`must_complete` = True): 
```
{
  "all_dares": [
    {
      "id": 8,
      "statement": "Show the most embarrassing photo on your phone",
      "truth": false,
      "dare": true,
      "must_complete": true,
      "check_complete": false,
      "reject": false
    }
  ]
}
```

---

#### 9. **`/search`**
```
@route_get(BASE_URL + 'search', args={'keyword':str, 'must_complete': bool})
def search_tods(args):
    search_list = []
    if TOD.objects.filter(statement__contains = args['keyword']).filter(reject = False).filter(must_complete = args['must_complete']).exists():
        for search in TOD.objects.filter(statement__contains = args['keyword']).filter(reject = False).filter(must_complete = args['must_complete']):
            search_list.append(search.json_response())
        return {'search_list': search_list}
    else:
        return {'search_list': 'No truth or dare exists'}
```
> A success JSON response example (`must_complete` = False):
```
{
  "search_list": [
    {
      "id": 1,
      "statement": "State five of your weird habits",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 4,
      "statement": "Keep 3 ice cubes in your mouth until they melt",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 6,
      "statement": "What is your biggest fear?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 8,
      "statement": "Show the most embarrassing photo on your phone",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    }
  ]
}
```
> Another success JSON response example (`must_complete` = True):
```
{
  "search_list": [
    {
      "id": 6,
      "statement": "What is your biggest fear?",
      "truth": true,
      "dare": false,
      "must_complete": true,
      "check_complete": false,
      "reject": false
    }
  ]
}
```

---

#### 10. **`/reset_game`**
```
@route_post(BASE_URL + 'reset_game')
def reset_tods(args):
    reset_list = []
    if TOD.objects.exists():
        for r_reject in TOD.objects.filter(reject = True):
            r_reject.reset_change_reject()
        for r_must_complete in TOD.objects.filter(must_complete = True):
            r_must_complete.reset_must_complete()
        for r_change_complete in TOD.objects.filter(check_complete = True):
            r_change_complete.reset_change_complete()
        for reset_tod in TOD.objects.all():
            reset_list.append(reset_tod.json_response())
        return {'reset_truths_or_dares': reset_list}
    else:
        return {'error': 'No truth or dare exists'}
```
> A success JSON response example:
```
{
  "reset_truths_or_dares": [
    {
      "id": 1,
      "statement": "State five of your weird habits",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 2,
      "statement": "Text 'I won't be coming home tonight' to mom",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 3,
      "statement": "When was the last time you lied?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 4,
      "statement": "Keep 3 ice cubes in your mouth until they melt",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 5,
      "statement": "What’s the most embarrassing problem you’ve gone to the doctor for?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 6,
      "statement": "What is your biggest fear?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 7,
      "statement": "Eat a bite of a banana peel",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 8,
      "statement": "Show the most embarrassing photo on your phone",
      "truth": false,
      "dare": true,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    },
    {
      "id": 9,
      "statement": "What happened when you cried last time?",
      "truth": true,
      "dare": false,
      "must_complete": false,
      "check_complete": false,
      "reject": false
    }
  ]
}
```

---

Here is a table summarizing the meaning and usage of each route/endpoint.
| **Route Name** | **HTTP Method** | **Payload** | **Description** | **Error JSON Response** |
|---|---|---|---|---|
| `/new` | `POST` | args={'statement':str, 'truth':bool, 'dare':bool} | Allows users to add a new truth or dare statement to the database. Requires a statement text and boolean values for truth or dare. | / |
| `/all` | `GET` | args={'must_complete':bool} | Retrieves all truth or dare statements from the database, with the must_complete field set as either true or false. During a round of game, only the chosen statement will be shown when a player tries to use this endpoint. When the game is reset, this endpoint will return all of the statements in the database. | 'error': 'No truth or dare exists' |
| `/one` | `GET` | args={'id': int, 'must_complete': bool} | Retrieves a specific truth or dare statement by its unique id. | 'error': 'No truth or dare exists' |
| `/random` | `GET` | args={'must_complete': bool} | Returns a random truth or dare statement from the database, with the must_complete field set as either true or false. During a round of game, only the chosen statement will be shown when a player tries to use this endpoint. When the game is reset, this endpoint will return statements in the database randomly. | / |
| `/change_complete` | `POST` | args={'id':int} | Updates the completion status (`check_complete` field, false to true) of a specified statement by id and the `must_complete` field from true to false (since the statement is completed). | 'error': 'No truth or dare exists' |
| `/reject` | `POST` | args={'id':int} | Rejects and archives a specified truth or dare statement by id, removing it from active use in one round of game. Then a random statement will be generated from the database for the user to respond to. The `must_complete` field is set from false to true, indicating that the generated statement is mandatory for the player to complete. | 'error': 'No truth or dare exists' |
| `/all/truth` | `GET` | args={'must_complete': bool} | Retrieves all statements categorized as truths (true for the `truth` field). Filters result accordingly when the `must_complete` field of the user's statement is set to true. | 'error': 'No truth statements found' |
| `/all/dare` | `GET` | args={'must_complete': bool} | Retrieves all statements categorized as dares (true for the `dare` field). Filters result accordingly when the `must_complete` field of the user's statement is set to true. | 'error': 'No dare statements found' |
| `/search` | `GET` | args={'keyword':str, 'must_complete': bool} | Searches in the database for truth or dare statements that contain the specified keyword that the users put in. Filters search result accordingly when the `must_complete` field of the user's statement is set to true. | 'search_list': 'No truth or dare exists' |
| `/reset_game` | `POST` | / | Resets the game state, potentially clearing all completed or archived statements, setting all fields back to the original state, then returning a full list of the statements in the database. | 'error': 'No truth or dare exists' |

---

## Setup
💻 **Clone the repository in the `unit03_networking` folder.** Change `yourgithubusername` to the actual Github username before the download.
```
cd ~/desktop/making_with_code/unit03_networking/
git clone https://github.com/the-isf-academy/project_networking_backend_yourgithubusername.git
cd project_networking_project_networking_backend_yourgithubusername
```

💻 **Install necessary requirements for packages.**
```
poetry update
```

💻 **Enter the poetry shell.**
```
poetry shell
```

💻 **Enter the banjo debug to enable the routes.**
```
banjo --debug
```

💻 **Open up HTTPie for the interaction with the API.**

💻 **In HTTPie, on the top bar, enter http://127.0.0.1:5000/TOD in order to access the server.**


### Contents

Here's what is included:
- `\app`
    - `models.py` - `TOD` model
    - `views.py` - endpoints
- `database.sqlite`  
- `README.md` 

**To start a Banjo server:** `banjo` 
- [Banjo Documentation](https://the-isf-academy.github.io/banjo_docs/)
