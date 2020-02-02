from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post
# 폼작성할 때 로드해야함!
from .forms import PostForm

# 장고 ORM
# 꺼내기 함수 중 create는 적재 함수
# from django.contrib.auth.models import Use
# User.objects.all()로 user 이름 확인
# me = User.objects.get(username='ola')
# Post.objects.create(author=me, title='Sample title', text='Test')
# 작성시간은 디폴드 값으로, 게시시간은 null로 들어감

# Post.objects.filter(author=me)
# filter함수는 용도는 get과 같으나 여러개를 가져올 수 있다. list로 들고옴. 또한 조건을 복잡하게 걸어줄 수 있음
# Post.objects.filter(컬럼명__contains='조건')


# Post.objects.filter(published_date__lte=timezone.now())
# lte는 우측에 있는 시간보다 이전에 있는 것들만 가져옴
# 파이썬은 시간을 초단위로 저장, 기준시간(1970년 1월 1일 00시 00초)을 정하고 1초가 지날 때 마다 1씩 더함
# 크기가 더 작은 게 이전시간 큰게 이후시간이 됨
# 하지만 결과가 안나오죠! 왜??
# published_date에 데이터가 없어서 비교 자체가 안되어서

# post = Post.objects.get(title='안녕하세요 bamtol입니다')
# type(post)
# <class 'blog.models.Post'> Post라는 class타입
# QuerySet : class의 objects들(테이블에서 각 row들의 column들이 list의 요소로 저장됨)

# post.publish() (post 자료형이 Post class니깐!)
# publish 메서드를 사용해서 게시함

# 두 개 이상의 조건 연달아 쓸 수 있음
# Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html',{'posts':posts})

# pk는 우아한 url패턴에서 가져온 것
def post_detail(request, pk):
    # pk에 해당하는 게시판 글은 무조건 1개이므로 get을 쓴다!
    # get_object_or_404는 Post.objects와 같이 쓰이는 함수가 아니라 단독으로 쓰이는 함수!!, 문법 기억해두기
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{'post':post})

# post_new는 폼으로 연결해주는 함수이다.
def post_new(request):
    
    # form.py의 method="post"이므로 form을 사용해 들어온 자료는 무조건 post여야함
    # POST방식으로 자료가 들어오는지 검사 -> POST방식으로 들어오면 적재하라!
    # request는 사용자의 요청, method는 요청 방식
    if request.method == "POST":
        form = PostForm(request.POST)
        
        # .is_vaild()는 form에 유효한 값이 들어왔는지를 검사(자료형)
        if form.is_valid():
            # commit은 임시저장 언제든지 롤백할 수 있도록, author와 published_date가 비어있어서 실제 DB에 반영이 안됨
            # 우선 form에서 입력한 title, text 정보를 넘겨받고(pk, crete_date정보는 자동입력)
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # 모든 컬럼 정보 입력후 이제 저장
            post.save()
            
            # 글 다 썼으면 detail 페이지에서 쓴 글 확인
            # redirect는 특정 페이지로 돌아가라 
            return redirect('post_detail', pk=post.pk)
            
    # get방식으로 들어오는 자료는 무시해야 함: 빈 폼을 저장해라
    else:
        # 만들어놨던 폼 양식을 가져오기 위해서는
        # 변수 = 폼양식()를 써야 한다. ()가 우측에 붙음에 주의.
        # 현재 코드는 PostForm()양식을 따라 만들것임을 보여준다.
        # 깡통 폼
        form = PostForm()

    # 저장한 폼 양식은 템플릿 파일에 같이 넘겨야 한다.
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    # 글을 수정해야 하기 때문에 기존에 입력되어 있던 자료를 가져오는게 먼저임.
    # 개발자 에러페이지가 아니라 사용자 에러 페이지를 띄어줌
    post = get_object_or_404(Post,pk=pk)
    
    # GET방식, POST방식 구분
    # POST는 Form 내부의 submit버튼으로 전송되는 자료, GET은 url로 들어오는 자료(★a태그로 넘어오는 경우)
    # POST 방식은 수정이 완료된 상황을 나타냄!! => 기존 것에 덮어씌어줌
    if request.method == 'POST':
        # POST 방식인 경우는 기존 자료 post에 새로 들어온 정보를 덮어씌움
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # 게시시간을 다시 현재 서버시간으로 변경
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    
    # get방식으로 들어왔으면 수정 시작
    # db에서 기존 글을 가져와서 PostForm에 기입해둠
    else:
        # 만약 post방식이 아닌 경우라면 get방식 이므로 수정 직전임
        # 따라서 폼으로 다시 연결해줘야함. 이 때의 폼은 수정용 폼이며 수정용 폼에는 기존에 써놨던 글이 먼저 입력되어 있어야 하므로
        # 감안해서 기존 글의 내용이 담겨있는 post를 통해 instance로 넘겨줌
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form':form})











