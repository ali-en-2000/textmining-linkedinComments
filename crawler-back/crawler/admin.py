from django.contrib import admin

from .models import Comment, Post, miningData


class postAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'url', 'password')


class commentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'postUrl')


class minginDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'postUrl', 'vader_neg', 'vader_neu',
                    'vader_pos', 'vader_compound', 'roberta_neg', 'roberta_neu', 'roberta_pos')


admin.site.register(Post, postAdmin)
admin.site.register(Comment, commentAdmin)
admin.site.register(miningData, minginDataAdmin)
