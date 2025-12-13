"""
阿里云盘数据集下载脚本
使用前：pip install aligo
首次运行会显示二维码，用阿里云盘APP扫码授权
"""
from aligo import Aligo
import os

# 配置
DOWNLOAD_DIR = '/root/autodl-tmp/'  # 下载目录
CLOUD_DIR = '/WorkData/Datasets/DIV2K'  # 阿里云盘中的目录路径（留空则搜索全盘）
FILES_TO_DOWNLOAD = [
    'DIV2K_train_HR.zip',
    'DIV2K_valid_HR.zip',
]

def get_folder_id(ali, folder_path):
    """获取指定路径的文件夹ID"""
    if not folder_path or folder_path == '/':
        return 'root'
    
    parts = [p for p in folder_path.split('/') if p]
    parent_id = 'root'
    
    for part in parts:
        file_list = ali.get_file_list(parent_file_id=parent_id)
        found = False
        for f in file_list:
            if f.name == part and f.type == 'folder':
                parent_id = f.file_id
                found = True
                break
        if not found:
            print(f"❌ 未找到文件夹: {part}")
            return None
    return parent_id

def main():
    print("=" * 50)
    print("阿里云盘数据集下载工具")
    print("=" * 50)
    
    # 登录（首次需扫码）
    ali = Aligo()
    print(f"✅ 登录成功")
    
    # 获取云盘目录ID
    folder_id = get_folder_id(ali, CLOUD_DIR)
    if folder_id:
        print(f"📂 云盘目录: {CLOUD_DIR}")
    
    # 创建下载目录
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # 获取目录下的文件列表
    if folder_id:
        file_list = ali.get_file_list(parent_file_id=folder_id)
        file_map = {f.name: f for f in file_list}
    else:
        file_map = {}
    
    # 下载文件
    for filename in FILES_TO_DOWNLOAD:
        print(f"\n🔍 查找: {filename}")
        
        # 优先从指定目录查找
        if filename in file_map:
            file = file_map[filename]
        else:
            # 回退到全盘搜索
            print(f"   目录中未找到，尝试全盘搜索...")
            files = ali.search_file(filename)
            if not files:
                print(f"❌ 未找到文件: {filename}")
                print(f"   请确保已上传到阿里云盘: {CLOUD_DIR}")
                continue
            file = files[0]
        
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