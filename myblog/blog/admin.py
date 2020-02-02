from django.contrib import admin
from blog.models import Post

# admin 계정에 모델 등록하기
admin.site.register(Post)
