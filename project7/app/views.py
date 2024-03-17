from django.shortcuts import render,get_object_or_404
from .models import Post, Category, Sub_Cat, Comment, About, Author, Video

from .forms import CommentForm, UserForm, UserAuthenticationForm, UserInfoForm, PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime


def home(request):
    posts = Post.objects.filter(is_approved=True)
    #=======================================================================================================

    # trending topic section
    try:
        all_topics = posts.order_by('-view')[:20]
        trending_topic = []
        for post in all_topics:
            if trending_topic:
                if not post.sub_cat in (trending_topic):
                    trending_topic.append(post.sub_cat)
            else:
                trending_topic.append(post.sub_cat)
    except posts.DoesNotExist:
        all_topics = None

    trending_topic = trending_topic[:6]
    #==========================================================================================================


    # most popular posts
    all_pop_post = posts.order_by('date','-view')
    four_cat = 0
    popular_post_list = []
    if all_pop_post:
        for post in all_pop_post:
            if popular_post_list:
                if not post.sub_cat in popular_post_list and four_cat <= 3:
                    popular_post_list.append(post.sub_cat)
                    four_cat += 1
            else:
                popular_post_list.append(post.sub_cat)
                four_cat += 1
    else:
        popular_post_list = None

    print(f'{popular_post_list}___________________')
    #=========================================================================================================

    new_posts = posts.order_by('-date')[:6]
    #========================================================================================================


    # vidoes part
    all_videos = Video.objects.order_by('-date')[:5]
    try:
        first_video = all_videos[0]
    except IndexError:
        first_video = None
    all_videos = all_videos[1:5]
    print(f'{first_video}-----------------')
    print(all_videos)


    context = {
        'posts': posts,
        'trending_topics': trending_topic,
        'pop_post': popular_post_list,
        'new_posts':new_posts,
        'first_video': first_video,
        'all_videos': all_videos,
    }
    return render(request,'home.html',context=context)


def page404(request):
    return render(request,'404.html')


def about(request):
    about_data = About.objects.all()
    if about_data:
        about_data = about_data[0]

    context = {
        'about': about_data,
    }
    return render(request,'about.html',context)


def author(request,id):
    if request.user.is_authenticated:
        if id == int(request.user.id):
            if request.method == 'POST':
                form = UserInfoForm(request.POST)
                if form.is_valid():
                    author_model = get_object_or_404(Author,pk=id)
                    info = form.cleaned_data.get('info')
                    author_model.info = info
                    author_model.save()
                else:
                    return HttpResponse('user information form is not valid')
            else:
                form = UserInfoForm()
            all_obj = Author.objects.all()
            author = get_object_or_404(Author,pk=id)
            author_posts = Post.objects.filter(post_author=author,is_approved=True)
        else:
            return HttpResponseRedirect('/404/')
    else:
        return HttpResponse('لومړی باید تاسو یو اکونټ جوړ کړی ترسو خپل اکونټ ته ننوځی. تاسی کولاشی د یو پوسټ معلوماتو پاڼه کړی د اکونټ جوړیدو برخه وګورې.')


    context = {
        "author": author,
        "author_posts":author_posts,
        'form': form
    }
    return render(request,'author.html',context)


def contact(request):
    posts = Post.objects.filter(is_approved=True).order_by('-id')[:3]
    print(posts)

    context = {
        'posts': posts,
    }
    return render(request,'contact.html',context)


def post_list(request,id):
    try:
        categories = Category.objects.get(pk=id)
    except:
        return HttpResponseRedirect('/404/')

    context = {
        'main_cat': categories,
    }
    return render(request,'post-list.html',context=context)


def sub_post_list(request, id):
    try:
        sub_cat = Sub_Cat.objects.get(pk=id)
    except:
        return HttpResponseRedirect('/404/')

    context = {
        'sub_cat': sub_cat,
        'main_cat':None,
    }

    return render(request, 'post-list.html', context=context)


def post_details(request,id):
    try:
        single_post = get_object_or_404(Post,pk=id)
    except:
        return HttpResponseRedirect('/404/')
    views = single_post.view
    single_post.view = views + 1

    single_post.save()
    if request.method == "POST":
        condition = int(request.POST.get('cond'))

        if condition != 0 :
            cmn_id = condition
            comment = get_object_or_404(Comment,pk=cmn_id)
            form = CommentForm(request.POST,post=single_post,replay=comment)

        else:
            form = CommentForm(request.POST,post=single_post)
        if form.is_valid():
            form.save()
            form = CommentForm()
            print(f'data save successfully!')
    else:
        form = CommentForm()

    userform = UserForm()
    user_auth_form = UserAuthenticationForm()
    no_comments = single_post.comments.all()
    no_comments = len(no_comments)

    related_post = Post.objects.filter(post_cat=single_post.post_cat,is_approved=True)[:5]
    recent_post = Post.objects.filter(is_approved=True).order_by('-id')[:3]


    context = {
        'single_post': single_post,
        'form': form,
        'related_post': related_post,
        'recent_post':recent_post,
        'userform': userform,
        'user_auth_form': user_auth_form,
        'no_comments': no_comments,

    }
    return render(request, 'post-details.html',context=context)


def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.post_author = request.user
                post.date = datetime.now()
                post.save()
                messages.success(request,"ستاسو پوسټ به په ۲۴ ساعتونو کی وکتل شی. که چیرته ستاسو پوسټ په ویب پاڼه ښکاره نه شو. نو تاسی شاید غلط عکس یا غلط پوسټ عنوان او یا مو د پوسټ محتوا غلته وی. نو بیا مهربانی وکړی  دوهم ځلی پوسټ وکړئ.")
                print(f'/author/{int(request.user.id)}')
                return HttpResponseRedirect(f'/author/{int(request.user.id)}/')
        else:
            form = PostForm()
    else:
        return HttpResponseRedirect('/404/')

    context = {
        'form': form,
    }

    return render(request,'create-post.html',context)


def privacy(request):
    return render(request,'privacy-policy.html')


def search(request):
    try:
        search_value = request.GET['search_val']
    except:
        return HttpResponseRedirect('/404/')
    posts = Post.objects.filter(title__icontains=search_value)


    context = {
        'posts': posts,
    }
    return render(request,'search.html',context=context)


def maintenance(request):
    return render(request,'maintenance.html')


def register_user(request):

    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            author = form.save()
            login(request,author)
            return HttpResponseRedirect(f'/author/{author.id}/')
        else:
            print(form.errors)
            return HttpResponse('form not valid')
    else:
        return HttpResponseRedirect('/404/')


def author_login(request):

    if request.method == 'POST':
        form = UserAuthenticationForm(request,data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(request,username=uname, password=upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(f'/author/{user.id}/')
            else:
                return HttpResponse('user is none!')
        else:
            print(form.errors)
            return HttpResponse('invalid login credential')
    else:
        return HttpResponseRedirect('/404/')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/404/')