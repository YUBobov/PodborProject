from django.db import models


class FTTx(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'FTTx'
        verbose_name_plural = 'FTTx'


class ADSS(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'Подвесной самонесущий, ADSS'
        verbose_name_plural = 'Подвесной самонесущий, ADSS'


class Tip8(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'Подвесной, тип-8'
        verbose_name_plural = 'Подвесной, тип-8'


class Vkanal(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'В канализацию'
        verbose_name_plural = 'В канализацию'


class Vgrunt(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'В грунт'
        verbose_name_plural = 'В грунт'


class Raspredelitelnyj(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'Распределительный'
        verbose_name_plural = 'Распределительный'


class Ognestojkij(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'Огнестойкий'
        verbose_name_plural = 'Огнестойкий'


class Universalnyj(models.Model):
    objects = models.Manager() #Параметр для работы с объектами модели
    name = models.TextField(
        verbose_name='Название',
    )
    volokno = models.PositiveIntegerField(
        verbose_name='Кол-во волокн',
    )
    kN= models.TextField(
        verbose_name='кН',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    link = models.URLField(
        verbose_name='Ссылка',
        unique=True,
    )

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'Универсальный'
        verbose_name_plural = 'Универсальный'