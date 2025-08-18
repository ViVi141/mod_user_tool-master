"""
模组用户工具 - 美化版主程序
使用增强版UI组件，提供更美观的界面
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import json
import threading
import os

from mod_manager import ModManager
from ui_components_enhanced import (
    SectionFrame, ModernButton, EnhancedFileSelector, 
    EnhancedTextArea, EnhancedProgressBar, EnhancedLogDisplay,
    ModernToolTip
)
from config import *


class EnhancedModUserTool:
    """美化版模组用户工具主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.mod_manager = ModManager()
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 设置窗口属性
        self.root.title(WINDOW_TITLE)
        self.root.geometry("900x900")
        self.root.minsize(800, 800)
        
        # 设置窗口背景色
        self.root.configure(bg="#f8f9fa")
        
        # 配置网格权重
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(10, weight=1)
        
        # 创建UI组件
        self.create_header()
        self.create_json_section()
        self.create_folder_section()
        self.create_progress_section()
        self.create_button_section()
        self.create_log_section()
        
    def create_header(self):
        """创建页面头部"""
        header_frame = tk.Frame(self.root, bg="#ffffff", height=80, relief="flat", bd=1)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)
        
        # 标题
        title_label = tk.Label(
            header_frame,
            text="模组用户工具",
            font=("Microsoft YaHei", 20, "bold"),
            fg="#007bff",
            bg="#ffffff"
        )
        title_label.pack(side="left", padx=30, pady=20)
        
        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="Arma Reforger 服务器模组管理工具",
            font=("Microsoft YaHei", 12, "normal"),
            fg="#6c757d",
            bg="#ffffff"
        )
        subtitle_label.pack(side="left", padx=(20, 0), pady=20)
        
        # 作者信息
        author_label = tk.Label(
            header_frame,
            text="作者: ViVi141 | QQ: 747384120",
            font=("Microsoft YaHei", 10, "normal"),
            fg="#6c757d",
            bg="#ffffff"
        )
        author_label.pack(side="right", padx=30, pady=20)
        
    def create_json_section(self):
        """创建JSON相关UI组件"""
        # JSON文件选择
        self.json_file_selector = EnhancedFileSelector(
            self.root, "选择服务器用JSON文件:", "浏览", self.select_json_file
        )
        self.json_file_selector.grid(row=1, column=0, columnspan=3)
        
        # JSON内容文本框
        self.json_text_area = EnhancedTextArea(
            self.root, 
            "粘贴游戏中JSON内容:", 
            width=70, 
            height=8,
            placeholder="在此粘贴JSON内容或选择文件..."
        )
        self.json_text_area.grid(row=2, column=0, columnspan=3)
        
        # 加载JSON按钮
        self.load_json_button = ModernButton(
            self.root,
            "加载JSON内容",
            self.load_json_from_text,
            style="primary",
            width=15
        )
        self.load_json_button.grid(row=2, column=3, padx=15, pady=15)
        
    def create_folder_section(self):
        """创建文件夹选择UI组件"""
        # 源文件夹选择
        self.source_folder_selector = EnhancedFileSelector(
            self.root, "选择源文件夹:", "浏览", self.select_source_folder
        )
        self.source_folder_selector.grid(row=3, column=0, columnspan=3)
        
        # 目标文件夹选择
        self.target_folder_selector = EnhancedFileSelector(
            self.root, "选择目标文件夹:", "浏览", self.select_target_folder
        )
        self.target_folder_selector.grid(row=4, column=0, columnspan=3)
        
    def create_progress_section(self):
        """创建进度条UI组件"""
        self.progress_bar = EnhancedProgressBar(self.root)
        self.progress_bar.grid(row=5, column=0, columnspan=3)
        
    def create_button_section(self):
        """创建操作按钮UI组件"""
        # 按钮容器
        button_frame = tk.Frame(self.root, bg="#f8f9fa")
        button_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=15, pady=20)
        
        # 第一行按钮
        row1_frame = tk.Frame(button_frame, bg="#f8f9fa")
        row1_frame.pack(fill="x", pady=(0, 10))
        
        # 复制模组并单独压缩按钮
        self.copy_button = ModernButton(
            row1_frame,
            "复制模组并单独压缩每个模组并导出模组信息文件",
            self.run_copy_mods,
            style="primary",
            width=45
        )
        self.copy_button.pack(side="left", padx=(0, 10))
        ModernToolTip(self.copy_button, "复制所有需要更新的模组文件夹到目标文件夹，并压缩每个模组文件夹，生成模组信息文件。")
        
        # 仅复制模组按钮
        self.only_copy_button = ModernButton(
            row1_frame,
            "仅复制模组",
            self.run_only_copy_mods,
            style="success",
            width=15
        )
        self.only_copy_button.pack(side="left", padx=(0, 10))
        ModernToolTip(self.only_copy_button, "仅复制所有需要更新的模组文件夹到目标文件夹，不进行压缩和删除操作。")
        
        # 第二行按钮
        row2_frame = tk.Frame(button_frame, bg="#f8f9fa")
        row2_frame.pack(fill="x", pady=(0, 10))
        
        # 智能更新按钮
        self.smart_update_button = ModernButton(
            row2_frame,
            "智能更新模组（跳过重复）",
            self.run_smart_update_mods,
            style="info",
            width=25
        )
        self.smart_update_button.pack(side="left", padx=(0, 10))
        ModernToolTip(self.smart_update_button, "智能更新模组：只有版本号不同和新的模组列表中有但目标文件夹中没有的模组才会被更新，并单独创建更新文件夹存放。")
        
        # 仅导出JSON按钮
        self.only_export_json_button = ModernButton(
            row2_frame,
            "仅导出模组信息文件",
            self.run_only_export_json,
            style="warning",
            width=20
        )
        self.only_export_json_button.pack(side="left", padx=(0, 10))
        ModernToolTip(self.only_export_json_button, "仅生成模组信息文件，不进行复制和压缩操作。")
        
        # 第三行按钮
        row3_frame = tk.Frame(button_frame, bg="#f8f9fa")
        row3_frame.pack(fill="x")
        
        # 处理多个服务器按钮
        self.process_multiple_button = ModernButton(
            row3_frame,
            "处理多个服务器 JSON 文件",
            self.process_multiple_json_files,
            style="secondary",
            width=25
        )
        self.process_multiple_button.pack(side="left")
        ModernToolTip(self.process_multiple_button, "选择多个服务器 JSON 文件，输出每个服务器的模组清单和所有包含的模组。")
        
    def create_log_section(self):
        """创建日志显示UI组件"""
        self.log_display = EnhancedLogDisplay(self.root, width=80, height=15)
        self.log_display.grid(row=7, column=0, columnspan=3)
        
    def select_json_file(self):
        """选择JSON文件"""
        file_path = filedialog.askopenfilename(filetypes=SUPPORTED_JSON_TYPES)
        if not file_path:
            messagebox.showwarning("警告", "未选择文件")
            self.log_display.log_message("警告: 未选择文件", "warning")
            return

        try:
            with open(file_path, 'r', encoding=DEFAULT_ENCODING) as file:
                config = json.load(file)
                self.json_text_area.set_content(json.dumps(config, ensure_ascii=False, indent=4))
        except Exception as e:
            messagebox.showerror("错误", f"解析JSON文件时出错: {e}")
            self.log_display.log_message(f"错误: 解析JSON文件时出错: {e}", "error")
            return

        # 禁用文本框加载按钮
        self.load_json_button.configure(state=tk.DISABLED)
        self.log_display.log_message(f"成功: 加载JSON文件: {file_path}", "success")
        
    def load_json_from_text(self):
        """从文本框加载JSON内容"""
        json_content = self.json_text_area.get_content()
        if not json_content:
            messagebox.showwarning("警告", "JSON内容为空")
            self.log_display.log_message("警告: JSON内容为空", "warning")
            return

        # 增加JSON格式以符合预期，并正确添加换行符和缩进
        json_content = f'{{\n    "game": {{\n        "mods": [\n            {json_content}\n        ]\n    }}\n}}'

        try:
            config = json.loads(json_content)
            self.json_text_area.set_content(json.dumps(config, ensure_ascii=False, indent=4))
        except Exception as e:
            messagebox.showerror("错误", f"解析JSON内容时出错: {e}")
            self.log_display.log_message(f"错误: 解析JSON内容时出错: {e}", "error")
            return

        # 禁用文件选择加载按钮
        self.json_file_selector.button.configure(state=tk.DISABLED)
        self.log_display.log_message("成功: 从文本框加载JSON内容", "success")
        
    def select_source_folder(self):
        """选择源文件夹"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.source_folder_selector.set_path(folder_path)
            
    def select_target_folder(self):
        """选择目标文件夹"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.target_folder_selector.set_path(folder_path)
            
    def run_copy_mods(self):
        """运行复制模组操作"""
        thread = threading.Thread(target=self.copy_mods)
        thread.start()
        
    def run_only_copy_mods(self):
        """运行仅复制模组操作"""
        thread = threading.Thread(target=self.only_copy_mods)
        thread.start()
        
    def run_smart_update_mods(self):
        """运行智能更新模组操作"""
        thread = threading.Thread(target=self.smart_update_mods)
        thread.start()
        
    def run_only_export_json(self):
        """运行仅导出JSON操作"""
        thread = threading.Thread(target=self.only_export_json)
        thread.start()
        
    def copy_mods(self):
        """复制模组的主要逻辑"""
        self.log_display.clear()
        json_content = self.json_text_area.get_content()
        source_folder = self.source_folder_selector.get_path()
        target_folder = self.target_folder_selector.get_path()

        if not json_content:
            messagebox.showerror("错误", ERROR_MESSAGES["json_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['json_empty']}", "error")
            return

        if not source_folder:
            messagebox.showerror("错误", ERROR_MESSAGES["source_folder_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['source_folder_empty']}", "error")
            return

        if not target_folder:
            messagebox.showerror("错误", ERROR_MESSAGES["target_folder_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['target_folder_empty']}", "error")
            return

        try:
            config = json.loads(json_content)
            if 'game' not in config or 'mods' not in config['game']:
                messagebox.showerror("错误", ERROR_MESSAGES["json_format_error"])
                self.log_display.log_message(f"错误: {ERROR_MESSAGES['json_format_error']}", "error")
                return

            mods = config['game']['mods']
            total_mods = len(mods)
            processed_mods = 0
            new_mods = 0
            updated_mods = 0
            skipped_mods = 0

            self.log_display.log_message(f"开始处理 {total_mods} 个模组...", "info")
            
            for mod in mods:
                mod_id = mod.get('modId', '')
                if not mod_id:
                    continue
                    
                for folder_name in os.listdir(source_folder):
                    if mod_id in folder_name:
                        mod_source_path = os.path.join(source_folder, folder_name)
                        if not os.path.isdir(mod_source_path):
                            continue

                        # 解析版本，生成标准化目录名：源文件夹名_版本
                        parsed = self.mod_manager.parse_mod_info(mod_source_path, mod_id)
                        standardized_name = self.mod_manager.generate_mod_folder_name(
                            os.path.basename(mod_source_path), parsed.get('version', '未知')
                        )
                        standardized_target_path = os.path.join(target_folder, standardized_name)

                        # 若目标已有包含该ID的旧命名目录且标准化目录不存在，先尝试重命名为标准化目录
                        existing_path = self.mod_manager.find_existing_mod_path(target_folder, mod_id)
                        if existing_path and existing_path != standardized_target_path and not os.path.exists(standardized_target_path):
                            try:
                                os.rename(existing_path, standardized_target_path)
                                existing_path = standardized_target_path
                            except Exception:
                                pass

                        mod_target_path = standardized_target_path if os.path.exists(standardized_target_path) else (existing_path or standardized_target_path)

                        # 检查是否需要更新
                        needs_update, reason, source_version, target_version = self.mod_manager.check_mod_needs_update(
                            mod_source_path, mod_target_path, mod_id
                        )

                        if needs_update:
                            if os.path.exists(mod_target_path):
                                self.log_display.log_message(f"更新模组: {standardized_name} - {reason}", "info")
                                updated_mods += 1
                            else:
                                self.log_display.log_message(f"新增模组: {standardized_name}", "info")
                                new_mods += 1

                            # 复制到标准化目录
                            if self.mod_manager.copy_mod_folder(mod_source_path, standardized_target_path):
                                self.log_display.log_message(f"成功复制: {standardized_name}", "success")
                            else:
                                self.log_display.log_message(f"复制失败: {standardized_name}", "error")
                        else:
                            self.log_display.log_message(f"跳过模组: {standardized_name} - {reason}", "info")
                            skipped_mods += 1
                        break
                
                processed_mods += 1
                progress = (processed_mods / total_mods) * 100
                self.progress_bar.update_progress(progress)

            # 生成模组信息JSON文件
            if new_mods > 0 or updated_mods > 0:
                mod_info = {}
                for mod in mods:
                    mod_id = mod.get('modId', '')
                    if mod_id:
                        for folder_name in os.listdir(source_folder):
                            if mod_id in folder_name:
                                mod_source_path = os.path.join(source_folder, folder_name)
                                if os.path.isdir(mod_source_path):
                                    mod_info[mod_id] = self.mod_manager.parse_mod_info(mod_source_path, mod_id)
                                break

                mod_info_path = self.mod_manager.save_mod_info_json(mod_info, target_folder)
                if mod_info_path:
                    self.log_display.log_message(f"成功生成模组信息文件: {mod_info_path}", "success")

            messagebox.showinfo("成功", SUCCESS_MESSAGES["mods_copied"].format(new_mods, updated_mods, skipped_mods))
            self.log_display.log_message(SUCCESS_MESSAGES["mods_copied"].format(new_mods, updated_mods, skipped_mods), "success")

        except Exception as e:
            messagebox.showerror("错误", f"操作过程中出错: {e}")
            self.log_display.log_message(f"错误: {e}", "error")
        finally:
            self.progress_bar.reset()
            
    def only_copy_mods(self):
        """仅复制模组"""
        self.copy_mods()  # 复用复制模组的逻辑
        
    def smart_update_mods(self):
        """智能更新模组"""
        self.log_display.clear()
        json_content = self.json_text_area.get_content()
        source_folder = self.source_folder_selector.get_path()
        target_folder = self.target_folder_selector.get_path()

        if not json_content:
            messagebox.showerror("错误", ERROR_MESSAGES["json_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['json_empty']}", "error")
            return

        if not source_folder:
            messagebox.showerror("错误", ERROR_MESSAGES["source_folder_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['source_folder_empty']}", "error")
            return

        if not target_folder:
            messagebox.showerror("错误", ERROR_MESSAGES["target_folder_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['target_folder_empty']}", "error")
            return

        try:
            # 禁用按钮
            self.smart_update_button.configure(state=tk.DISABLED)
            self.progress_bar.update_progress(10)
            
            self.log_display.log_message("开始智能更新模组...", "info")
            self.log_display.log_message("只有版本号不同和新的模组列表中有但目标文件夹中没有的模组才会被更新", "info")
            
            # 调用智能更新方法
            result = self.mod_manager.smart_update_mods(json_content, source_folder, target_folder)
            
            self.progress_bar.update_progress(100)
            
            # 显示结果
            update_folder = result.get('update_folder', '')
            if update_folder and os.path.exists(update_folder):
                self.log_display.log_message(f"智能更新完成！", "success")
                self.log_display.log_message(f"更新文件夹: {update_folder}", "success")
                self.log_display.log_message(f"总模组数: {result['total_mods']}", "info")
                self.log_display.log_message(f"新增模组: {result['new_mods']}", "info")
                self.log_display.log_message(f"更新模组: {result['updated_mods']}", "info")
                self.log_display.log_message(f"跳过模组: {result['skipped_mods']}", "info")
                
                messagebox.showinfo("成功", f"智能更新完成！\n\n新增: {result['new_mods']}\n更新: {result['updated_mods']}\n跳过: {result['skipped_mods']}\n\n更新文件夹: {update_folder}")
            else:
                self.log_display.log_message("智能更新完成，但没有需要更新的模组", "info")
                messagebox.showinfo("信息", "所有模组都是最新版本，无需更新")
                
        except Exception as e:
            messagebox.showerror("错误", f"智能更新过程中出错: {e}")
            self.log_display.log_message(f"错误: {e}", "error")
        finally:
            # 恢复按钮状态
            self.smart_update_button.configure(state=tk.NORMAL)
            self.progress_bar.reset()
        
    def only_export_json(self):
        """仅导出模组信息JSON"""
        self.log_display.clear()
        json_content = self.json_text_area.get_content()
        source_folder = self.source_folder_selector.get_path()

        if not json_content:
            messagebox.showerror("错误", ERROR_MESSAGES["json_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['json_empty']}", "error")
            return

        if not source_folder:
            messagebox.showerror("错误", ERROR_MESSAGES["source_folder_empty"])
            self.log_display.log_message(f"错误: {ERROR_MESSAGES['source_folder_empty']}", "error")
            return

        try:
            config = json.loads(json_content)
            if 'game' not in config or 'mods' not in config['game']:
                messagebox.showerror("错误", ERROR_MESSAGES["json_format_error"])
                self.log_display.log_message(f"错误: {ERROR_MESSAGES['json_format_error']}", "error")
                return

            mods = config['game']['mods']
            mod_info = {}
            
            for mod in mods:
                mod_id = mod.get('modId', '')
                if not mod_id:
                    continue
                    
                for folder_name in os.listdir(source_folder):
                    if mod_id in folder_name:
                        mod_source_path = os.path.join(source_folder, folder_name)
                        if os.path.isdir(mod_source_path):
                            mod_info[mod_id] = self.mod_manager.parse_mod_info(mod_source_path, mod_id)
                            self.log_display.log_message(f"记录模组信息: {mod_info[mod_id]['name']} ({mod_id}) - {mod_info[mod_id]['version']}", "info")
                        break

            # 生成模组信息JSON文件
            if mod_info:
                mod_info_path = self.mod_manager.save_mod_info_json(mod_info, source_folder)
                if mod_info_path:
                    self.log_display.log_message(f"成功生成模组信息文件: {mod_info_path}", "success")
                    messagebox.showinfo("成功", "模组信息文件生成完成！")
                else:
                    messagebox.showerror("错误", "生成模组信息文件失败")
            else:
                messagebox.showwarning("警告", "未找到任何模组信息")

        except Exception as e:
            messagebox.showerror("错误", f"操作过程中出错: {e}")
            self.log_display.log_message(f"错误: {e}", "error")
            
    def process_multiple_json_files(self):
        """处理多个服务器JSON文件"""
        file_paths = filedialog.askopenfilenames(filetypes=SUPPORTED_JSON_TYPES)
        if not file_paths:
            messagebox.showwarning("警告", "未选择文件")
            return

        self.log_display.clear()
        self.log_display.log_message(f"开始处理 {len(file_paths)} 个JSON文件...", "info")

        try:
            for file_path in file_paths:
                self.log_display.log_message(f"\n处理文件: {os.path.basename(file_path)}", "info")
                
                with open(file_path, 'r', encoding=DEFAULT_ENCODING) as file:
                    config = json.load(file)
                
                if 'game' in config and 'mods' in config['game']:
                    mods = config['game']['mods']
                    self.log_display.log_message(f"  模组数量: {len(mods)}", "info")
                    
                    for mod in mods:
                        mod_id = mod.get('modId', '')
                        if mod_id:
                            self.log_display.log_message(f"  - {mod_id}", "info")
                else:
                    self.log_display.log_message("  格式不正确，跳过", "warning")

            messagebox.showinfo("成功", INFO_MESSAGES["processing_complete"])
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中出错: {e}")
            self.log_display.log_message(f"错误: {e}", "error")
            
    def run(self):
        """运行应用程序"""
        self.root.mainloop()


if __name__ == "__main__":
    app = EnhancedModUserTool()
    app.run()
