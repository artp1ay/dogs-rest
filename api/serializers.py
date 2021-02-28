from rest_framework import serializers

from .models import Dog, Breed


class ChoiceField(serializers.ChoiceField):
    """

    Поле выбора варианта ответа
    принимает и отдает человека-читаемые варианты

    """

    def to_representation(self, obj):
        if obj == "" or self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class DogSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Dog (Собак)"""

    breed = serializers.CharField(
        source="breed.title",
    )
    sex = ChoiceField(
        choices=Dog.SEX_CHOICES,
        required=False,
    )
    behavior = ChoiceField(
        choices=Dog.BEHAVIOR_CHOICES,
        required=False,
    )

    class Meta:
        model = Dog
        fields = (
            "name",
            "sex",
            "coat_color",
            "behavior",
            "breed",
            "age",
        )


class BreedSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Breed (Породы)"""

    class Meta:
        model = Breed
        fields = ("title", "description")
