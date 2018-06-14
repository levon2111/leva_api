from django.contrib import admin

from apps.users.models import User, Syndicate, SyndicateMember, InvitedToSyndicate


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'first_name',
        'last_name',
        'phone',
        'zip_code',
        'email',
        'email_confirmation_token',
        'reset_key',
    ]

    search_fields = [
        'username',
        'first_name',
        'last_name',
        'phone',
        'email',
    ]

    list_filter = [
        'created_at'
    ]

    class Meta:
        model = User


@admin.register(Syndicate)
class SyndicateModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'name',
        'description',
        'focus',
        'industry',
        'privacy',
        'currency',
        'horizon',
        'capital_raised',
        'min_commitment',
        'leadership_commitment',
        'personal_note',
    ]

    class Meta:
        model = Syndicate


@admin.register(SyndicateMember)
class SyndicateMemberModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'syndicate',
    ]

    class Meta:
        model = SyndicateMember


@admin.register(InvitedToSyndicate)
class InvitedToSyndicateModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'syndicate',
        'token',
    ]

    class Meta:
        model = InvitedToSyndicate
