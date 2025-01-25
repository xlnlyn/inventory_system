# inventory_system.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import sys


class InventoryGUI:
    def __init__(self):
        self.inventory = {}
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'inventory_data.json')
        self.load_data()

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("库存管理系统 v1.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # 设置样式
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TEntry', padding=2)

        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 设置网格权重
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_rowconfigure(0, weight=1)

        # 创建左右分栏
        self.create_left_panel(main_frame)
        self.create_right_panel(main_frame)

        # 绑定关闭窗口事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 初始化消息
        self.add_message("欢迎使用库存管理系统！")
        self.add_message("可用命令：view(查看库存), delete 物品名(删除物品)")

    def create_left_panel(self, parent):
        """创建左侧输入面板"""
        left_frame = ttk.LabelFrame(parent, text="物品信息", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # 输入区域
        input_frame = ttk.Frame(left_frame)
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)

        # 创建输入框
        labels = ["物品名称:", "数量:", "价格:"]
        entries = [self.name_entry, self.quantity_entry, self.price_entry] = [
            ttk.Entry(input_frame) for _ in range(3)
        ]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, pady=5, sticky=tk.W)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=(tk.W, tk.E))

        # 按钮区域
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(button_frame, text="添加物品", command=self.add_item).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="更新物品", command=self.update_item).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="清空输入", command=self.clear_entries).grid(row=0, column=2, padx=5)

        # 帮助信息
        help_text = "使用说明：\n\n" + \
                    "1. 添加物品：填写信息后点击'添加物品'\n" + \
                    "2. 更新物品：输入物品名和新的信息\n" + \
                    "3. 查看库存：在命令框输入'view'或'查看'\n" + \
                    "4. 删除物品：在命令框输入'delete 物品名'"

        help_label = ttk.Label(left_frame, text=help_text, wraplength=200, justify=tk.LEFT)
        help_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=20)

    def create_right_panel(self, parent):
        """创建右侧聊天面板"""
        right_frame = ttk.LabelFrame(parent, text="系统消息", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # 配置网格权重
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        # 创建消息显示区域
        self.message_area = tk.Text(right_frame, wrap=tk.WORD, width=50)
        self.message_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.message_area.config(state=tk.DISABLED)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.message_area.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.message_area['yscrollcommand'] = scrollbar.set

        # 命令输入区域
        command_frame = ttk.Frame(right_frame)
        command_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.command_entry = ttk.Entry(command_frame)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.command_entry.bind('<Return>', lambda e: self.handle_command())

        ttk.Button(command_frame, text="发送", command=self.handle_command).pack(side=tk.RIGHT)

    def load_data(self):
        """加载保存的数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.inventory = json.load(f)
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败：{str(e)}")

    def save_data(self):
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存数据失败：{str(e)}")

    def on_closing(self):
        """关闭窗口时保存数据"""
        if messagebox.askokcancel("退出", "确定要退出吗？"):
            self.save_data()
            self.root.destroy()

    # [其他方法保持不变...]
    def add_message(self, message, is_user=False):
        """添加消息到聊天区域"""
        self.message_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = "用户" if is_user else "系统"
        self.message_area.insert(tk.END, f"[{timestamp}] {prefix}: {message}\n")
        self.message_area.see(tk.END)
        self.message_area.config(state=tk.DISABLED)

    def add_item(self):
        """添加物品"""
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name:
            messagebox.showwarning("警告", "请输入物品名称！")
            return

        try:
            quantity = float(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("错误", "数量和价格必须为数字！")
            return

        if quantity <= 0:
            self.add_message(f"错误：数量必须为正数，添加{name}失败。")
            return
        if price <= 0:
            self.add_message(f"错误：价格必须为正数，添加{name}失败。")
            return

        if name in self.inventory:
            self.inventory[name]['quantity'] += quantity
            if self.inventory[name]['price'] != price:
                self.add_message(f"警告：{name}存在不同价格，已保留原价{self.inventory[name]['price']}。")
        else:
            self.inventory[name] = {'quantity': quantity, 'price': price}

        self.add_message(f"成功添加{quantity}个{name}，当前库存：{self.inventory[name]['quantity']}。")
        self.clear_entries()
        self.save_data()  # 自动保存数据

    def update_item(self):
        """更新物品"""
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not name:
            messagebox.showwarning("警告", "请输入物品名称！")
            return

        if name not in self.inventory:
            self.add_message(f"{name}不在库存中。")
            return

        update_made = False

        if quantity:
            try:
                quantity = float(quantity)
                if quantity < 0:
                    self.add_message(f"错误：数量不能为负数，更新{name}失败。")
                    return
                self.inventory[name]['quantity'] = quantity
                update_made = True
            except ValueError:
                messagebox.showerror("错误", "数量必须为数字！")
                return

        if price:
            try:
                price = float(price)
                if price <= 0:
                    self.add_message(f"错误：价格必须为正数，更新{name}失败。")
                    return
                self.inventory[name]['price'] = price
                update_made = True
            except ValueError:
                messagebox.showerror("错误", "价格必须为数字！")
                return

        if update_made:
            self.add_message(f"已更新{name}的信息。")
            self.save_data()  # 自动保存数据
        else:
            self.add_message("未提供更新内容。")

        self.clear_entries()

    def delete_item(self, name):
        """删除物品"""
        if name in self.inventory:
            if messagebox.askyesno("确认", f"确定要删除{name}吗？"):
                del self.inventory[name]
                self.add_message(f"已移除{name}。")
                self.save_data()  # 自动保存数据
        else:
            self.add_message(f"{name}不在库存中。")

    def view_inventory(self):
        """查看库存"""
        self.add_message("当前库存：")
        if not self.inventory:
            self.add_message("库存为空")
            return

        total_value = 0
        for item, details in self.inventory.items():
            value = details['quantity'] * details['price']
            total_value += value
            self.add_message(
                f"物品：{item}\n"
                f"  数量：{details['quantity']:.2f}\n"
                f"  单价：￥{details['price']:.2f}\n"
                f"  总值：￥{value:.2f}"
            )
        self.add_message(f"\n库存总值：￥{total_value:.2f}")

    def handle_command(self):
        """处理命令"""
        command = self.command_entry.get().strip().lower()
        if not command:
            return

        self.add_message(command, True)

        if command in ['view', '查看']:
            self.view_inventory()
        elif command.startswith('delete ') or command.startswith('删除 '):
            name = command.split(' ', 1)[1].strip()
            self.delete_item(name)
        else:
            self.add_message("未知命令。请使用以下命令：\n- view/查看：查看库存\n- delete [物品名]/删除 [物品名]：删除物品")

        self.command_entry.delete(0, tk.END)

    def clear_entries(self):
        """清空输入框"""
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.name_entry.focus()

    def run(self):
        """运行程序"""
        self.root.mainloop()


if __name__ == "__main__":
    app = InventoryGUI()
    app.run()

# 打包指令（创建一个新文件 build_exe.bat）：
"""
@echo off
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon=inventory.ico --name="库存管理系统" --add-data "inventory.ico;." inventory_system.py
pause
"""

# 创建图标的Python代码（创建一个新文件 create_icon.py）：
"""
from PIL import Image, ImageDraw

def create_icon():
    # 创建一个 256x256 的图像
    size = 256
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # 绘制一个简单的箱子图标
    margin = size // 8
    box_color = (52, 152, 219)  # 蓝色

    # 主体
    draw.rectangle([margin, margin * 2, size - margin, size - margin], 
                  fill=box_color)

    # 盖子
    draw.polygon([
        (margin, margin * 2),  # 左下
        (margin // 2, margin),  # 左上
        (size - margin // 2, margin),  # 右上
        (size - margin, margin * 2)  # 右下
    ], fill=box_color)

    # 保存图标
    image.save('inventory.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_icon()
"""
