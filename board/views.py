from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from board.forms import BoardForm
from board.models import Board


@login_required(login_url='/user/login')
def register(request):
    if request.method == "GET":
        boardForm = BoardForm()
        return render(request, 'board/register.html',
                      {'boardForm': boardForm})
    elif request.method =="POST":
        boardForm = BoardForm(request.POST)

        if boardForm.is_valid():
            board = boardForm.save(commit=False)
            board.writer=request.user
            board.save()
            return redirect('board/register')


@login_required(login_url='/user/login')
def list(request):
    posts = Board.objects.all()
    return render(request, 'board/list.html',{'posts': posts})


@login_required(login_url='/user/login')
def read(request, bid):
    post = Board.objects.get( Q(id=bid))
    return  render(request, 'board/read.html',
                   {'post': post})

@login_required(login_url='/user/login')
def register(request):
    if request.method == "GET":
        boardForm = BoardForm()
        return render(request, 'board/register.html',
                      {'boardForm': boardForm})
    elif request.method =="POST":
        boardForm = BoardForm(request.POST)

        if boardForm.is_valid():
            board = boardForm.save(commit=False)
            board.writer=request.user
            board.save()
            return redirect('board/register')