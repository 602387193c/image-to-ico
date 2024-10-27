from PIL import Image
import os
import gradio as gr
import tempfile
import shutil

def convert_to_ico(image_data, output_path, sizes):
    """
    将图片转换为 ICO 格式，支持多尺寸。
    """
    try:
        with Image.open(image_data) as img:
            # 确保图片是 RGBA 模式
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 确保尺寸有效
            sizes = [size for size in sizes if size[0] <= img.size[0] and size[1] <= img.size[1]]
            if not sizes:
                sizes = [img.size]

            # 调整图像尺寸
            imgs = [img.resize(size, Image.LANCZOS) for size in sizes]

            # 保存为 ICO 格式
            imgs[0].save(
                output_path,
                format='ICO',
                sizes=[img.size for img in imgs],
            )
            return output_path
    except Exception as e:
        print(f"转换过程出错: {str(e)}")
        return None

def parse_sizes(size_strings):
    sizes = []
    for s in size_strings:
        try:
            width, height = map(int, s.lower().split('x'))
            sizes.append((width, height))
        except:
            continue
    return sizes

def ensure_output_dir():
    """
    确保输出目录存在，并返回路径
    """
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def copy_to_temp(file_path):
    """
    将文件复制到临时目录并返回新路径
    """
    temp_dir = tempfile.gettempdir()
    filename = os.path.basename(file_path)
    temp_path = os.path.join(temp_dir, filename)
    shutil.copy2(file_path, temp_path)
    return temp_path

def process_single_file(image_file, sizes, output_dir_input):
    if image_file is None:
        return None, "请先上传一张图片。"
    if not sizes:
        return None, "请至少选择一个尺寸。"

    try:
        sizes = parse_sizes(sizes)
        
        # 处理输出目录
        if output_dir_input and output_dir_input.strip():
            # 如果用户指定了输出目录，使用用户指定的
            output_dir = os.path.abspath(output_dir_input.strip())
        else:
            # 否则使用默认的output目录
            output_dir = ensure_output_dir()

        os.makedirs(output_dir, exist_ok=True)

        # 获取上传文件的文件名，以生成输出文件名
        filename = os.path.basename(image_file.name)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.ico")

        # 使用临时文件进行转换
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ico") as temp_output:
            temp_output_path = temp_output.name

        result = convert_to_ico(image_file, temp_output_path, sizes)
        if result:
            # 确保移动文件时覆盖已存在的文件
            if os.path.exists(output_path):
                os.remove(output_path)
            shutil.move(temp_output_path, output_path)
            
            # 为了让 Gradio 能够显示文件，将结果复制到临时目录
            temp_display_path = copy_to_temp(output_path)
            
            return temp_display_path, f"转换成功！文件已保存到：{output_path}"
        else:
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)
            return None, "转换失败，请检查文件格式和尺寸。"
    except Exception as e:
        return None, f"发生错误：{str(e)}"

def batch_convert(input_dir, sizes, output_dir_input, progress=gr.Progress()):
    if not os.path.exists(input_dir):
        return "输入目录不存在。"

    sizes = parse_sizes(sizes)
    if not sizes:
        return "请至少选择一个尺寸。"

    # 处理输出目录
    if output_dir_input and output_dir_input.strip():
        output_dir = os.path.abspath(output_dir_input.strip())
    else:
        output_dir = ensure_output_dir()

    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        return f"创建输出目录失败: {str(e)}"

    supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    try:
        files = [f for f in os.listdir(input_dir) if os.path.splitext(f)[1].lower() in supported_formats]
    except Exception as e:
        return f"读取输入目录失败: {str(e)}"

    total = len(files)
    if total == 0:
        return "输入目录中没有找到支持的图片文件。"

    success_count = 0
    for i, filename in enumerate(files):
        progress((i + 1) / total)
        input_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.ico")

        try:
            # 使用临时文件进行转换
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ico") as temp_output:
                temp_output_path = temp_output.name

            with open(input_path, 'rb') as f:
                result = convert_to_ico(f, temp_output_path, sizes)
                
            if result:
                if os.path.exists(output_path):
                    os.remove(output_path)
                shutil.move(temp_output_path, output_path)
                success_count += 1
            else:
                if os.path.exists(temp_output_path):
                    os.remove(temp_output_path)
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {str(e)}")
            continue

    return f"批量转换完成！成功转换 {success_count} 个文件，共 {total} 个文件。\n保存位置：{output_dir}"

with gr.Blocks(title="高清图片转ICO工具") as demo:
    gr.Markdown("""
    # 高清图片转 ICO 工具
    将常见图片格式转换为 Windows 图标（ICO）格式。
    
    **默认输出目录**: 程序所在目录下的 `output` 文件夹
    """)

    with gr.Tab("单个文件转换"):
        with gr.Column():
            image_file = gr.File(label="上传图片", file_types=["image"])
            size_choices = gr.Checkboxgroup(
                choices=["16x16", "32x32", "48x48", "64x64", "128x128", "256x256", "512x512"],
                value=["32x32", "48x48", "256x256"],
                label="选择图标尺寸"
            )
            output_dir_input = gr.Textbox(
                label="输出目录（可选）", 
                placeholder="留空则保存到项目目录下的output文件夹"
            )
            convert_btn = gr.Button("转换")
            output_file = gr.File(label="转换后的 ICO 文件")
            status_text = gr.Text(label="状态信息")

        convert_btn.click(
            process_single_file,
            inputs=[image_file, size_choices, output_dir_input],
            outputs=[output_file, status_text]
        )

    with gr.Tab("批量转换"):
        with gr.Column():
            input_dir = gr.Textbox(label="输入图片目录")
            size_choices_batch = gr.Checkboxgroup(
                choices=["16x16", "32x32", "48x48", "64x64", "128x128", "256x256", "512x512"],
                value=["32x32", "48x48", "256x256"],
                label="选择图标尺寸"
            )
            output_dir_input_batch = gr.Textbox(
                label="输出目录（可选）", 
                placeholder="留空则保存到项目目录下的output文件夹"
            )
            batch_convert_btn = gr.Button("开始批量转换")
            batch_status = gr.Text(label="状态信息")

        batch_convert_btn.click(
            batch_convert,
            inputs=[input_dir, size_choices_batch, output_dir_input_batch],
            outputs=batch_status
        )

if __name__ == "__main__":
    # 确保输出目录存在
    ensure_output_dir()
    
    # 获取系统临时目录
    temp_dir = tempfile.gettempdir()
    
    # 启动 Gradio
    demo.launch(
        server_port=7860,
        server_name="127.0.0.1",
        share=True,
        show_error=True,
        inbrowser=True,
        # 允许访问临时目录和当前目录
        allowed_paths=[".", temp_dir]
    )