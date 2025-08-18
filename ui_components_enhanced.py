"""
增强版UI组件模块
包含更美观的界面元素和样式
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


class ModernFrame:
    """现代化框架组件"""
    
    def __init__(self, parent, title="", bg_color="#f8f9fa", border_color="#dee2e6"):
        self.frame = tk.Frame(parent, bg=bg_color, relief="flat", bd=1)
        self.title = title
        self.bg_color = bg_color
        self.border_color = border_color
        
    def pack(self, **kwargs):
        """包装frame的pack方法"""
        return self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """包装frame的grid方法"""
        return self.frame.grid(**kwargs)
        
    def configure(self, **kwargs):
        """包装frame的configure方法"""
        return self.frame.configure(**kwargs)


class SectionFrame(ModernFrame):
    """带标题的分区框架"""
    
    def __init__(self, parent, title, bg_color="#ffffff", border_color="#e9ecef"):
        super().__init__(parent, title, bg_color, border_color)
        self.create_title()
        
    def create_title(self):
        """创建标题"""
        if self.title:
            title_frame = tk.Frame(self.frame, bg=self.bg_color, height=30)
            title_frame.pack(fill="x", padx=15, pady=(10, 5))
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(
                title_frame, 
                text=self.title, 
                font=("Microsoft YaHei", 11, "bold"),
                fg="#495057",
                bg=self.bg_color
            )
            title_label.pack(side="left")
            
            # 添加分隔线
            separator = tk.Frame(title_frame, height=2, bg=self.border_color)
            separator.pack(fill="x", side="bottom", pady=(5, 0))


class ModernButton:
    """现代化按钮组件"""
    
    def __init__(self, parent, text, command, style="primary", width=None, height=None):
        self.parent = parent
        self.text = text
        self.command = command
        self.style = style
        self.width = width
        self.height = height
        
        self.button = tk.Button(
            parent, 
            text=text, 
            command=command,
            font=("Microsoft YaHei", 9, "normal"),
            relief="flat",
            bd=0,
            cursor="hand2",
            width=width,
            height=height
        )
        
        self.apply_style()
        self.bind_events()
        
    def apply_style(self):
        """应用样式"""
        if self.style == "primary":
            self.button.configure(
                bg="#007bff",
                fg="white",
                activebackground="#0056b3",
                activeforeground="white"
            )
        elif self.style == "success":
            self.button.configure(
                bg="#28a745",
                fg="white",
                activebackground="#1e7e34",
                activeforeground="white"
            )
        elif self.style == "warning":
            self.button.configure(
                bg="#ffc107",
                fg="#212529",
                activebackground="#e0a800",
                activeforeground="#212529"
            )
        elif self.style == "info":
            self.button.configure(
                bg="#17a2b8",
                fg="white",
                activebackground="#117a8b",
                activeforeground="white"
            )
        elif self.style == "secondary":
            self.button.configure(
                bg="#6c757d",
                fg="white",
                activebackground="#545b62",
                activeforeground="white"
            )
            
    def bind_events(self):
        """绑定事件"""
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)
        
    def on_enter(self, event):
        """鼠标进入事件"""
        if self.style == "primary":
            self.button.configure(bg="#0056b3")
        elif self.style == "success":
            self.button.configure(bg="#1e7e34")
        elif self.style == "warning":
            self.button.configure(bg="#e0a800")
        elif self.style == "info":
            self.button.configure(bg="#117a8b")
        elif self.style == "secondary":
            self.button.configure(bg="#545b62")
            
    def on_leave(self, event):
        """鼠标离开事件"""
        self.apply_style()
        
    def grid(self, **kwargs):
        """包装grid方法"""
        return self.button.grid(**kwargs)
        
    def pack(self, **kwargs):
        """包装pack方法"""
        return self.button.pack(**kwargs)
        
    def configure(self, **kwargs):
        """包装configure方法"""
        return self.button.configure(**kwargs)
        
    def bind(self, event, callback):
        """包装bind方法"""
        return self.button.bind(event, callback)


class EnhancedFileSelector:
    """增强版文件选择器"""
    
    def __init__(self, parent, label_text, button_text, command, entry_width=50):
        self.parent = parent
        self.label_text = label_text
        self.button_text = button_text
        self.command = command
        self.entry_width = entry_width
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建组件"""
        # 标签
        self.label = tk.Label(
            self.parent,
            text=self.label_text,
            font=("Microsoft YaHei", 9, "normal"),
            fg="#495057",
            bg=self.parent.cget("bg") if hasattr(self.parent, 'cget') else "#ffffff"
        )
        
        # 输入框
        self.entry = tk.Entry(
            self.parent,
            width=self.entry_width,
            font=("Microsoft YaHei", 9, "normal"),
            relief="solid",
            bd=1,
            bg="white",
            fg="#495057"
        )
        
        # 按钮
        self.button = ModernButton(
            self.parent,
            self.button_text,
            self.command,
            style="secondary",
            width=8
        )
        
    def grid(self, row, column, **kwargs):
        """网格布局"""
        self.label.grid(row=row, column=column, padx=15, pady=8, sticky="w")
        self.entry.grid(row=row, column=column+1, padx=(0, 10), pady=8, sticky="ew")
        self.button.grid(row=row, column=column+2, padx=0, pady=8)
        
    def get_path(self):
        """获取路径"""
        return self.entry.get()
        
    def set_path(self, path):
        """设置路径"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, path)


class EnhancedTextArea:
    """增强版文本区域"""
    
    def __init__(self, parent, label_text, width=65, height=10, placeholder=""):
        self.parent = parent
        self.label_text = label_text
        self.width = width
        self.height = height
        self.placeholder = placeholder
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建组件"""
        # 标签
        self.label = tk.Label(
            self.parent,
            text=self.label_text,
            font=("Microsoft YaHei", 9, "normal"),
            fg="#495057",
            bg=self.parent.cget("bg") if hasattr(self.parent, 'cget') else "#ffffff"
        )
        
        # 文本框架
        self.text_frame = tk.Frame(self.parent, bg="white", relief="solid", bd=1)
        
        # 文本框
        self.text = tk.Text(
            self.text_frame,
            width=self.width,
            height=self.height,
            wrap=tk.WORD,
            font=("Consolas", 9, "normal"),
            relief="flat",
            bd=0,
            bg="white",
            fg="#495057",
            insertbackground="#007bff"
        )
        
        # 滚动条
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        
        # 布局
        self.text.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        self.scrollbar.pack(side="right", fill="y")
        
        # 绑定事件
        self.text.bind("<FocusIn>", self.on_focus_in)
        self.text.bind("<FocusOut>", self.on_focus_out)
        
        # 设置占位符
        if self.placeholder:
            self.text.insert("1.0", self.placeholder)
            self.text.config(fg="#6c757d")
            
    def on_focus_in(self, event):
        """获得焦点事件"""
        if self.text.get("1.0", "end-1c") == self.placeholder:
            self.text.delete("1.0", tk.END)
            self.text.config(fg="#495057")
            
    def on_focus_out(self, event):
        """失去焦点事件"""
        if not self.text.get("1.0", "end-1c").strip():
            self.text.insert("1.0", self.placeholder)
            self.text.config(fg="#6c757d")
            
    def grid(self, row, column, **kwargs):
        """网格布局"""
        self.label.grid(row=row, column=column, padx=15, pady=(15, 5), sticky="w")
        self.text_frame.grid(row=row, column=column+1, columnspan=2, padx=15, pady=(15, 5), sticky="ew")
        
    def get_content(self):
        """获取内容"""
        content = self.text.get("1.0", "end-1c")
        if content == self.placeholder:
            return ""
        return content
        
    def set_content(self, content):
        """设置内容"""
        self.text.delete("1.0", tk.END)
        if content:
            self.text.insert("1.0", content)
            self.text.config(fg="#495057")
        else:
            self.text.insert("1.0", self.placeholder)
            self.text.config(fg="#6c757d")
            
    def clear(self):
        """清空内容"""
        self.text.delete("1.0", tk.END)
        if self.placeholder:
            self.text.insert("1.0", self.placeholder)
            self.text.config(fg="#6c757d")


class EnhancedProgressBar:
    """增强版进度条"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
        
    def create_widgets(self):
        """创建组件"""
        # 标签
        self.label = tk.Label(
            self.parent,
            text="进度:",
            font=("Microsoft YaHei", 9, "normal"),
            fg="#495057",
            bg=self.parent.cget("bg") if hasattr(self.parent, 'cget') else "#ffffff"
        )
        
        # 进度条框架
        self.progress_frame = tk.Frame(self.parent, bg="white", relief="solid", bd=1)
        
        # 进度条
        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="Custom.Horizontal.TProgressbar"
        )
        
        # 百分比标签
        self.percentage_label = tk.Label(
            self.progress_frame,
            text="0%",
            font=("Microsoft YaHei", 8, "normal"),
            fg="#6c757d",
            bg="white"
        )
        
        # 布局
        self.progress.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        self.percentage_label.pack(side="right", padx=(0, 10), pady=10)
        
        # 自定义样式
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#e9ecef",
            background="#007bff",
            bordercolor="#dee2e6",
            lightcolor="#007bff",
            darkcolor="#007bff"
        )
        
    def grid(self, row, column, **kwargs):
        """网格布局"""
        self.label.grid(row=row, column=column, padx=15, pady=10, sticky="w")
        self.progress_frame.grid(row=row, column=column+1, columnspan=2, padx=15, pady=10, sticky="ew")
        
    def update_progress(self, value):
        """更新进度"""
        self.progress['value'] = value
        self.percentage_label.config(text=f"{int(value)}%")
        self.progress.update_idletasks()
        
    def reset(self):
        """重置进度"""
        self.progress['value'] = 0
        self.percentage_label.config(text="0%")
        self.progress.update_idletasks()


class EnhancedLogDisplay:
    """增强版日志显示"""
    
    def __init__(self, parent, width=65, height=12):
        self.parent = parent
        self.width = width
        self.height = height
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建组件"""
        # 标签
        self.label = tk.Label(
            self.parent,
            text="操作日志:",
            font=("Microsoft YaHei", 9, "normal"),
            fg="#495057",
            bg=self.parent.cget("bg") if hasattr(self.parent, 'cget') else "#ffffff"
        )
        
        # 日志框架
        self.log_frame = tk.Frame(self.parent, bg="white", relief="solid", bd=1)
        
        # 日志文本框
        self.text = tk.Text(
            self.log_frame,
            width=self.width,
            height=self.height,
            wrap=tk.WORD,
            font=("Consolas", 8, "normal"),
            relief="flat",
            bd=0,
            bg="#f8f9fa",
            fg="#495057",
            insertbackground="#007bff"
        )
        
        # 滚动条
        self.scrollbar = tk.Scrollbar(self.log_frame, command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        
        # 布局
        self.text.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        self.scrollbar.pack(side="right", fill="y")
        
    def grid(self, row, column, **kwargs):
        """网格布局"""
        self.label.grid(row=row, column=column, padx=15, pady=(15, 5), sticky="w")
        self.log_frame.grid(row=row, column=column+1, columnspan=2, padx=15, pady=(15, 5), sticky="ew")
        
    def log_message(self, message, level="info"):
        """添加日志消息"""
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # 根据级别设置颜色
        if level == "success":
            color = "#28a745"
        elif level == "error":
            color = "#dc3545"
        elif level == "warning":
            color = "#ffc107"
        else:
            color = "#17a2b8"
            
        # 插入消息
        self.text.insert(tk.END, f"[{timestamp}] ")
        self.text.insert(tk.END, message + "\n")
        
        # 设置颜色
        start = f"{self.text.index('end-2c').split('.')[0]}.0"
        end = f"{self.text.index('end-2c').split('.')[0]}.{len(timestamp) + 2}"
        self.text.tag_add("timestamp", start, end)
        self.text.tag_config("timestamp", foreground="#6c757d")
        
        # 滚动到底部
        self.text.see(tk.END)
        self.text.update_idletasks()
        
    def clear(self):
        """清空日志"""
        self.text.delete("1.0", tk.END)


class ModernToolTip:
    """现代化工具提示"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        
        self.widget.bind("<Enter>", self.showtip)
        self.widget.bind("<Leave>", self.hidetip)
        
    def showtip(self, event=None):
        """显示提示"""
        if self.tipwindow:
            return
            
        # 获取实际的widget对象
        actual_widget = self.widget.button if hasattr(self.widget, 'button') else self.widget
        
        x, y, cx, cy = actual_widget.bbox("insert")
        x = x + actual_widget.winfo_rootx() + 25
        y = y + cy + actual_widget.winfo_rooty() + 25
        
        self.tipwindow = tw = tk.Toplevel(actual_widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # 设置样式
        tw.configure(bg="#343a40", relief="flat", bd=0)
        
        label = tk.Label(
            tw, 
            text=self.text, 
            justify="left",
            background="#343a40", 
            foreground="white",
            relief="flat", 
            borderwidth=0,
            font=("Microsoft YaHei", 8, "normal"),
            wraplength=200
        )
        label.pack(padx=8, pady=6)
        
    def hidetip(self, event=None):
        """隐藏提示"""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
