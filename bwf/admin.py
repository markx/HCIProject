from django import forms
from django.contrib import admin

from bwf.models import User, Friend,  Bill

admin.site.register(User)
admin.site.register(Friend)

class BillAdminForm(forms.ModelForm):
    class Meta:
        model=Bill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BillAdminForm, self).__init__(*args, **kwargs)

        user_choices = tuple( (each.email, "user: "+ each.get_full_name()+"  "+each.email) for each in  User.objects.all() )
        friend_choices = tuple( (each.email, "friend: "+ each.get_full_name()+"  "+each.email) for each in  Friend.objects.all() )

        self.fields['creditor'] = forms.ChoiceField( user_choices+friend_choices )
        self.fields['debtor'] = forms.ChoiceField( user_choices+friend_choices )

class BillAdmin(admin.ModelAdmin):
    form = BillAdminForm
admin.site.register(Bill, BillAdmin)
