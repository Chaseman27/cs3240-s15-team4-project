from django.shortcuts import render, render_to_response
#from SecureWitness.forms import UserForm, UserProfileForm
#from SecureWitness.models import UserProfile, File
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from SecureWitness.forms import FileUploadForm,UserForm, UserProfileForm
from SecureWitness.models import File, Group, Report, UserProfile
import datetime

def index(request):
    context = RequestContext(request)

    reports = Report.objects.all()
    groups = Group.objects.all()
    context_dict = {'reports': reports, 'groups': groups}
    return render_to_response('SecureWitness/index.html', context_dict, context)

def register(request):
    context = RequestContext(request)
    
    #set to False initially. Changes to True when registration succeeds.
    registered = False

    #If HTTP POST, interested in processing form data
    if request.method == 'POST':
        #try to grab info from raw form info.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #hash password then update user object
            user.set_password(user.password)
            user.save()

            #Sort out UserProfile instance
            #Since we need to set the user attribute ourselves, set commit=False.
            #delays saving model until ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True

        else:
            #print problems to terminal and also shown to user
            print (user_form.errors, profile_form.errors)

    #Not HTTP POST, so render form using two ModelForm instances
    #Forms will be blank for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
        'SecureWitness/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)

def user_login(request):
    context = RequestContext(request)

    #If request is HTTP POST, try to pull out relevant information
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #See if username/password combo is valid
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/SecureWitness/')
            else:
                return HttpResponse("Your Profiles account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    #Request not HTTP POST, so display login form.
    #Scenario most liekly HTTP GET.
    else:
        return render_to_response('SecureWitness/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/SecureWitness/')

@login_required
def uploadView(request):
    if request.method == 'POST':
		#form that holds the upload file buttons
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
			#if the form is valid, put the file where it is supposed to go
			
            #new_fileUpload = SampleModel(file = request.FILES['file'])
            #new_fileUpload.save()
			
            User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
            new_Report = Report(author = request.user.profile, title = request.POST['title'], shortDesc = request.POST['shortDesc'], detailsDesc = request.POST['detailsDesc'], dateOfIncident = request.POST['dateOfIncident'], locationOfIncident = request.POST['locationOfIncident'], keywords = request.POST['keywords'], user_perm = request.POST.get('user_perm', False), timestamp = str(datetime.datetime.now()), files = request.FILES['file'])
            new_Report.save()
 
            return HttpResponseRedirect(reverse('SecureWitness:index'))
        else:
			#If there is an issue with uploading a file let the user know
            return HttpResponse("Invalid File Upload details... Please be sure you are filling out the appropriate fields.")
    else:
        form = FileUploadForm()
 
    data = {'form': form}
	#return render(request, 'polls/upload.html', data)
    return render_to_response('SecureWitness/upload.html', data, context_instance=RequestContext(request))

@login_required
def user_portal(request):
    context = RequestContext(request)
    return render_to_response('SecureWitness/portal.html', {}, context)

@login_required
def user_settings(request):
    context = RequestContext(request)
    return render_to_response('SecureWitness/settings.html', {}, context)

@login_required
def group(request, usergroup):

    context = RequestContext(request)
    group_list = Group.objects.all()
    context_dict = {'group_list': group_list}
    g = Group.objects.get(name=usergroup)
    context_dict['group'] = g

    members = [val for val in g.members.all() if val in g.members.all()]
    context_dict['members'] = members

    return render_to_response('SecureWitness/group.html', context_dict, context)

def encode_url(str):
    return str.replace(' ', '_')

def report(request, selectedReport):
    #print("looking at report")
    #return HttpResponse ("Looking at report: {0}".format(selectedReport.title))
    context = RequestContext(request)
    report_list = Report.objects.all()
    context_dict = {'report_list': report_list}
	#need to get rid of extra space AND encode url
    titleRequest = selectedReport + " "
    report = Report.objects.filter(title=titleRequest)
    context_dict['report'] = report
	
	
    return render_to_response('SecureWitness/reportDetails.html', context_dict, context)

