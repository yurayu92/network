# encoding: utf-8
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from md5 import md5

from classes.database_class import database

db = database()

def check_auth(request):
    if request.session.get('user_id'):
        is_loggined = True
    else:
        is_loggined = False
        return HttpResponseRedirect('/')
    return {'is_loggined' : is_loggined}


def login(request):
    if request.method == 'POST':
        check_user = db.fetchOne('SELECT id, password FROM users\
                                  WHERE email = "%s"' % (request.POST['email']))
        
        if md5(request.POST['password']).hexdigest() == check_user['password']:
            request.session['user_id'] = check_user['id']
            return HttpResponseRedirect('/profile/%s/' % (check_user['id']))
        else:
            return render_to_response('base.html', {'error' : True})
    else:
        return render_to_response('base.html', {'error' : False})
            

def person(request, offset):
    if request.method == 'POST':
        if request.POST.has_key('logout'):
            try:
                del request.session['user_id']
            except:
                pass
            return HttpResponseRedirect('/')
    
    person = db.fetchOne('SELECT first_name, last_name, avatar, birthday, job, email, phone\
                           FROM users WHERE id = %s' % (offset))
    
    some_friends = db.fetchMany('SELECT `u`.`id`, `u`.`first_name`,\
                                 `u`.`last_name`, `u`.`avatar`\
                                 FROM `users_friends` `f` INNER JOIN `users` `u`\
                                 ON `u`.`id` = `f`.`users1_id` or `u`.`id` = `f`.`users2_id`\
                                 WHERE `f`.`is_active` = 1 AND `u`.`id` != %s AND \
                                 (`f`.`users1_id` = %s or `f`.`users2_id` = %s) ORDER BY RAND()' 
                                 % (offset, offset, offset), 3)
    
    all_friends_count = int(db.fetchOne('SELECT FOUND_ROWS()')['FOUND_ROWS()'])

    return render_to_response('person.html',{'person' : person,
                                             'some_friends' : some_friends,
                                             'all_friends_count' : all_friends_count},
                                             context_instance = RequestContext(request, processors=[check_auth]))