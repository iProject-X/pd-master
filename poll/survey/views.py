from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.


 # start and create user for survey!!!!
def starttest(request):
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            fullname = form['fullname'].value()
            age = form['age'].value()
            pol = form['pol'].value()
            specialite = form['specialite'].value()
            language = form['language'].value()
            vibor_test_id = form['survey'].value()
            user_id = createuser(fullname, age, pol, specialite, language)
            testlink(user_id, vibor_test_id )
            return test_first(request, user_id, vibor_test_id)
    else:
        form = userform()
    return render(request, 'create.html', {'form': form})

def createuser(fullname, age, pol, specialite, language):
    try:
        user = users.objects.get(fullname=fullname, age=age, pol=pol, specialite=specialite, language=language)
    except ObjectDoesNotExist:
        user = users(fullname=fullname, age=age, pol=pol, specialite=specialite, language=language)
        user.save()
        return user.id
    return user.id

def testlink(user_id, vibor_test_id):
    try:
        links = userlink.objects.get(user_id=user_id, vibor_test_id=vibor_test_id)
    except:
        user = users.objects.get(id=user_id)
        crlink = vibor_test.objects.get(id=vibor_test_id)
        links = userlink( user_id=user, vibor_test_id=crlink)
        links.save()
        return links.id
    return links.id
# end start and create user for survey!!!
def test_first(request, user_id,vibor_test_id):
    stimul_id = getFirstQuestionNumber(vibor_test_id)
    nevigation = questionNevigation(stimul_id,user_id,vibor_test_id)
    next = nevigation.get('next')
    previous = nevigation.get('previous')
    fullname = nevigation.get('fullname')
    question = stimul_slov.objects.filter(id=stimul_id,test_id=vibor_test_id).first()
    answer = otvet.objects.filter(stimul_id=stimul_id,test_id=vibor_test_id).first()

    return render(request, 'test.html', {'question': question, 'answer': answer, 'stimul_id': stimul_id,
                                         'next':next, 'previous': previous,'user_id': user_id,
                                         'fullname': fullname, 'vibor_test_id': vibor_test_id})

def getFirstQuestionNumber(vibor_test_id):
    question =  stimul_slov.objects.filter(test_id=vibor_test_id).first()
    return question.id

def questionNevigation(stimul_id,user_id,vibor_test_id):
    nevigation = {}
    next_privious = nevigatequestionnumber(stimul_id,vibor_test_id)
    candidate = users.objects.get(pk=user_id)
    nevigation['stimul_id'] = stimul_id
    nevigation['next'] = next_privious.get("next")
    nevigation['previous'] = next_privious.get("previous")
    return nevigation

def nevigatequestionnumber(stimul_id,vibor_test_id):
    next_privious = {}
    previous = get_previous_stimul_id(stimul_id,vibor_test_id)
    next = get_next_stimul_id(stimul_id,vibor_test_id)
    next_privious['next']=next
    next_privious['previous'] = previous
    next_privious['stimul_id'] = stimul_id
    return next_privious


def get_previous_stimul_id(current_stimul_id,vibor_test_id):
    position = int(current_stimul_id)
    try:
        current_stimul_id = int(current_stimul_id) - 1
        question = stimul_slov.objects.filter(test_id=vibor_test_id).filter(id__lte=current_stimul_id ).last()
        retval = question.id
    except AttributeError:
        return position
    except ObjectDoesNotExist:
        return position
    return retval

def get_next_stimul_id(current_stimul_id,vibor_test_id):
    position = int(current_stimul_id)
    try:
        current_stimul_id = int(current_stimul_id) + 1
        question = stimul_slov.objects.filter(test_id=vibor_test_id).filter(id__gte=current_stimul_id ).first()
        retval = question.id
    except AttributeError:
        return position
    except ObjectDoesNotExist:
        return position
    return retval


def test(request, vibor_test_id, user_id, question_id):
    if request.method == 'POST':

        user_id = request.POST['user_id']

        
        vibor_test_id = request.POST['vibor_test_id']
        saveAnswers(user_id, question_id, vibor_test_id)
        question_id = request.POST['next']
        if remaining == 0:
             return showResultpage(request, vibor_test_id, user_id, fullname )
    nevigation = questionNevigation(question_id,user_id,vibor_test_id)
    next = nevigation.get('next')
    previous = nevigation.get('previous')

    fullname = nevigation.get('fullname')

    question = stimul_slov.objects.filter(id=question_id,test_id=vibor_test_id).first()



    # return showResultpage(request,vibor_test_id,user_id,fullname)
    return render(request, 'test.html', {'question': question,
                                         'next':next, 'previous': previous,'user_id': user_id,
                                         'vibor_test_id': vibor_test_id})


def saveAnswers( vibor_test_id, user_id, question_id,):
    answer = request.POST['answer']
    vibor_test_id = vibor_test.objects.get(pk=int(vibor_test_id))
    user = users.objects.get(pk=int(users_id))
    question = stimul_slov.objects.get(pk=int(stimul_slov_id))
    saveans = otvet(user_id=user, test_id=vibor_test_id, stimul_id=question,)
    saveans.save()


#
# def showResultpage(request,vibor_test_id,user_id,fullname):
#     pass
