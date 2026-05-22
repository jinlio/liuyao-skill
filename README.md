# liuyao-skill

基于周易原理的六爻占卜与解卦 skill，供 AI 编码助手（opencode、Claude Code 等）调用。

## 功能

- **三种起卦方式**：铜钱法、蓍草法、手动输入
- **自动推导变卦**：动爻翻转后计算变卦名
- **卦辞爻辞查询**：完整收录六十四卦卦辞与爻辞
- **解卦规则指引**：按动爻数量给出解读侧重
- **三不占原则**：占卜前自动检查是否满足诚、义、疑

## 快速使用

```bash
# 铜钱法起卦（推荐）
python3 scripts/qigua.py --method coin --json

# 蓍草法起卦
python3 scripts/qigua.py --method shicao --json

# 手动输入（6个0-3的数字，逗号分隔）
python3 scripts/qigua.py --method manual --input "1,2,3,0,1,2" --json
```

输出 JSON 包含本卦名、变卦名、各爻详情、动爻标签等。

## 项目结构

```
├── SKILL.md                 Skill 定义与占卜流程说明
├── assets/
│   └── gua-data.json        八卦与六十四卦结构化数据
├── references/
│   ├── 64gua-table.md       六十四卦速查表
│   ├── guaci-full.md        六十四卦卦辞全文
│   ├── yaoci-full.md        六十四卦爻辞全文
│   └── jiegu-guide.md       解卦方法与注解指引
├── scripts/
│   ├── qigua.py             起卦脚本（核心）
│   └ regenerate_guaci.py   重新生成 guaci-full.md
├── tests/
│   └ test_qigua.py          单元测试
└── .gitignore
```

## 作为 Skill 使用

将本项目目录放入编码助手的 skill 配置路径，助手会在用户提及六爻、占卜、起卦、解卦、算卦、周易、易经、卦象、divination、hexagram 等关键词时自动激活。

详见 `SKILL.md` 中的完整占卜流程与解卦规则。

## 测试

```bash
python3 -m unittest discover -s tests -v
```

## 蓍草法概率

脚本按经典蓍草法爻值概率建模：

| 爻值 | 类型 | 概率 |
|------|------|------|
| 6 | 老阴（动爻） | 1/16 |
| 7 | 少阳（静爻） | 5/16 |
| 8 | 少阴（静爻） | 7/16 |
| 9 | 老阳（动爻） | 3/16 |

## License

[MIT](LICENSE)