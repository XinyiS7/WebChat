from django.utils.safestring import mark_safe # 为了能够渲染markdown
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import TextSubmission
from .processing import process_text_model, process_long_text  # 我们稍后会创建这个处理函数
import markdown
import json

@require_POST
def process_longchat(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')
        mode = request.POST.get('mode', 'chat')

        # 从session获取历史（注意保持格式一致）
        chat_history = request.session.get('chat_history', [])
        processed_text = process_long_text(
            text=input_text,
            mode=mode,
            history=chat_history  # 传入历史上下文
        )
        # 调用支持上下文的处理函数
        TextSubmission.objects.create(
            input_text=input_text,
            mode=mode,
            processed_text=chat_history
        )
        # 更新对话历史（先保存用户消息）
        chat_history.append({"role": "user", "content": input_text})
        if processed_text and not processed_text.startswith("错误"):
            chat_history.append(
                {"role": "assistant", "content": processed_text})

        # 控制历史记录长度
        request.session['chat_history'] = chat_history[-6:]  # 保留最近3轮对话

        return JsonResponse({
            'input_text': input_text,
            'processed_text': processed_text,
            'mode': mode
        })

    return render(request, 'chatapp/longchat.html')


# 这里用来处理md以及按钮切换
def process_text_mdview_swt(request):
    if request.method == 'POST':
        # 获取表单提交的文本
        input_text = request.POST.get('input_text', '')

        # 这里用来接收切换按钮的值
        mode = request.POST.get('mode', 'chat')  # 默认值 'chat'，获取的是表单返回值
        # print(mode)
        # processed_text 是从 DeepSeek API 返回的 Markdown 格式文本
        processed_text = process_text_model(input_text, mode)

        # 保存到数据库
        TextSubmission.objects.create(
            input_text=input_text,
            mode=mode,
            processed_text=processed_text
        )
        # 将 Markdown 转换为 HTML，并标记为安全字符串（避免转义）
        processed_html = mark_safe(markdown.markdown(processed_text))

        return render(request, 'chatapp/resultMD.html', {
            'input_text': input_text,
            'mode': mode,
            'processed_text': processed_html  # 传递已转换的 HTML
        })
    return render(request, 'chatapp/formMD.html')