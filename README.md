# 还礼仙翁传 · The Returning Gift Sage

> Cocos Creator 3.8.8 老年修仙放置叙事小游戏

## 环境要求

| 项目 | 版本 |
|------|------|
| Cocos Creator | **3.8.8** |
| 安装路径 | `D:\Program Files\cocos\editors\Creator\3.8.8` |

## 快速开始

1. 打开 Cocos Dashboard 或直接启动编辑器：
   ```
   "D:\Program Files\cocos\editors\Creator\3.8.8\CocosCreator.exe"
   ```
2. **打开项目** → 选择本目录 `00000LegendOfTheElderCultivator`
3. 等待脚本编译完成（首次打开约 1-2 分钟）
4. 确认启动场景为 `assets/scenes/Main.scene`
5. 点击编辑器顶部 **▶ 播放** 按钮预览

## 项目结构

```
LegendOfTheElderCultivator/          # Cocos Creator 3.8.8 项目根目录
├── assets/
│   ├── scenes/Main.scene
│   └── scripts/
│       ├── GameController.ts        # 主界面（赠缘簿 + 日常）
│       ├── core/GameManager.ts      # 赠礼/因果/突破逻辑
│       └── data/GameData.ts         # 境界/人物/地图/剧情
├── docs/
│   ├── 还礼仙翁传/                  # ★ 游戏绑定小说文档
│   │   ├── README.md
│   │   └── chapters/
│   └── 万古守灯人/                  # ★ 《万古守灯人》全部文档
│       ├── README.md                # 文档索引
│       ├── 02-原创小说剧情.md
│       ├── 10-五百万字全书架构.md
│       ├── chapters/                # 五卷分章正文
│       └── scripts/                 # 扩写工具
├── prototype/web/                   # 旧版 HTML5 原型
├── settings/
├── package.json
└── tsconfig.json
```

## 小说文档

**全部剧情与章纲**见 [`docs/还礼仙翁传/README.md`](docs/还礼仙翁传/README.md)。

**《万古守灯人》**独立文档见 [`docs/万古守灯人/README.md`](docs/万古守灯人/README.md)。

## 游戏简介

扮演**莫长春**（七十二岁暮年长老），渡劫失败后获得「赠缘簿」。

- **核心玩法**：向气运之人赠礼 → 即时小回赠 + 因果大回赠（延迟爆发）→ 闭关突破
- **境界**：筑基中期 → 筑基后期 → 金丹 → 元婴 → 化神
- **四张地图**：执法堂、杂役丹堂、百宝阁、九府盟会
- **气运之人**：沈晚晴（天）、柳青鸢（甲）、苏念慈（乙）、顾小满（丁）、秦商言（乙）

## 玩法说明

| 资源 | 说明 |
|------|------|
| 寿元 | 开局 9 月，每 15 回合减 1，赠礼/剧情可延长 |
| 善缘 | 赠礼小回赠获得，突破境界需要 |
| 因果 | 延迟积累，可手动结算或满80自动爆发 |
| 灵石 | 小回赠/大回赠获得 |
| 赠礼次数 | 每月 7 次，每 15 回合重置 |

| 操作 | 说明 |
|------|------|
| 🎁 赠缘簿 | 赠礼获小回赠，同时积累因果（首赠加成） |
| 日常行动 | 修炼、巡视、交易等 |
| 闭关突破 | 修为满后突破境界 |
| 结算因果 | 消耗因果换取修为和灵石（≥20可结算，≥80自动爆发） |

## 脚本说明

| 脚本 | 职责 |
|------|------|
| `GameData.ts` | 境界、气运人物、赠礼、地图、剧情事件 |
| `GameManager.ts` | 赠礼逻辑、首赠加成、因果结算、存档 |
| `GameController.ts` | 动态 UI（赠缘簿区 + 日常区） |

## 构建发布

1. 菜单 **项目 → 构建发布**
2. 选择平台（Web Mobile / 微信小游戏 / Android 等）
3. 点击 **构建** → **运行**

## 版权说明

- 主剧情《还礼仙翁传》：完全原创
- 《万古守灯人》文档：[`docs/万古守灯人/`](docs/万古守灯人/README.md)
- 游戏代码可自由修改和分发
