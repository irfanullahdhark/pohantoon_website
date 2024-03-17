from .models import Comment, Author, Post
from tinymce.widgets import TinyMCE
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-controls','rows':4}),label='ځرګندونه')
    class Meta:
        model = Comment
        fields = ['name','email','message']
        labels = {
            'name': 'نوم',
            'email': 'بریښنالیک',
            'message': 'ځرګندونه'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-controls'}),
            'email': forms.EmailInput(attrs={'class': 'form-controls'}),
        }

    def __init__(self, *args, post=None,replay=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.post = post
        self.replay = replay

    def save(self, commit=True):
        instace = super().save(commit=False)
        instace.post = self.post
        instace.replay = self.replay


        if commit:
            instace.save()

        return commit


class UserForm(UserCreationForm):
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-controls','name': 'password', "placeholder": "خپل پټ نوم داخل کړئ."}))
    password2 = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-controls', "placeholder": 'خپل پټ نوم تايید کړئ.'}))
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-controls', 'placeholder': 'خپل نوم مو داخل کړئ.'}))

    class Meta(UserCreationForm.Meta):
        model = Author
        fields = UserCreationForm.Meta.fields + ('name','image')

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-controls',"placeholder":'خپل استعمالوونکي نوم داخل کړئ'}),
        }


class UserInfoForm(UserCreationForm):
    username = None
    password1 = None
    password2 = None
    image = None
    name = None
    no_post = None
    info = forms.CharField(widget = forms.Textarea(attrs={'class':'form-controls',"placeholder":'خپل ځان په اړه مو معلومات دلته ولیکئ ' , "style":'border:1px solid #555;'}))
    class Meta:
        model = Author
        fields = ['info']


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Author
        fields = ['username','password']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['orginal_source_name', 'post_cat', 'sub_cat', 'title', 'image', 'description']

        widgets = {
            'orginal_source_name': forms.TextInput(attrs={'class':'form-control'}),
            'post_cat': forms.Select(attrs={'class': 'form-control','style':"font-size: 20px;"}),
            'sub_cat': forms.Select(attrs={'class': 'form-control','style':"font-size: 20px;"}),
            'title': forms.TextInput(attrs={'class': 'form-control','style':"font-size: 20px;"}),
            'image': forms.FileInput(attrs={'class': 'form-control','style':"font-size: 20px;"}),
            'description': TinyMCE(attrs={'cols': 80, 'rows':20})


        }

        labels = {
            'orginal_source_name': 'د اصلی سرچینی یا لیکوال نوم',
            'post_cat':'د پوسټ کټیګوری',
            'sub_cat':'د پوسټ sub کټیګوری',
            'title':'د پوسټ عنوان',
            'image': 'د پوسټ عکس',
            'description':'د پوسټ تفصیل'
        }





