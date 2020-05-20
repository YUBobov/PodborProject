from django.contrib import admin

from .models import FTTx
from .forms import FTTxForm
from .forms import ADSSForm
from .models import ADSS
from .models import Tip8
from .forms import Tip8Form
from .models import Vkanal
from .forms import VkanalForm
from .models import Vgrunt
from .forms import VgruntForm
from .models import Raspredelitelnyj
from .forms import RaspredForm
from .models import Ognestojkij
from .forms import OgnestoiForm
from .models import Universalnyj
from .forms import UniversForm


@admin.register(FTTx)
class FTTxAdmin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = FTTxForm


@admin.register(ADSS)
class ADSSAdmin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = ADSSForm


@admin.register(Tip8)
class Tip8Admin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = Tip8Form


@admin.register(Vkanal)
class VkanalAdmin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = VkanalForm


@admin.register(Vgrunt)
class VgruntAdmin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = VgruntForm


@admin.register(Raspredelitelnyj)
class RaspredAdmin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = RaspredForm


@admin.register(Ognestojkij)
class OgneAdmin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = OgnestoiForm


@admin.register(Universalnyj)
class UniversAdmin(admin.ModelAdmin):
    list_display = ('name','volokno','kN','price','link')
    list_filter = ('volokno','price')
    form = UniversForm


