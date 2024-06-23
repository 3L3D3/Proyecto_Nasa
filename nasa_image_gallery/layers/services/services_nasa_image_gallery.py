# service.py
from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user

def getAllImages(input=None):
    json_collection = transport.getAllImages(input)
    
    images = [
        mapper.NASACard(
            title=item['data'][0]['title'],
            description=item['data'][0]['description'],
            image_url=item['links'][0]['href'],
            date=item['data'][0]['date_created'][:10]  # Asegurando el formato de fecha YYYY-MM-DD
        )
        for item in json_collection
        if 'links' in item and item['links'] and 'href' in item['links'][0]
    ]
    
    return images

def getImagesBySearchInputLike(input):
    return getAllImages(input)

def saveFavourite(request):
    fav = mapper.NASACard(
        title=request.POST.get('title'),
        description=request.POST.get('description'),
        image_url=request.POST.get('image_url'),
        date=request.POST.get('date')[:10],  # Asegurando el formato de fecha YYYY-MM-DD
        user=get_user(request)
    )
    repositories.saveFavourite(fav)

def getAllImagesAndFavouriteList(request):
    images = getAllImages()
    favourite_list = repositories.getAllFavouritesByUser(get_user(request))
    return images, favourite_list

def getAllFavouritesByUser(request):
    user = get_user(request)
    favourite_list = repositories.getAllFavouritesByUser(user)
    return favourite_list

def deleteFavourite(request):
    fav_id = request.POST.get('id')
    return repositories.deleteFavourite(fav_id)