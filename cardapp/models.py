from django.db import models
from faicon.fields import FAIconField
from colorfield.fields import ColorField
from embed_video.fields import EmbedVideoField
from accounts.models import CustomUser
#from smart_selects.db_fields import ChainedForeignKey
#from smart_selects.db_fields import GroupedForeignKey


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class CardProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    title = models.CharField(max_length=35, blank=True)
    description = models.CharField(max_length=81, blank=True)

class Background(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    color_bg = ColorField("Цвет фона", default='#FF0000', help_text='Выберите цвет фона',)

class CreateBlock(models.Model):
    """ blocks  """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField("Название блока", max_length=100)
    close = models.BooleanField("Свернуть блок", default=False)
    order = models.SmallIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('order',)
        verbose_name = 'Мой раздел'
        verbose_name_plural = 'Мои разделы'

class CreateLink(models.Model):
    """ links  """

    LINK_CHOICES = (
        (1, ("Обычная ссылка")),
        (2, ("Электронная почта")),
        (3, ("Номер телефона"))
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    block = models.ForeignKey(CreateBlock, on_delete=models.CASCADE, related_name='blocklinks')
    name = models.CharField("Название", max_length=100, help_text='Максимально 100 символов')
    status = models.IntegerField("Тип ссылки", choices=LINK_CHOICES, default=1)
    url = models.CharField("Ссылка", max_length=900, help_text='Вставьте ссылку с пртоколом http:// или https://, если выбран тип электронной почты или телефона, то просто впишите вашу почту или номер телефона')
    icon = FAIconField("Иконка", help_text='Выберите иконку')
    color_icon = ColorField("Цвет иконки", default='#FFF', help_text='Выберите цвет иконки')
    color_bg = ColorField("Цвет фона", default='#FF0000', help_text='Выберите цвет фона')
    order = models.SmallIntegerField("Позиция", default=0, db_index=True, help_text='Номер позиции в очереди', blank=True)
    choose = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order',)
        verbose_name = 'Моя ссылка'
        verbose_name_plural = 'Мои ссылки'

class CreateFaq(models.Model):
    """ faq  """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    block = models.ForeignKey(CreateBlock, on_delete=models.CASCADE, related_name='blockfaq')
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.SmallIntegerField(default=0, db_index=True,)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('order',)
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'

# tables models
class TableCategory(models.Model):
    """ table category  """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    block = models.ForeignKey(CreateBlock, on_delete=models.CASCADE, related_name='blocktablecat',)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория таблицы'
        verbose_name_plural = 'Категории таблицы'

class TableItems(models.Model):
    """ table items  """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(TableCategory,
                                 related_name='tableitems',
                                 on_delete=models.CASCADE,
                                 )
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Содержимое таблицы'
        verbose_name_plural = 'Содержимое таблицы'


class AddImage(models.Model):
    """ images  """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    block = models.ForeignKey(CreateBlock, on_delete=models.CASCADE, related_name='blockimages')
    img = models.ImageField(upload_to='images/%Y/%m/%d', help_text='Рекомендуем добавлять картинки одного размера', verbose_name='Загрузите картинку')

class YoutubeVideo(models.Model):
    """ videos  """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    block = models.ForeignKey(CreateBlock, on_delete=models.CASCADE, related_name='blockvideos')
    url = EmbedVideoField(default='', verbose_name='Вставьте ссылку', help_text='Скопируйте и вставьте ссылку с youtube')



