# 高分辨率图像修复与增强 (SR-GAN)

基于 MindSpore 2.2.14 实现的图像超分辨率重建与修复项目。

## 功能

- 低清图像超分辨率重建 (LR→HR, ×4放大)
- 去噪、去模糊、去压缩伪影
- 真实旧照片修复与增强

## 技术架构

| 组件 | 说明 |
|------|------|
| **生成器** | SRResNet (23残差块 + PixelShuffle上采样) |
| **判别器** | VGG风格 PatchGAN |
| **损失函数** | L1像素损失 + BCE对抗损失 |
| **评估指标** | PSNR↑、SSIM↑ |
| **训练策略** | 两阶段训练（像素预训练+GAN精调） |

## 环境要求

- Python 3.9
- MindSpore 2.2.14 (CPU/GPU)
- 详见 `requirements.txt`

## 安装

需要提前准备 mindspore-2.2.14-cp39-cp39-win_amd64.whl 文件，可在官网历史版本处自行下载。

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 安装MindSpore (CPU、GPU通用版)
pip install mindspore-2.2.14-cp39-cp39-win_amd64.whl
```

## 数据集准备

将数据放置于 `data/` 目录：
只需要准备train_HR、val_HR、old_photos数据集即可，然后执行re_data.ipynb数据预处理工具生成其他数据集。

```text
data/
├── train_HR/    # 训练高分辨率图像
├── train_LR/    # 训练低分辨率图像 (文件名格式: {stem}x4.png)
├── val_HR/      # 验证高分辨率图像
├── val_LR/      # 验证低分辨率图像
└── old_photos/  # 旧照片 (用于推理)
```

**推荐数据集**: [DIV2K](https://data.vision.ee.ethz.ch/cvl/DIV2K/)

## 使用方法

### 两阶段训练流程

1. **第一阶段 - 像素级预训练**
   - 打开 `restoration_stage1.ipynb`
   - 训练600轮，使用L1损失
   - 输出：`ckpt_sr_stage1/G_best.ckpt`

2. **第二阶段 - GAN精调**
   - 打开 `restoration_stage2.ipynb`
   - 加载第一阶段权重
   - 训练200轮，使用L1+对抗损失
   - 输出：`ckpt_sr_stage2/G_best.ckpt`

## 项目结构

```text
TrainGAN2/
├── restoration_stage1.ipynb  # 第一阶段训练（像素预训练）
├── restoration_stage2.ipynb  # 第二阶段训练（GAN精调）
├── restoration.ipynb         # 原始训练notebook
├── tools/
│   └── re_data.ipynb        # 数据预处理工具
├── requirements.txt          # 依赖列表
└── docs/                    # 项目文档
    └── TrainGAN2项目设计文档.md
```

## 训练输出

训练完成后生成：

- `ckpt_sr_stage1/G_best.ckpt` - 第一阶段最佳生成器权重
- `ckpt_sr_stage2/G_best.ckpt` - 第二阶段最佳生成器权重
- `ckpt_sr_stage2/D_best.ckpt` - 最佳判别器权重
- `ckpt_sr_stage1/training_curves.png` - 第一阶段训练曲线
- `ckpt_sr_stage2/training_curves.png` - 第二阶段训练曲线
- `output_sr/` - 推理结果

## 验收标准

- PSNR ≥ 25dB
- SSIM ≥ 0.5

## License

MIT
