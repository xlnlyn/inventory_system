from PIL import Image, ImageDraw
import sys

# 设置输出编码为 UTF-8
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def create_icon():
    # 创建一个 256x256 的透明背景图像
    size = 256
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # 设置基本参数
    margin = size // 8
    box_color = (52, 152, 219)  # 使用清新的蓝色

    # 绘制主体箱子
    draw.rectangle(
        [margin, margin * 2, size - margin, size - margin], 
        fill=box_color,
        outline=(41, 128, 185),  # 稍深的蓝色作为边框
        width=2
    )

    # 绘制箱子盖子
    draw.polygon([
        (margin, margin * 2),           # 左下
        (margin // 2, margin),          # 左上
        (size - margin // 2, margin),   # 右上
        (size - margin, margin * 2)     # 右下
    ], 
    fill=box_color,
    outline=(41, 128, 185),
    width=2)

    # 添加一些细节 - 箱子边缘的高光
    highlight_color = (133, 193, 233)  # 浅蓝色
    draw.line(
        [(margin + 10, margin * 2 + 10), (margin + 40, margin * 2 + 10)],
        fill=highlight_color,
        width=2
    )

    # 保存图标
    # 支持多种尺寸的图标
    image.save('inventory.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("图标创建成功！")

if __name__ == '__main__':
    try:
        create_icon()
    except Exception as e:
        print(f"创建图标时出错: {str(e)}")