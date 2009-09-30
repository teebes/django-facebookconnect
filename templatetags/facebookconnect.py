from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
    
register = template.Library()
    
class FacebookScriptNode(template.Node):
        def render(self, context):
            return """
            <script src="http://static.ak.connect.facebook.com/js/api_lib/v0.4/FeatureLoader.js.php" type="text/javascript"></script>
    
            <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
    
            <script type="text/javascript"> FB.init("%s", "%s");
                function facebook_onlogin() {
                    var uid = FB.Facebook.apiClient.get_session().uid;
                    var session_key = FB.Facebook.apiClient.get_session().session_key;
                    var expires = FB.Facebook.apiClient.get_session().expires;
                    var secret = FB.Facebook.apiClient.get_session().secret;
                    var sig = FB.Facebook.apiClient.get_session().sig;
    
                    fb_connect_ajax(expires, session_key, secret, uid, sig);
    
                }
    
                function fb_connect_ajax(expires, session_key, ss, user, sig) {
        
                    var post_string = 'expires=' + expires;
                    post_string = post_string + '&session_key=' + session_key;
                    post_string = post_string + '&ss=' + ss;
                    post_string = post_string + '&user=' + user;
                    post_string = post_string + '&sig=' + sig;
    
                    $.ajax({
                        type: "POST",
                        url: "%s",
                        data: post_string,
                        success: function(msg) {
                            window.location = '%s'; //.reload()
                        }
                    });
                } 
            </script>       
            """ % (settings.FACEBOOK_API_KEY, reverse('xd_receiver'), reverse('facebook_connect_ajax'), settings.LOGIN_REDIRECT_URL)
    
    
def facebook_connect_script(parser, token): return FacebookScriptNode()
    
register.tag(facebook_connect_script)
    
class FacebookLoginNode(template.Node):
        def render(self, context): return """<fb:login-button onlogin="facebook_onlogin();"></fb:login-button>"""
    
def facebook_connect_login_button(parser, token): return FacebookLoginNode()
    
register.tag(facebook_connect_login_button)

