# Project Networking


> **Don't forget to edit this `README.md` file**
>
> If you're interested in how to format markdown, click [here](https://www.markdownguide.org/basic-syntax/#images-1)

## API Overview
A **"Truth or Dare"** game is usually played within friend groups to encourage people to say things that they may not be willing to tell in a normal setting (truths) or to do something they may not normally do for other people's enjoyment (dare). 

This API hosts statements of *truths* and *dares* and is a helpful tool assisting friend groups to play and customize the game of **"Truth or Dare"**. In one round of the game using this API, you can be allocated a random truth or dare statement to answer or do, add new truths or dares to the database, and archive truth or dare statements that you don't like.

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
In the models.py file, there are 6 fields in total of different field data types. 
| **Field Name** | **Data Type** | **Description** |
|---|---|---|
| `id` | `IntegerField` | A unique identifier for each truth or dare statement, ensuring each entry can be distinctly retrieved or modified. |
| `statement` | `StringField` | The text of the truth or dare statement itself, holding the actual content that the user is going to interact with. |
| `truth` | `BooleanField` | A variable indicating whether the statement presented is a truth (true) or a dare (false), providing categorization of the content for the user. |
| `dare` | `BooleanField` | Similar to the 'truth' field, this variable indicates whether the statement presented is a dare (true) or a truth (false), providing categorization of the content for the user. To clarify, at least one of the `truth` or `dare` fields should be true for a statement. |
| `check_complete` | `BooleanField` | A field that can be used to mark whether a statement has been answered or completed in a round of game, helping track user progress and ensuring that statements can be revisited or marked as done. |
| `archive` | `BooleanField` | A variable that indicates if a statement has been hidden (true) or is still active/visible (false), allows users to hide statements they no longer want to see, without deleting them entirely from the database. |

#### Methods
In the models.py file, there are 4 methods in total. 
| **Method Name** | **Parameter** | **Description** |
|---|---|---|
| `json_response` | `IntegerField` | This method generates a clearly-formatted JSON response for a specific truth or dare statement. It takes the `id` to identify the statement and the `truth` and `dare` boolean variables to indicate the type. This is useful for returning structured data to users, allowing them to easily access statement details and information. |
| `change_statement` | `StringField` | This method allows users to update the text of an existing truth or dare statement. It takes `new_statement` as a parameter, which replaces the original statement. This enables users to edit statements flexibly, ensuring highly-customizable and up-to-date content in the database. |
| `change_complete` | `BooleanField` | This method switches the completion status of a statement. It can be used to mark whether the statement is answered or completed by the players, which is useful for tracking user interactions. |
| `change_archive` | `BooleanField` | This method updates the archival status of a statement. It allows users to effectively manage the visibility of truth or dare statements and hide ones they don't want to see without deleting them from the database. |

### Endpoints
In the views.py file, there are 10 endpoints in total. 
| **Route Name** | **HTTP Method** | **Payload** | **Success JSON Response** | **Error JSON Response** |
|---|---|---|---|---|
| `/all` | `GET` | / | 'all_truths_or_dares': tods_list | / |
| `/new` | `POST` | args={'statement':str, 'truth':bool, 'dare':bool} | 'new_truth_or_dare': new_tod.json_response() | / |
| `/all/truth` | `GET` | / | 'all_truths': truth_list | 'error': 'No truth statements found' |
| `/all/dare` | `GET` | / | 'all_dares': dare_list | 'error': 'No dare statements found' |
| `/one` | `GET` | args={'id':int} | 'one_truth_or_dare': one_tod.json_response() | 'error': 'No truth or dare exists' |
| `/random` | `GET` | / | 'random_truth_or_dare': random_tod.json_response() | / |
| `/change_complete` | `POST` | args={'id':int} | 'completed_truth_or_dare': complete_tod.json_response() | 'error': 'No truth or dare exists' |
| `/reject` | `GET` | args={'id':int} | 'another_truth_or_dare': reject_tod.json_response() | 'error': 'No truth or dare exists' |
| `/change_archive` | `POST` | args={'id':int} | 'archived_tod': archive_tod.json_response() | 'error': 'No truth or dare exists' |
| `/search` | `GET` | args={'keyword':str} | 'search_list': search_list | 'search_list': 'No truth or dare exists' |

---

## Setup

### Contents

Here's what is included:
- `\app`
    - `models.py` - `Truth_or_Dare` model
    - `views.py` - endpoints
- `database.sqlite`  
- `README.md` 

**To start a Banjo server:** `banjo` 
- [Banjo Documentation](https://the-isf-academy.github.io/banjo_docs/)



