from django.db import models


class Dog(models.Model):
    """Dog Model
    name - field with the dog's name
    sex - field with a choice of the sex of the dog
    coat_color - field with the color of the dog's coat
    behavior - after with a choice of dog behavior
    breed - a field with a dog breed
    age - field with the age of the dog
    pub_date - field with the date the dog was added to the database
    """

    SEX_CHOICES = [("MALE", "Male"), ("FEMALE", "Female"), ("UNKNOWN", "Unknown")]

    BEHAVIOR_CHOICES = [
        ("CALM", "Calm"),
        ("AGGRESSIVE", "Aggressive"),
        ("PLAYFUL", "Playful"),
        ("UNKNOWN", "Unknown"),
    ]

    name = models.CharField("Name", max_length=1000)
    sex = models.TextField(choices=SEX_CHOICES, default="UNKNOWN")
    coat_color = models.TextField("Coat color", blank=True, null=True)
    behavior = models.TextField("Behavior", choices=BEHAVIOR_CHOICES, default="UNKNOWN")
    breed = models.ForeignKey(
        "Breed", on_delete=models.CASCADE, blank=True, null=True, related_name="dogs"
    )
    age = models.PositiveIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)


class Breed(models.Model):
    """
    Dog breed model
    title - breed name field
    description - breed description field
    """

    title = models.CharField("Name", max_length=1000, unique=True)
    description = models.TextField("Description", blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        The method capitalizes the first letter of the name,
        and all the rest are lowercase
        """
        self.title = self.title.capitalize()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
