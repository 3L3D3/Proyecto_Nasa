# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def index_page(request):
    return render(request, 'index.html')

def getAllImagesAndFavouriteList(request):
    images, favourite_list = services_nasa_image_gallery.getAllImagesAndFavouriteList(request)
    return images, favourite_list

@login_required
def home(request):
    images = services_nasa_image_gallery.getAllImages()  # Obtenemos todas las imágenes
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)  # Obtenemos favoritos del usuario

    # Crear un conjunto de títulos de imágenes favoritas para facilitar la búsqueda
    favourite_titles = set(fav['title'] for fav in favourite_list)

    # se agrega la propiedad "estaEnTusFavoritos a cada imagen y se anexa al home.html"
    for image in images:
        image.estaEnTusFavoritos = image.title in favourite_titles

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('query', '')

    if not search_msg:
        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})
    else:
        filtered_images = [img for img in images if search_msg.lower() in img.title.lower() or search_msg.lower() in img.description.lower()]
        return render(request, 'home.html', {'images': filtered_images, 'favourite_list': favourite_list, 'search_msg': search_msg})

@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.deleteFavourite(request)
    return redirect('favoritos')

def exit(request):
    logout(request)
    return redirect('index-page')