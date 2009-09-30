import datetime
import hashlib
import logging
    
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
    
from facebookconnect.models import FacebookUser
    
def login_facebook_connect(request):
    status = 'unknown failure'
    try:
        expires = request.POST['expires']
        ss = request.POST['ss']
        session_key = request.POST['session_key']
        user = request.POST['user']
        sig = request.POST['sig']
    
        pre_hash_string = "expires=%ssession_key=%sss=%suser=%s%s" % (
            expires,
            session_key,
            ss,
            user,
            settings.FACEBOOK_APPLICATION_SECRET,
        )
        post_hash_string = hashlib.new('md5')
        post_hash_string.update(pre_hash_string)
        if post_hash_string.hexdigest() == sig:
            try:
                fb = FacebookUser.objects.get(facebook_id=user)
                status = "logged in existing user"
            except FacebookUser.DoesNotExist:
                contrib_user = User()
                contrib_user.save()
                contrib_user.username = u"fbuser_%s" % contrib_user.id

                fb = FacebookUser()
                fb.facebook_id = user
                fb.contrib_user = contrib_user
                
                temp = hashlib.new('sha1')
                temp.update(str(datetime.datetime.now()))
                password = temp.hexdigest()
                    
                contrib_user.set_password(password)
                fb.contrib_password = password
                    
                fb.save()
                contrib_user.save()
                status = "created new user"
                
            authenticated_user = auth.authenticate(username=fb.contrib_user.username, password=fb.contrib_password)
            auth.login(request, authenticated_user)
        else:
            status = 'wrong hash sig'
            
            logging.debug("Facebook connect: user %s with exit status %s" % (user, status))
            
    except Exception, e:
        logging.debug("Exception thrown in the FBConnect ajax call: %s" % e)
            
    return HttpResponse("%s" % status)
        
def xd_receiver(request):
        return render_to_response('facebookconnect/xd_receiver.html')

