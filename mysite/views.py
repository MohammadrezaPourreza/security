from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
import os
import subprocess
from mysite.models import attempts
from .forms import loginForm
import crypt
from ip2geotools.databases.noncommercial import DbIpCity

# Create your views here.
def login(request):
    if request.method == 'POST':
        myform = loginForm(request.POST)
        user = myform.data['username']
        passwd = myform.data['password']
        checkpassword = findlinuxuserpass(user,passwd)
        if checkpassword:
            host = request.headers['Host'].split(':')[0]
            content_length = request.headers['Content-Length']
            content_type = request.headers['Content-Type']
            user_agent = request.headers['User-Agent']
            username = user
            password = passwd
            time = timezone.now()
            # result = DbIpCity.get('147.229.2.90', api_key='free')
            # country = result.country
            country = "iran"
            obj = attempts(username=username, password=password, host=host, user_agent=user_agent, content_type=content_type,
                           content_length=content_length, country=country, att_date=time)
            obj.save()
            return redirect(files,username = username)
        else:
            return HttpResponse("username or password is incorrect")
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})

def restrict(request):
    # os.system('sudo iptables-legacy -A INPUT -p tcp --dport 22 -m state --state NEW -j DROP')
    # os.system('sudo iptables-legacy -A INPUT -p tcp --dport 3022 -m state --state NEW -j DROP')
    os.system('sudo iptables-legacy -A INPUT -p tcp --dport 8000 -s 12.470.113.0/8 -j ACCEPT')
    os.system('sudo iptables-legacy -A INPUT -p tcp --dport 8000 -j DROP')
    return HttpResponse("iptables modified")

def files(request,username):
    output = ""
    path = "/home/mohammadreza/Desktop/files"
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            temp = ['getfacl']
            temp.append(path+"/"+file)
            result = subprocess.check_output(temp)
            parts = str(result).split('\\n')
            print(parts)
            print("_______")
            for part in parts:
                if username in part:
                    print(part)
                    output= output + (file + " : "+part+" |******| ")
    return HttpResponse(output)


def findlinuxuserpass(user,password):
    file = open('/etc/shadow', 'r')
    lines = file.readlines()
    for line in lines:
        if user in line:
            passwd = line.split(":")[1]
            method = crypt.METHOD_SHA512
            met = passwd.split("$")[1]
            salt = passwd.split("$")[2]
            if met == "6":
                method = crypt.METHOD_SHA512
            elif met == "2a":
                method = crypt.METHOD_BLOWFISH
            elif met == "1":
                method = crypt.METHOD_MD5
            elif met == "5":
                method = crypt.METHOD_SHA256
            if passwd == crypt.crypt(password, "$"+met+"$"+salt):
                return True
    return False