from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.template.context import RequestContext
from django.shortcuts import render_to_response

from forms import TaxRecruitmentForm

login_required_kwargs = {
    'login_url': '/admin/', #TODO
    'redirect_field_name': 'redirect',
}

@login_required(**login_required_kwargs)
def account(request):
    
    if request.method == "POST":
        tax_form = TaxRecruitmentForm(request.POST, instance=request.user.lord)
        
        if tax_form.is_valid():
            tax_form.save()
    else:
        tax_form = TaxRecruitmentForm(instance=request.user.lord)
    
    return render_to_response('account.html', context_instance=RequestContext(request, {
        'lord': request.user.lord,
        'form_tax_recruitment': tax_form,
        }))