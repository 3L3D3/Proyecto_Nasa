# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')


def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []  #por defecto, lista vacía si no se ha implementado la funcionalidad de favoritos

    return images, favourite_list


# # función principal de la galería.
def home(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})


# función utilizada en el buscador.

def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('query', '')

    if not search_msg:
        # Si no hay texto de búsqueda, redirigir a la misma página (efecto de refrescar la página)
        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})
    else:
        # Filtrar las imágenes que contienen el texto de búsqueda en el título o la descripción
        filtered_images = [img for img in images if search_msg.lower() in img.title.lower() or search_msg.lower() in img.description.lower()]
        return render(request, 'home.html', {'images': filtered_images, 'favourite_list': favourite_list, 'search_msg': search_msg})



# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    pass


@login_required
def deleteFavourite(request):
    pass


@login_required
def exit(request):
    pass