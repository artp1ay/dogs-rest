from .models import Breed


def create_or_update(serializer):
    """
    The method brings the name of the breed to a single structure,
    If there is no object found, it first creates it.
    """
    title = serializer.validated_data["breed"]
    title = title["title"].capitalize()
    breed = Breed.objects.get_or_create(title=title)
    return breed
