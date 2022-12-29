from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import View
import gtts  
from playsound import playsound

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    # make a request to google to get synthesis  
                    # t1 = gtts.gTTS("Hi my name is Wilson I am your virtual assistance to control this website. you must have to say Wilson before every command")
                    # # save the audio file  
                    # t1.save("welcome.mp3")
                    # play the audio file  
                    playsound("welcome.mp3")           

                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message,})

def logout(request):
    request.session.clear()
    return redirect('login')
