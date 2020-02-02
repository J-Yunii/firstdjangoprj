from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    # author는 사용자의 createsuperuser 혹은 superuser가 만든 계정자료와 연동
    # 'auth.User' 는 장고에서 말하는 admin 계정 class(자동생성됨) - id,pw,pk등등이 속성으로 있음
    # 계정은 여러개 만들 수 있음 : pk로 식별
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # on_delete = models.CASCADE(회원탈퇴하면 연동된 글들이 같이 지워짐)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # CharField는 글자수 제한
    title = models.CharField(max_length=200)
    text = models.TextField()
    # 작성일, default = timezone.now(자동으로 서버시간이 들어감)
    created_date = models.DateTimeField(default = timezone.now)
    
    # 게시일(공개시간)
    # blank=True일 경우 컬럼이 비어있어도 됨,  null=True는 null값 넣기 허용
    published_date = models.DateTimeField(blank=True, null=True)
    
    # 게시하는 함수, self꼭 써줘야함 table에서 row하나(글(Post) 하나)를 뜻함
    # row하나를 self에 저장해서 수정뒤 반영
    def publish(self):
        self.published_date = timezone.now()
        # 수정하고 반영해줘야 함!!
        self.save()
    
    # admin에 보여질 정보를 models에서 정의해줘야함
    def __str__(self):
        return self.title
    
    
