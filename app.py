import gradio as gr
import traceback
import re


def hello_world_fn(username: str) -> tuple[str, str]:
    try:
        return f"HELLO WORLD\n{username.upper()}", "SUCCESS"
    except Exception as e:
        return f"opus! some exception {e}\n{traceback.format_exc()}", "FAILED"


# 函数的作用是解析出字符串中所有在<p>与</p>之间的内容,如果存在嵌套标签那么也应该过滤掉其他的标签，不同的标签之间用换行符隔开
def html_parser_fn(html: str) -> tuple[str, str]:
    try:
        pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)

        # 提取所有匹配的内容
        matches = pattern.findall(html)

        # 对每个匹配的内容，移除嵌套的 HTML 标签
        cleaned_contents = []
        for match in matches:
            # 移除嵌套的 HTML 标签（包括自闭合标签和普通标签）
            clean_text = re.sub(r'<[^>]+>', '', match).strip()
            cleaned_contents.append(clean_text)

        # 将不同标签的内容用换行符隔开
        result = '\n'.join(cleaned_contents)

        # 返回解析结果和状态信息
        return result, "SUCCESS" if cleaned_contents else "NO CONTENT FOUND"
    except Exception as e:
        return f"opus! some exception {e}\n{traceback.format_exc()}", "FAILED"


def main() -> None:
    with gr.Blocks(title="DeepLang Data test project") as demo:
        with gr.Tab("hello world 0"):
            raw_input = gr.Textbox(lines=1, placeholder="输入你的名字(英文)", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=hello_world_fn,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )

        with gr.Tab("hello world 1"):
            raw_input = gr.Textbox(lines=1, placeholder="输入你的名字(英文)", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=hello_world_fn,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )

        with gr.Tab("html parser"):
            raw_input = gr.Textbox(lines=1, placeholder="输入html", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=html_parser_fn,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )

    demo.queue(default_concurrency_limit=100).launch(
        inline=False,
        debug=False,
        server_name="127.0.0.1",
        server_port=8081,
        show_error=True,
    )


if __name__ == "__main__":
    main()
