# Contributing to liuyao-skill

感谢你对本项目的关注！

## 开发环境

```bash
git clone https://github.com/jinlio/liuyao-skill.git
cd liuyao-skill
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## 运行测试

```bash
# 运行全部测试
python3 -m pytest -v

# 查看覆盖率
python3 -m pytest --cov=scripts --cov-report=term-missing
```

## 代码风格

项目使用 [Ruff](https://docs.astral.sh/ruff/) 进行代码检查和格式化：

```bash
# 检查
ruff check .

# 自动修复
ruff check --fix .

# 格式化
ruff format .
```

## 提交规范

使用 Conventional Commits 格式：

```
<type>: <description>

类型: feat, fix, refactor, docs, test, chore
```

## Pull Request 流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feat/xxx`)
3. 确保测试通过 (`python3 -m pytest -v`)
4. 确保 lint 通过 (`ruff check .`)
5. 提交 PR 并描述改动内容

## 添加新卦数据

如果需要修正或补充卦辞、爻辞：

1. 编辑 `scripts/regenerate_guaci.py` 中的 `GUACI_DATA`
2. 运行 `python3 scripts/regenerate_guaci.py` 重新生成 `references/guaci-full.md`
3. 运行测试确认数据一致性
