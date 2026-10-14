# 图片测量与比较接口

依赖 Python 3.10+ 与 Pillow。执行顺序以[图片测量与校准](calibration.md)为准；本文件定义静态图片测量、比较的输入、命令和输出。所有路径相对各自清单目录解析，输出目录必须是新目录。

## 区域清单

在任务目录保存 `regions.json`。坐标使用原图像素；看到缩略图时，先按原图实际宽高分别换算坐标。

```json
{
  "reference": "reference.png",
  "css_viewport_width": 1024,
  "regions": [
    {"name": "background", "kind": "color", "box": [20, 20, 100, 40], "inset": 2},
    {"name": "card-a", "box": [40, 200, 280, 320], "group": "cards"},
    {"name": "card-b", "box": [344, 200, 280, 320], "group": "cards"},
    {"name": "title-ink", "box": [40, 90, 420, 70], "box_type": "ink"}
  ]
}
```

| 字段 | 含义 |
| --- | --- |
| `name` | 区域或扫描的唯一名称 |
| `box` | 原图像素的 `[x, y, width, height]`，整数且不得越界；不是右下角坐标 |
| `kind` | `box`（默认）记录几何；`color` 统计框内颜色 |
| `box_type` | `element` 为元素外框，`ink` 为可见字形，`sample` 为采样区；颜色区必须为 `sample` |
| `inset` | 颜色采样向内避开的像素数，不得使区域变空 |
| `group` | 同一横向重复结构，至少两个元素框，不混入字形或采样框 |
| `css_viewport_width` | 已知时填写的逻辑视口宽度，用于建立 CSS 与图像像素比例；不证明参考图原始 DPR 或视口 |
| `vertical_scans` | 可选的纵向颜色阈值扫描，详见下文 |

## 命令与产物

以下路径为示例，占位目录需替换为本次任务路径。

| 阶段 | 命令 | 主要输出 |
| --- | --- | --- |
| 测量 | `python3 scripts/measure_reference.py --manifest /task/regions.json --out-dir /task/measurement-01` | `measurements.json` 与自包含标注图 `annotations.svg` |
| 比较 | `python3 scripts/compare_mockup.py --reference /task/reference.png --candidate /task/candidate.png --out-dir /task/image-report --prefix screen` | 比较指标、差异图和未匹配尾部图（如有） |

`measurements.json` 保存原图尺寸与摘要、原始坐标、归一化比例、可选 CSS 映射、RGB 中位数与 10%／90% 分位数、网格尺寸和间距分布。`annotations.svg` 用于核对人工选区，不代表自动识别边界。

`compare_mockup.py` 默认要求两张图宽高一致；显式增加 `--allow-height-difference` 后，只比较共同坐标并保留高度差与未匹配尾部。宽度不一致始终停止，不自动拉伸。可用 `--clip header:0,0,1024,80` 限定区域，坐标为图片像素。

已有浏览器截图可以作为候选图片输入。比较仅检查图片像素，不验证页面身份、DOM、资源加载或交互。

## 可选的纵向色带扫描

适合阈值判断的平坦色带可在清单中增加：

```json
{"vertical_scans": [{"name": "light-band-left", "x": 10, "y": 300, "height": 500, "min_channel": 175, "max_channel_spread": 45, "min_run": 20}]}
```

脚本寻找各通道不低于 `min_channel`、通道最大差不超过 `max_channel_spread`、长度至少为 `min_run` 的不透明连续区间，结束坐标不包含尾像素。多个横坐标可帮助定位斜边；命中也可能是文字或插画高光，不能自动认定为区块边界。

## 失败语义

- 标注越界、区域无效、颜色没有不透明样本、输出目录已存在：退出码 2，不自动裁短错误框或覆盖旧结果。
- 比较图片的宽度不一致、未允许的高度差或裁剪区域无效：比较停止，不拉伸图片，也不生成通过结论。
- 图像差异只用于定位变化，不设通用审美通过阈值。
