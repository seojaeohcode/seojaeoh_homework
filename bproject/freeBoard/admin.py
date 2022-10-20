from django.contrib import admin
from freeBoard.models import Revenue
from freeBoard.models import Fboard
from freeBoard.models import Comment
@admin.register(Fboard)
class FboardAdmin(admin.ModelAdmin):
    list_display = ['b_no','b_title','b_date']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['c_no','member', 'c_content','c_date']

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ['r_no','r_month', 'r_revenue']