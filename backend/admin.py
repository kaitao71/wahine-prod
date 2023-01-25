from django.contrib import admin
from backend.models import *
# Register your models here.
import json
import logging
from django.db.models import JSONField 
from django.forms import widgets


logger = logging.getLogger(__name__)


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)

class JsonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }
    search_fields = ('user',)
    list_display = ('uuid', 'user', 'data', 'item_type','created_at','modified_at')
    list_display_links = ('uuid', 'user', 'data', )
    list_filter = ('user','item_type')

    def value1(self, instance):
        data = json.dumps(instance.data)
        return data[0:9]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','plan','created_at',)

admin.site.register(Item, JsonAdmin)

admin.site.register(PropertyType)
admin.site.register(ResidentialType)
