from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ChatMessageCreateForm


@login_required
def chat(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()
    
    if request.method == 'POST':
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author_id = request.user.id
            message.group = chat_group
            message.save()
            return redirect('chat')

    return render(request, 'chat/chat.html',{'chat_messages':chat_messages,'form':form })

