from django.contrib import admin
from .models import Ticket, TicketComment, UserProfile, IdempotencyKey

# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketComment)
admin.site.register(UserProfile)
admin.site.register(IdempotencyKey)
