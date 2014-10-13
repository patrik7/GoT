from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.template.context import RequestContext
from django.shortcuts import render_to_response

login_required_kwargs = {
    'login_url': '/admin/', #TODO
    'redirect_field_name': 'redirect',
}

@login_required(**login_required_kwargs)
def account(request):
        
    return render_to_response('account.html', context_instance=RequestContext(request))