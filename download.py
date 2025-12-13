"""
阿里云盘数据集下载脚本
使用前：pip install aligo
首次运行会显示二维码，用阿里云盘APP扫码授权
"""
from aligo import Aligo
import os
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# 配置
DOWNLOAD_DIR = '/root/autodl-tmp/'  # 下载目录
CLOUD_PATH = []  # 云盘目录路径，空表示根目录（转存后文件放根目录）
FILES_TO_DOWNLOAD = [
    'DIV2K_train_HR.zip',
    'DIV2K_valid_HR.zip',
]

def get_all_drive_ids(ali):
    """获取所有可用的drive_id"""
    user = ali.get_user()
    drives = {}
    if hasattr(user, 'default_drive_id') and user.default_drive_id:
        drives['default'] = user.default_drive_id
    if hasattr(user, 'backup_drive_id') and user.backup_drive_id:
        drives['backup'] = user.backup_drive_id
    if hasattr(user, 'resource_drive_id') and user.resource_drive_id:
        drives['resource'] = user.resource_drive_id
    return drives

def navigate_to_folder(ali, path_parts, drive_id=None):
    """导航到指定目录，返回目录ID"""
    parent_id = 'root'
    
    for folder_name in path_parts:
        print(f"   进入目录: {folder_name}")
        file_list = ali.get_file_list(parent_file_id=parent_id, drive_id=drive_id)
        
        found = False
        for f in file_list:
            if f.name == folder_name and f.type == 'folder':
                parent_id = f.file_id
                found = True
                break
        
        if not found:
            # 列出当前目录内容帮助调试
            print(f"   ❌ 未找到文件夹: {folder_name}")
            print(f"   当前目录内容:")
            for f in file_list[:10]:
                print(f"      - {f.name} ({f.type})")
            return None
    
    return parent_id

def list_root_folders(ali, drive_id=None):
    """列出根目录所有文件夹"""
    print(f"\n📂 根目录内容 (drive_id={drive_id}):")
    file_list = ali.get_file_list(parent_file_id='root', drive_id=drive_id)
    for f in file_list:
        print(f"   - {f.name} ({f.type})")
    return file_list

def main():
    print("=" * 50)
    print("阿里云盘数据集下载工具")
    print("=" * 50)
    
    # 登录（首次需扫码）
    ali = Aligo()
    print(f"✅ 登录成功")
    
    # 获取所有drive_id并列出每个盘的内容
    drives = get_all_drive_ids(ali)
    print(f"\n📀 可用的盘:")
    for name, did in drives.items():
        print(f"   - {name}: {did}")
    
    # 选择第一个可用的盘
    drive_id = list(drives.values())[0] if drives else None
    if not drive_id:
        print("\n❌ 未找到可用的盘")
        return
    
    # 如果有CLOUD_PATH，遍历所有盘找到包含目标文件夹的盘
    if CLOUD_PATH:
        target_folder = CLOUD_PATH[0]
        for name, did in drives.items():
            print(f"\n📂 检查 {name} 盘 (drive_id={did}):")
            file_list = ali.get_file_list(parent_file_id='root', drive_id=did)
            for f in file_list:
                print(f"   - {f.name} ({f.type})")
                if f.name == target_folder and f.type == 'folder':
                    drive_id = did
                    print(f"   ✅ 找到 {target_folder}!")
    
    print(f"\n📀 使用 drive_id: {drive_id}")
    
    # 创建下载目录
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # 导航到云盘目录
    print(f"\n📂 定位目录: /{'/'.join(CLOUD_PATH)}")
    folder_id = navigate_to_folder(ali, CLOUD_PATH, drive_id)
    
    if not folder_id:
        print("\n❌ 无法找到云盘目录，请检查 CLOUD_PATH 配置")
        return
    
    # 获取目录下所有文件
    print(f"\n📋 列出目录文件:")
    file_list = ali.get_file_list(parent_file_id=folder_id, drive_id=drive_id)
    file_map = {}
    for f in file_list:
        print(f"   - {f.name}")
        file_map[f.name] = f
    
    # 下载文件
    for filename in FILES_TO_DOWNLOAD:
        print(f"\n🔍 查找: {filename}")
        
        if filename not in file_map:
            print(f"❌ 目录中未找到: {filename}")
            continue
        
        file = file_map[filename]
        print(f"📁 找到: {file.name} (ID: {file.file_id})")
        print(f"📥 开始下载到: {DOWNLOAD_DIR}")
        
        try:
            ali.download_file(file_id=file.file_id, local_folder=DOWNLOAD_DIR)
            print(f"✅ 下载完成: {filename}")
        except Exception as e:
            print(f"❌ 下载失败: {e}")
    
    print("\n" + "=" * 50)
    print("下载完成！后续步骤：")
    print(f"  cd {DOWNLOAD_DIR}")
    print("  unzip DIV2K_train_HR.zip && mv DIV2K_train_HR train_HR")
    print("  unzip DIV2K_valid_HR.zip && mv DIV2K_valid_HR val_HR")
    print("=" * 50)

if __name__ == '__main__':
    main()