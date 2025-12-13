# 高分辨率图像修复与增强 (SR-GAN)

基于 MindSpore 2.2.14 实现的图像超分辨率重建与修复项目。

## 功能

- 低清图像超分辨率重建 (LR→HR, ×4放大)
- 去噪、去模糊、去压缩伪影
- 真实旧照片修复与增强

## 技术架构

| 组件 | 说明 |
|------|------|
| **生成器** | SRResNet (16残差块 + PixelShuffle上采样) |
| **判别器** | VGG风格 PatchGAN |
| **损失函数** | L1像素损失 + BCE对抗损失 |
| **评估指标** | PSNR↑、SSIM↑ |

## 环境要求

- Python 3.9
- MindSpore 2.2.14 (CPU/GPU)
- 详见 `requirements.txt`

## 安装

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 安装MindSpore (CPU版)
pip install mindspore-2.2.14-cp39-cp39-win_amd64.whl

# GPU版 (Linux CUDA 11.6)
pip install mindspore==2.2.14 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 数据集准备

将数据放置于 `data/` 目录：

```
data/
├── train_HR/    # 训练高分辨率图像
├── train_LR/    # 训练低分辨率图像 (文件名格式: {stem}x4.png)
├── val_HR/      # 验证高分辨率图像
├── val_LR/      # 验证低分辨率图像
└── old_photos/  # 旧照片 (用于推理)
```

**推荐数据集**: [DIV2K](https://data.vision.ee.ethz.ch/cvl/DIV2K/)

## 使用方法

1. 打开 `restoration.ipynb`
2. 按顺序运行各cell完成：
   - 环境验证
   - 数据加载
   - 模型训练
   - 评估与推理

## 项目结构

```
TrainGAN2/
├── restoration.ipynb    # 主训练notebook
├── tools/
│   └── re_data.ipynb    # 数据预处理工具
├── requirements.txt     # 依赖列表
└── docs/                # 项目文档
```

## 训练输出

训练完成后生成：
- `ckpt_sr/G_best.ckpt` - 最佳生成器权重
- `ckpt_sr/training_curves.png` - 训练曲线
- `output_sr/` - 推理结果

## 验收标准

- PSNR ≥ 28dB
- SSIM ≥ 0.80

## License

MIT
