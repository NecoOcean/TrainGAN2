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
FILES_TO_DOWNLOAD = [
    'DIV2K_train_HR.zip',
    'DIV2K_valid_HR.zip',
]

def main():
    print("=" * 50)
    print("阿里云盘数据集下载工具")
    print("=" * 50)
    
    # 登录（首次需扫码）
    ali = Aligo()
    print(f"✅ 登录成功")
    
    # 创建下载目录
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # 下载文件
    for filename in FILES_TO_DOWNLOAD:
        print(f"\n🔍 搜索: {filename}")
        
        # 全盘搜索（去掉扩展名搜索更容易匹配）
        search_name = filename.replace('.zip', '')
        files = ali.search_file(search_name)
        
        print(f"   搜索关键词: {search_name}")
        print(f"   找到 {len(files) if files else 0} 个结果")
        
        if files:
            for i, f in enumerate(files[:5]):  # 显示前5个结果
                print(f"   [{i}] {f.name}")
        
        if not files:
            print(f"❌ 未找到文件: {filename}")
            print(f"   请尝试在云盘中搜索确认文件名")
            continue
        
        # 精确匹配文件名
        file = None
        for f in files:
            if f.name == filename:
                file = f
                break
        
        if not file:
            file = files[0]  # 使用第一个结果
        
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