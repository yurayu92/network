# encoding: utf-8
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from md5 import md5

from classes.database_class import database
from classes.person_class import Person

db = database()
Person = Person(db)

def check_auth(request):
    if request.session.get('user_id'):
        is_loggined = True
    else:
        is_loggined = False
        return HttpResponseRedirect('/')
    return {'is_loggined' : is_loggined}


def login(request):    
    if request.session.get('user_id'):
        return HttpResponseRedirect('/profile/%s/' % (request.session['user_id']))
    else:
        is_loggined = False
    
    if request.method == 'POST':
        check_user = db.fetchOne('SELECT id, password FROM users\
                                  WHERE email = "%s"' % (request.POST['email']))
        
        if md5(request.POST['password']).hexdigest() == check_user['password']:
            request.session['user_id'] = check_user['id']
            return HttpResponseRedirect('/profile/%s/' % (check_user['id']))
        else:
            return render_to_response('base.html', {'error' : True})
    else:
        return render_to_response('base.html', 
                                  {'error' : False}, 
                                  context_instance = RequestContext(request, processors=[check_auth]))
            

def person_update(request):
    if request.session.get('user_id'):
        is_loggined = True
    else:
        return HttpResponseRedirect('/')
    
    if request.method == 'POST':
        return HttpResponseRedirect('/profile/update/')
    
    id = request.session['user_id']
    person_info = Person.getPersonById(id)
    
    return render_to_response('person_info.html', 
                              {'person_info' : person_info,
                               'user_id' : id},
                               context_instance = RequestContext(request, processors=[check_auth]))

def friends(request, offset):
    if request.session.get('user_id'):
        is_loggined = True
    else:
        return HttpResponseRedirect('/')
    
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            try:
                request.session.pop('user_id')
            except:
                pass
            return HttpResponseRedirect('/')
        
    not_friends = Person.getNewFriends(offset)
    id = request.session['user_id']
    friends = Person.getFriends(offset)
    
    return render_to_response('friends.html',
                              {'friends' : friends,
                               'user_id' : id,
                               'not_friends' : not_friends},
                               context_instance = RequestContext(request, processors=[check_auth]))


def person(request, offset):
    if request.session.get('user_id'):
        is_loggined = True
        id = request.session['user_id']
    else:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        if request.POST.has_key('logout'):
            try:
                request.session.pop('user_id')
            except:
                pass
            return HttpResponseRedirect('/')
        elif request.POST.has_key('add-friend'):
            Person.addFriend(offset, id)
            
    

    person_info = Person.getPersonById(offset)
    person_friends_info = Person.fetchProfile(offset, id)

    return render_to_response('person.html',{'person' : person_info,
                                             'some_friends' : person_friends_info['some_friends'],
                                             'all_friends_count' : person_friends_info['count'],
                                             'is_friend' : person_friends_info['is_friend'],
                                             'user_id' : id},
                                             context_instance = RequestContext(request, processors=[check_auth]))