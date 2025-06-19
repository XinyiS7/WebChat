from django.shortcuts import render
from django.utils.safestring import mark_safe # 为了能够渲染markdown
from django.shortcuts import render, redirect
from .models import TextSubmission
from .processing import process_text, process_text_model  # 我们稍后会创建这个处理函数
import markdown
def submit_text(request):
    if request.method == 'POST':
        # 获取表单提交的文本
        input_text = request.POST.get('input_text', '')

        # 处理文本
        processed_text = process_text(input_text)

        # 保存到数据库
        TextSubmission.objects.create(
            input_text=input_text,
            processed_text=processed_text
        )

        # 显示结果
        return render(request, 'chatapp/result.html', {
            'input_text': input_text,
            'processed_text': processed_text
        })

    # GET 请求时显示空表单
    return render(request, 'chatapp/form.html')


# 这里是用来处理需要渲染的文字，将 `processed_text` 从 Markdown 转换为 HTML
def process_text_mdview(request):
    if request.method == 'POST':
        # 获取表单提交的文本
        input_text = request.POST.get('input_text', '')

        # 这里用来接收切换按钮的值
        mode = request.POST.get('mode', 'chat')  # 默认值 'chat'

        # processed_text 是从 DeepSeek API 返回的 Markdown 格式文本
        processed_text = process_text(input_text)

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