from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from board.forms import BoardForm2
from board.models import Board



def nnhome(request):
    return render(request, 'board/testmain.html')      # 테스트

def nhome(request):
    return render(request, 'board/nhome.html')         # sbk_첫번째페이지

def nboard(request):
    return render(request, 'board/nboard.html')        # sbk_두번째페이지


#@login_required(login_url='/users/login')
def register(request):
    if request.method == "GET":
        boardForm = BoardForm2()
        return render(request, 'board/register.html',
                      {'boardForm': boardForm})
    elif request.method =="POST":
        boardForm = BoardForm2(request.POST)

        if boardForm.is_valid():
            board = boardForm.save(commit=False)
            board.writer=request.user
            board.save()
            return redirect('/board/register')


#@login_required(login_url='/users/login')
def list(request):
    posts = Board.objects.all()
    lll = 1
    return render(request, 'board/list.html',
                  {'posts': posts})


#@login_required(login_url='/users/login')
def read(request, bid):
    post = Board.objects.get( Q(id=bid))
    return  render(request, 'board/read.html',
                   {'post': post})


#@login_required(login_url='/users/login')
def register(request):
    if request.method == "GET":
        boardForm = BoardForm2()
        return render(request, 'board/register.html',
                      {'boardForm': boardForm})
    elif request.method =="POST":
        boardForm = BoardForm2(request.POST)

        if boardForm.is_valid():
            com = boardForm.save(commit=False)
            com.writer=request.user
            com.save()
            return redirect('/board/register')