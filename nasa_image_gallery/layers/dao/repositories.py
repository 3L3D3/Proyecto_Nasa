#repositories.py
# capa DAO de acceso/persistencia de datos.

from nasa_image_gallery.models import Favourite

def saveFavourite(fav):
    try:
        favourite = Favourite.objects.create(
            title=fav.title,
            description=fav.description,
            image_url=fav.image_url,
            date=fav.date,
            user=fav.user
        )
        return favourite
    except Exception as e:
        print(f"Error al guardar el favorito: {e}")
        return None

def getAllFavouritesByUser(user):
    favourite_list = Favourite.objects.filter(user=user).values('id', 'title', 'description', 'image_url', 'date')
    return list(favourite_list)



def deleteFavourite(fav_id):
    try:
        favourite = Favourite.objects.get(id=fav_id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {fav_id} no existe.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False