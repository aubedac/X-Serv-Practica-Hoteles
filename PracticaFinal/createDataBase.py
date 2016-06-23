from hotelparser import getHotels
import itertools

def createDataBase(flagEsp, flagFr, flagEn):
    parsing = getHotels(flagEsp, flagFr, flagEn)
    names = parsing.get('name').split('|')[:-1]
    addresses = parsing.get('address').split('|')[:-1]
    latitude = parsing.get('latitude').split('|')[:-1]
    longitude = parsing.get('longitude').split('|')[:-1]
    bodies = parsing.get('body').split('|')[:-1]
    image = parsing.get('images')
    category = parsing.get('category')
    webs = parsing.get('web').split('|')[:-1]
    return names, addresses, latitude, longitude, bodies, image, category, webs
#imageUrban = ""
#or name,body,latitudes,longitudes,address,img,cat in itertools.izip(names,bodies,latitude,longitude,addresses,image,category):
#    for currentImage in img:
#        pass
#        if name == "Urban":
#            print "SAY SOMETHING"
#            break
#i = 0
#print len(img)
#while True:
    #try:
    #    print img[0][i]
    #    i = i + 1
    #except:
        #break

#currentbody = body
#currentLatitude = latitudes
#currentLongitude = longitudes
#currentAddress = address
#currentType = cat[0]
#currentStars = cat[1]
        #guardarlo por serpara [,]
        #guardar todas las imagenes, que estan en el diccionario
#print currentName
#print currentAddress
#print currentbody
#print currentImage #si puedo hacer bucle iterando para coger las fotos
#print currentType
#print currentStars
