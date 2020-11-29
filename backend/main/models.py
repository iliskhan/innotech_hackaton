from django.db import models


class OccupationType(models.TextChoices):
    """
    Тип Опроса
    """
    work = 'работа'
    school = 'школа'
    university = 'университет'


class VkUserEducation(models.Model):
    university = models.CharField(max_length=255, blank=True, null=True)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    graduation = models.IntegerField(max_length=10, blank=True, null=True)


class VkUserOccupation(models.Model):
    type = models.CharField(
        choices=OccupationType.choices,
        max_length=20,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255, blank=True, null=True)


class VkUserPersonal(models.Model):
    NO_POLITICS = 0
    COMMUNIST = 1
    SOCIALIST = 2
    MODERATE = 3
    LIBERAL = 4
    CONSERVATIVE = 5
    MONARCH = 6
    ULTRACONSERVATIVE = 7
    INDIFFERENT = 8
    LIBERTARIAN = 9

    POLITICAL_CHOICES = (
        (NO_POLITICS, 'Не указано'),
        (COMMUNIST, 'Коммунистические'),
        (SOCIALIST, 'Социалистические'),
        (MODERATE, 'Умеренные'),
        (LIBERAL, 'Либеральные'),
        (CONSERVATIVE, 'Консервативные'),
        (MONARCH, 'Монархические'),
        (ULTRACONSERVATIVE, 'Ультраконсервативные'),
        (INDIFFERENT, 'Индифферентные'),
        (LIBERTARIAN, 'Либертарианские')
    )

    NONE = 0
    FULLY_NEGATIVE = 1
    NEGATIVE = 2
    COMPROMISS = 3
    NEUTRAL = 4
    APPROVE = 5

    BAD_HABIT_CHOICES = (
        (NONE, 'Не указано'),
        (FULLY_NEGATIVE, 'Резко негативное'),
        (NEGATIVE, 'Негативное'),
        (COMPROMISS, 'Компромиссное'),
        (NEUTRAL, 'Нейтральное'),
        (APPROVE, 'Положительное')
    )
    langs = models.CharField(max_length=255, blank=True, null=True)
    religion = models.CharField(max_length=255, blank=True, null=True)
    inspired_by = models.CharField(max_length=255, blank=True, null=True)
    smoking = models.CharField(max_length=255, blank=True, null=True, choices=BAD_HABIT_CHOICES)
    alcohol = models.CharField(max_length=255, blank=True, null=True, choices=BAD_HABIT_CHOICES)
    political = models.CharField(max_length=255, blank=True, null=True, choices=POLITICAL_CHOICES)


class VkUserData(models.Model):
    MALE = 1
    FEMALE = 2
    NO_SEX = 0

    GENDER = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (NO_SEX, 'Не указан'),
    )

    vk_user_id = models.IntegerField(blank=False, null=False)
    avatar = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    bdate = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    contacts = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    interests = models.CharField(max_length=255, blank=True, null=True)
    education = models.OneToOneField(VkUserEducation, on_delete=models.CASCADE, null=True, blank=True)
    occupation = models.OneToOneField(VkUserOccupation, on_delete=models.CASCADE, null=True, blank=True)
    personal = models.OneToOneField(VkUserPersonal, on_delete=models.CASCADE, null=True, blank=True)
    sex = models.CharField(max_length=255, blank=True, null=True, choices=GENDER)
