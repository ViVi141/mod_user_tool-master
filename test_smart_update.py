#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能更新功能测试脚本
用于验证智能更新模组功能是否正常工作
"""

import os
import json
import tempfile
import shutil
from mod_manager import ModManager

def create_test_mod_folder(base_path, mod_id, version, is_new=False):
    """创建测试模组文件夹"""
    mod_folder = os.path.join(base_path, f"{mod_id}_mod")
    os.makedirs(mod_folder, exist_ok=True)
    
    # 创建ServerData.json文件
    server_data = {
        "id": mod_id,
        "name": f"{mod_id}模组",  # 添加模组名称字段
        "revision": {
            "version": version
        }
    }
    
    server_data_path = os.path.join(mod_folder, "ServerData.json")
    with open(server_data_path, 'w', encoding='utf-8') as f:
        json.dump(server_data, f, ensure_ascii=False, indent=4)
    
    # 创建一些测试文件
    test_file_path = os.path.join(mod_folder, "test.txt")
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(f"这是{mod_id}模组的测试文件，版本: {version}")
    
    return mod_folder

def test_smart_update():
    """测试智能更新功能"""
    print("开始测试智能更新功能...")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = os.path.join(temp_dir, "source")
        target_dir = os.path.join(temp_dir, "target")
        os.makedirs(source_dir, exist_ok=True)
        os.makedirs(target_dir, exist_ok=True)
        
        print(f"临时目录: {temp_dir}")
        print(f"源目录: {source_dir}")
        print(f"目标目录: {target_dir}")
        
        # 创建测试模组
        print("\n创建测试模组...")
        
        # 源模组：版本1.0
        create_test_mod_folder(source_dir, "test_mod1", "1.0")
        create_test_mod_folder(source_dir, "test_mod2", "2.0")
        create_test_mod_folder(source_dir, "test_mod3", "1.5")
        
        # 目标模组：版本1.0（相同），版本1.5（不同），缺少test_mod3
        create_test_mod_folder(target_dir, "test_mod1", "1.0")
        create_test_mod_folder(target_dir, "test_mod2", "1.5")  # 版本不同
        
        # 创建测试JSON配置
        test_json = {
            "game": {
                "mods": [
                    {"modId": "test_mod1"},
                    {"modId": "test_mod2"},
                    {"modId": "test_mod3"}
                ]
            }
        }
        
        json_content = json.dumps(test_json, ensure_ascii=False)
        print(f"测试JSON配置: {json_content}")
        
        # 测试智能更新
        print("\n执行智能更新...")
        mod_manager = ModManager()
        
        try:
            result = mod_manager.smart_update_mods(json_content, source_dir, target_dir)
            
            print("\n智能更新结果:")
            print(f"总模组数: {result['total_mods']}")
            print(f"新增模组: {result['new_mods']}")
            print(f"更新模组: {result['updated_mods']}")
            print(f"跳过模组: {result['skipped_mods']}")
            print(f"更新文件夹: {result['update_folder']}")
            
            # 检查更新文件夹
            if os.path.exists(result['update_folder']):
                print(f"\n更新文件夹内容:")
                for item in os.listdir(result['update_folder']):
                    item_path = os.path.join(result['update_folder'], item)
                    if os.path.isdir(item_path):
                        print(f"  - {item}/ (文件夹)")
                    else:
                        print(f"  - {item} (文件)")
            
            # 验证结果
            expected_new = 1  # test_mod3
            expected_updated = 1  # test_mod2 (版本不同)
            expected_skipped = 1  # test_mod1 (版本相同)
            
            if (result['new_mods'] == expected_new and 
                result['updated_mods'] == expected_updated and 
                result['skipped_mods'] == expected_skipped):
                print("\n✅ 测试通过！智能更新功能正常工作")
                return True
            else:
                print(f"\n❌ 测试失败！期望: 新增{expected_new}, 更新{expected_updated}, 跳过{expected_skipped}")
                return False
                
        except Exception as e:
            print(f"\n❌ 测试过程中出错: {e}")
            return False

if __name__ == "__main__":
    success = test_smart_update()
    if success:
        print("\n🎉 所有测试完成！")
    else:
        print("\n💥 测试失败！")

