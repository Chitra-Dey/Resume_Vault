from django.shortcuts import render,redirect
from django.db.models import Q
from .forms import candidateforms
from .models import Candidate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from .forms import StudentSignupForm, RecruiterSignupForm
from django.contrib.auth import logout
# def error_404_view(request, exception):
#      form = candidateforms()
#      return render(request,'404.html',{'form':form},status=404)

def signup_student(request):
    form = StudentSignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'signup.html', {'form': form, 'user_type': 'Student'})

def signup_recruiter(request):
    form = RecruiterSignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'signup.html', {'form': form, 'user_type': 'Recruiter'})


class LoginView(auth_views.LoginView):
    template_name = 'login.html'

class LogoutView(auth_views.LogoutView):
    next_page = 'login'

@login_required
def create_candidate(request):
    if request.method == 'POST':
       form = candidateforms(request.POST,request.FILES)
       if form.is_valid():
           form.save()
           return redirect('candidates_list')
    else:
        form=candidateforms()
    return render(request,'create.html',{'form':form})   
@login_required 
def candidates_list(request):
    query = request.GET.get('q', '').strip()

    # Step 1: Search filter (if keyword provided)
    qs = Candidate.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(skills__icontains=query)
    ) if query else Candidate.objects.all()

    # Step 2: Role-based access
    if request.user.is_authenticated:
        if request.user.is_recruiter:
            candidates = qs                                # recruiters see all matching records
        else:  # student user
            candidates = qs.filter(user=request.user)      # students see only their own
    else:
        candidates = Candidate.objects.none()              # anonymous sees nothing

    return render(request, 'list.html', {
        'candidates': candidates,
        'query': query
    })
def edit_candidate(request,pk):
    candidates=Candidate.objects.get(pk=pk)
    if request.method == 'POST':
       form = candidateforms(request.POST,request.FILES, instance=candidates)
       if form.is_valid():
           form.save()
           return redirect('candidates_list')
    else:
        form=candidateforms(instance=candidates)
    return render(request,'edit.html',{'form':form}) 
   
def delete_candidate(request,pk):
    candidates=Candidate.objects.get(pk=pk)
    if request.method =='POST':
        candidates.delete() 
        return redirect('candidates_list')
    return render(request,'delete.html',{'candidates':candidates})    

@login_required
def userLogout(request):
    logout(request)
    return redirect('signup_student')
