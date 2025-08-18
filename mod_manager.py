"""
模组管理核心功能模块
包含模组检查、复制、更新等核心功能
"""

import json
import shutil
import os
from typing import Tuple, Dict, List, Any


class ModManager:
    """模组管理器类"""
    
    def __init__(self):
        self.mod_info = {}
    
    def sanitize_folder_name(self, name: str) -> str:
        """将名称清理为合法的 Windows 文件夹名。"""
        import re
        cleaned = re.sub(r'[<>:"/\\|?*]', '_', name)
        cleaned = cleaned.strip().rstrip('.')
        return cleaned

    def generate_mod_folder_name(self, source_folder_name: str, version: str) -> str:
        """生成标准化的模组文件夹名: {源文件夹名称}_{version}。"""
        safe_name = self.sanitize_folder_name(source_folder_name)
        safe_version = self.sanitize_folder_name(version or '未知')
        return f"{safe_name}_{safe_version}"

    def resolve_target_mod_path(self, target_folder: str, mod_id: str, standardized_name: str) -> str:
        """在目标目录中查找已存在的包含该 mod_id 的文件夹；若不存在则返回标准化路径。"""
        for existing_name in os.listdir(target_folder):
            existing_path = os.path.join(target_folder, existing_name)
            if os.path.isdir(existing_path) and mod_id in existing_name:
                return existing_path
        return os.path.join(target_folder, standardized_name)

    def find_existing_mod_path(self, target_folder: str, mod_id: str) -> str:
        """仅查找包含 mod_id 的已存在目录，找不到返回空字符串。"""
        for existing_name in os.listdir(target_folder):
            existing_path = os.path.join(target_folder, existing_name)
            if os.path.isdir(existing_path) and mod_id in existing_name:
                return existing_path
        return ""

    def get_folder_size(self, folder_path: str) -> int:
        """获取文件夹大小（以字节为单位）"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size
    
    def check_mod_needs_update(self, source_path: str, target_path: str, mod_id: str) -> Tuple[bool, str, str, str]:
        """
        检查模组是否需要更新
        返回: (是否需要更新, 原因, 源版本, 目标版本)
        """
        try:
            # 检查目标文件夹是否存在
            if not os.path.exists(target_path):
                return True, "目标模组不存在", "未知", "不存在"
            
            # 检查源模组的ServerData.json
            source_server_data_path = os.path.join(source_path, 'ServerData.json')
            if not os.path.isfile(source_server_data_path):
                return True, "源模组缺少ServerData.json", "未知", "未知"
            
            # 检查目标模组的ServerData.json
            target_server_data_path = os.path.join(target_path, 'ServerData.json')
            if not os.path.isfile(target_server_data_path):
                return True, "目标模组缺少ServerData.json", "未知", "未知"
            
            # 读取版本信息
            with open(source_server_data_path, 'r', encoding='utf-8-sig') as f:
                source_data = json.load(f)
            with open(target_server_data_path, 'r', encoding='utf-8-sig') as f:
                target_data = json.load(f)
            
            source_version = source_data.get('revision', {}).get('version', '')
            target_version = target_data.get('revision', {}).get('version', '')
            
            # 如果版本不同，需要更新
            if source_version != target_version:
                return True, f"版本不同 (源: {source_version}, 目标: {target_version})", source_version, target_version
            
            # 检查文件修改时间
            source_mtime = os.path.getmtime(source_path)
            target_mtime = os.path.getmtime(target_path)
            
            # 如果源文件更新，需要更新
            if source_mtime > target_mtime:
                return True, f"源文件更新 (源: {source_mtime}, 目标: {target_mtime})", source_version, target_version
            
            return False, "模组已是最新版本", source_version, target_version
            
        except Exception as e:
            return True, f"检查过程中出错: {e}", "未知", "未知"
    
    def smart_update_mods(self, json_content: str, source_folder: str, target_folder: str) -> Dict[str, Any]:
        """
        智能更新模组
        只有版本号不同和新的模组列表中有但目标文件夹中没有的模组才更新
        单独新建一个文件夹来存放需要更新与添加的模组
        """
        try:
            config = json.loads(json_content)
        except Exception as e:
            raise ValueError(f"解析JSON内容时出错: {e}")
        
        if 'game' not in config or 'mods' not in config['game']:
            raise ValueError("JSON文件格式不正确")
        
        mods = config['game']['mods']
        
        # 创建更新文件夹
        update_folder = os.path.join(target_folder, "mods_update")
        if os.path.exists(update_folder):
            shutil.rmtree(update_folder)
        os.makedirs(update_folder, exist_ok=True)
        
        # 统计信息
        total_mods_count = len(mods)
        updated_mods_count = 0
        skipped_mods_count = 0
        new_mods_count = 0
        mod_info = {}
        
        for mod in mods:
            mod_id = mod.get('modId', '')
            if not mod_id:
                continue
                
            # 在源文件夹中查找对应的模组文件夹
            mod_source_path = None
            for folder_name in os.listdir(source_folder):
                if mod_id in folder_name:
                    mod_source_path = os.path.join(source_folder, folder_name)
                    if os.path.isdir(mod_source_path):
                        break
            
            if not mod_source_path or not os.path.isdir(mod_source_path):
                continue
            
            # 解析版本，确定标准化文件夹名（源文件夹名_版本）
            parsed_info = self.parse_mod_info(mod_source_path, mod_id)
            standardized_name = self.generate_mod_folder_name(os.path.basename(mod_source_path), parsed_info.get('version', '未知'))

            # 检查目标文件夹中是否存在该模组
            mod_target_path = self.resolve_target_mod_path(target_folder, mod_id, standardized_name)
            needs_update = False
            reason = ""
            source_version = ""
            target_version = ""
            
            if os.path.exists(mod_target_path):
                # 模组已存在，检查是否需要更新
                needs_update, reason, source_version, target_version = self.check_mod_needs_update(
                    mod_source_path, mod_target_path, mod_id
                )
                
                # 只有版本号不同时才更新
                if needs_update and "版本不同" in reason:
                    needs_update = True
                else:
                    needs_update = False
                    reason = "版本相同，无需更新"
            else:
                # 模组不存在，需要添加
                needs_update = True
                reason = "新模组，需要添加"
                source_version = "未知"
                target_version = "不存在"
            
            if needs_update:
                # 复制到更新文件夹
                update_mod_path = os.path.join(update_folder, standardized_name)
                if self.copy_mod_folder(mod_source_path, update_mod_path):
                    if os.path.exists(mod_target_path):
                        updated_mods_count += 1
                        print(f"模组 {mod_id} 已更新到更新文件夹: {update_mod_path}")
                    else:
                        new_mods_count += 1
                        print(f"新模组 {mod_id} 已添加到更新文件夹: {update_mod_path}")
                else:
                    print(f"复制模组 {mod_id} 失败")
            else:
                skipped_mods_count += 1
                print(f"模组 {mod_id} 跳过: {reason}")
            
            # 读取模组信息
            mod_info[mod_id] = self.parse_mod_info(mod_source_path, mod_id)
        
        # 在更新文件夹中生成模组信息文件
        self.save_mod_info_json(mod_info, update_folder)
        
        return {
            'total_mods': total_mods_count,
            'new_mods': new_mods_count,
            'updated_mods': updated_mods_count,
            'skipped_mods': skipped_mods_count,
            'update_folder': update_folder,
            'mod_info': mod_info
        }
    
    def parse_mod_info(self, mod_source_path: str, mod_id: str) -> Dict[str, str]:
        """解析模组信息"""
        try:
            server_data_path = os.path.join(mod_source_path, 'ServerData.json')
            if os.path.isfile(server_data_path):
                with open(server_data_path, 'r', encoding='utf-8-sig') as server_file:
                    server_data = json.load(server_file)
                    # 修复：优先读取name字段，如果没有则使用id字段作为名称
                    mod_name = server_data.get('name', server_data.get('id', mod_id))
                    mod_version = server_data.get('revision', {}).get('version', '')
                    return {'name': mod_name, 'version': mod_version}
        except Exception as e:
            print(f"解析模组信息时出错: {e}")
        
        return {'name': mod_id, 'version': '未知'}
    
    def copy_mod_folder(self, source_path: str, target_path: str) -> bool:
        """复制模组文件夹"""
        try:
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
            return True
        except Exception as e:
            print(f"复制模组文件夹时出错: {e}")
            return False
    
    def save_mod_info_json(self, mod_info: Dict[str, Any], target_folder: str) -> str:
        """保存模组信息到JSON文件"""
        try:
            mod_info_path = os.path.join(target_folder, 'mod_info.json')
            with open(mod_info_path, 'w', encoding='utf-8') as f:
                json.dump(mod_info, f, ensure_ascii=False, indent=4)
            return mod_info_path
        except Exception as e:
            print(f"保存模组信息文件时出错: {e}")
            return ""
    
    def process_mods_from_json(self, json_content: str, source_folder: str, target_folder: str) -> Dict[str, Any]:
        """从JSON内容处理模组"""
        try:
            config = json.loads(json_content)
        except Exception as e:
            raise ValueError(f"解析JSON内容时出错: {e}")
        
        if 'game' not in config or 'mods' not in config['game']:
            raise ValueError("JSON文件格式不正确")
        
        mods = config['game']['mods']
        total_mods = len(mods)
        found_and_copied = False
        mod_info = {}
        
        # 统计信息
        total_mods_count = len(mods)
        updated_mods_count = 0
        skipped_mods_count = 0
        new_mods_count = 0
        
        for mod in mods:
            mod_id = mod.get('modId', '')
            if not mod_id:
                continue
                
            for folder_name in os.listdir(source_folder):
                if mod_id in folder_name:
                    mod_source_path = os.path.join(source_folder, folder_name)
                    if not os.path.isdir(mod_source_path):
                        continue

                    parsed = self.parse_mod_info(mod_source_path, mod_id)
                    standardized_name = self.generate_mod_folder_name(os.path.basename(mod_source_path), parsed.get('version', '未知'))

                    standardized_target_path = os.path.join(target_folder, standardized_name)
                    existing_path = self.find_existing_mod_path(target_folder, mod_id)

                    # 若存在旧命名目录且标准化目录不存在，则先重命名为标准化目录，避免重复目录
                    if existing_path and existing_path != standardized_target_path and not os.path.exists(standardized_target_path):
                        try:
                            os.rename(existing_path, standardized_target_path)
                            existing_path = standardized_target_path
                        except Exception:
                            # 如果重命名失败，继续后续逻辑，复制时将覆盖/合并到标准化目录
                            pass

                    mod_target_path = standardized_target_path if os.path.exists(standardized_target_path) else (existing_path or standardized_target_path)
                    existed_before = os.path.exists(mod_target_path)

                    # 检查是否需要更新
                    needs_update, reason, source_version, target_version = self.check_mod_needs_update(
                        mod_source_path, mod_target_path, mod_id
                    )

                    if needs_update:
                        # 复制模组文件夹到目标文件夹（使用标准化名称）
                        if self.copy_mod_folder(mod_source_path, standardized_target_path):
                            if existed_before:
                                updated_mods_count += 1
                            else:
                                new_mods_count += 1
                            found_and_copied = True
                    else:
                        skipped_mods_count += 1

                    # 记录模组信息
                    mod_info[mod_id] = parsed
                    break
        
        return {
            'total_mods': total_mods_count,
            'new_mods': new_mods_count,
            'updated_mods': updated_mods_count,
            'skipped_mods': skipped_mods_count,
            'found_and_copied': found_and_copied,
            'mod_info': mod_info
        }
