from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import Hotels, Images, Comments, Selected, Configuration
from createDataBase import createDataBase
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import RequestContext
from django.utils.html import strip_tags
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
import itertools
# Create your views here.

def homepage(request):
    flagEsp = True
    flagFr = False
    flagEn = False
    hotels = Hotels.objects.all()
    if not hotels:
        rateDefault = 0
        names, addresses, latitude, longitude, bodies, image, category, webs = createDataBase(flagEsp, flagFr, flagEn)
        for name,body,latitudes,longitudes,address,img,cat,web in itertools.izip(names,bodies,latitude,longitude,addresses,image,category, webs):
            print name
            bodyStrip = strip_tags(body)
            newHotel = Hotels(name=name, body=bodyStrip, latitude=latitudes, longitude=longitudes, address=address, category=cat[0], stars=cat[1], web=web, rate=rateDefault)
            newHotel.save()
            for currentImage in img:
                if name == "Urban":
                    name = Hotels.objects.get(name=name)
                    try:
                        i = 0
                        flag = True
                        while flag:
                            imgUrban = currentImage[i]
                            print imgUrban
                            newImage = Images(url=imgUrban, hotel=name)
                            newImage.save()
                            i = i + 1
                    except IndexError:
                        flag = False
                else:
                    name = Hotels.objects.get(name=name)
                    newImage = Images(url=currentImage, hotel=name)
                    newImage.save()
    hotelComment = Hotels.objects.annotate(quantity=Count('comments')).order_by('-quantity')
    hotelList = []
    for count in range(10):
        if hotelComment[count].quantity > 0:
            hotel = Hotels.objects.get(name=hotelComment[count])
            image = Images.objects.filter(hotel=hotel)[0].url
            hotelList += [(hotel, image)]
    if request.method == "POST":
        imgList = []
        hotelList = []
        Coments = Comments.objects.all()
        passed = []
        for hotel in hotelComment:
            for coment in Coments:
                if  hotel == coment.hotelCommented and hotel not in passed:
                    passed.append(hotel)
                    imgFav = Images.objects.filter(hotel=hotel)
                    hotelList += [(hotel, imgFav)]
                    imgList = []
        context = RequestContext(request, {"hotelList" : hotelList})
        template = get_template("userXML.xml")
        return HttpResponse(template.render(context), content_type="text/xml")
    if request.method == "GET":
        allConfig = Configuration.objects.all()
        template = get_template("index.html")
        context = RequestContext(request, {"hotelList" : hotelList, "allConfig" : allConfig})
        return HttpResponse(template.render(context))

def accommodations(request):
    if request.method == "GET":
        hotels = Hotels.objects.all()
    elif request.method == "POST":
        category = request.POST.get('category')
        stars = request.POST.get('stars')
        if category != "None" and stars != "None":
            hotels = Hotels.objects.filter(category=category, stars=stars)
        elif stars != "None":
            hotels = Hotels.objects.filter(stars=stars)
        elif category != "None":
            hotels = Hotels.objects.filter(category=category)
        else:
            hotels = Hotels.objects.all()

    template = get_template("accommodations.html")
    context = RequestContext(request, {"hotels" : hotels})
    return HttpResponse(template.render(context))

@csrf_exempt
def register(request):
    if request.method == "POST":
        nickname = request.POST.get("login")
        passwd = make_password(request.POST.get("password"))
        newUser = User(username=nickname, password=passwd)
        newUser.save()
        userConfig = User.objects.get(username=nickname)
        newConfig = Configuration(user=userConfig)
        newConfig.save()
    return HttpResponseRedirect("/")

@csrf_exempt
def authentication(request):
    if request.method == "POST":
        username = request.POST.get('login')
    password = request.POST.get('password')
    users = User.objects.all()
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    return HttpResponseRedirect("/")

def hotelView(request, index):
    flagEsp = False
    flagFr = False
    flagEn = False
    hotel = Hotels.objects.get(id=index)
    comments = Comments.objects.filter(hotelCommented=hotel)
    currentRate = hotel.rate
    hotelImgs = Images.objects.filter(hotel=hotel)
    imgList = []
    i = 0
    for img in hotelImgs:
        imgList.append(img.url)
        i = i + 1
        if i == 5:
            break
    body = hotel.body
    if request.method == "POST":
        lang = request.POST.get("language")
        comment = request.POST.get("comentarios")
        chosen = request.POST.get("hotel")
        liked = request.POST.get("liked")
        repeated = False
        if liked == str(1):
            newRate = currentRate + 1
            hotel.rate = newRate
            hotel.save()
        if comment != "Escribe tu comentario." and comment != None:
            user = User.objects.get(username=request.user.username)
            commentUsers = Comments.objects.filter(hotelCommented=hotel)
            for commentUser in commentUsers:
                if commentUser.author == user:
                    repeated = True
            if repeated:
                commentEdited = Comments.objects.get(hotelCommented=hotel, author=user)
                commentEdited.annotation = comment
                commentEdited.save()
            else:
                newComment = Comments(annotation=comment, hotelCommented=hotel, author=user)
                newComment.save()
        if chosen != None:
            userCh = User.objects.get(username=request.user.username)
            newSelection = Selected(chosenHotel=hotel, user=userCh)
            newSelection.save()
        if lang == "Spa" or lang == "None":
            body = hotel.body
        elif lang == "Fra":
            flagFr = True
            names, addresses, latitude, longitude, bodies, image, category, webs = createDataBase(flagEsp, flagFr, flagEn)
            index = 0
            for name in names:
                if name == hotel.name:
                    break
                index = index + 1
            try:
                body = strip_tags(bodies[index])
            except IndexError:
                body = "Non disponible."
        elif lang == "Ing":
            flagEn = True
            names, addresses, latitude, longitude, bodies, image, category, webs = createDataBase(flagEsp, flagFr, flagEn)
            index = 0
            for name in names:
                if name == hotel.name:
                    break
                index = index + 1
            try:
                body = strip_tags(bodies[index])
            except IndexError:
                body = "Not avaliable"
    currentRate = hotel.rate
    template = get_template('hotelView.html')
    context = RequestContext(request, {"hotel" : hotel, "imgList" : imgList, "body" : body, "comments" : comments, "currentRate" : currentRate})
    return HttpResponse(template.render(context))

def css(request):
    color = "blue"
    size = 12
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        userConfig = Configuration.objects.get(user=user)
        color = userConfig.color
        size = userConfig.size
    template = get_template("css/style.css")
    context = RequestContext(request, {"color": color, "size": size})
    return HttpResponse(template.render(context), content_type="text/css")

def about(request):
    template = get_template('about.html')
    return HttpResponse(template.render())

def userXml(request, userXml):
    imgList = []
    hotelList = []
    user = User.objects.get(username=userXml)
    hotelFavs = Selected.objects.filter(user=user)
    for fav in hotelFavs:
        imgFav = Images.objects.filter(hotel=fav.chosenHotel)
        hotelList += [(fav.chosenHotel, imgFav)]
        imglList = []
    context = RequestContext(request, {"hotelList" : hotelList})
    template = get_template("userXML.xml")
    return HttpResponse(template.render(context), content_type="text/xml")

def userpage(request, user):
    if request.method == "POST":
        newTitle = request.POST.get("newTitle")
        newBGround = request.POST.get("backgroundSelected")
        newLSize = request.POST.get("letterSize")
        user = User.objects.get(username=user)
        newConfig = Configuration.objects.get(user=user)
        #print newConfig.title
        #print newTitle
        if newTitle != "Titulo de la pagina." and newTitle != newConfig.title and newTitle != None:
            newConfig.title = newTitle
            newConfig.save()
        if newBGround != None and newBGround != newConfig.color:
            newConfig.color = newBGround
            newConfig.save()
        if newLSize != None and newLSize != newConfig.size:
            newConfig.size = newLSize
            newConfig.save()
    userPage = User.objects.get(username=user)
    userConfig = Configuration.objects.get(user=userPage)
    hotelList = []
    favs = Selected.objects.filter(user=userPage)
    for fav in favs:
        image = Images.objects.filter(hotel=fav.chosenHotel)[0].url
        hotelList += [(fav.chosenHotel, image, fav.date)]
    context = RequestContext(request, {"hotelList" : hotelList, "userPage" : userPage, "userConfig" : userConfig})
    template = get_template("userPage.html")
    return HttpResponse(template.render(context))
