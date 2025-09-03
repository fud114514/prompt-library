# 📚 Prompt Library - 高质量提示词库

![License](https://img.shields.io/badge/license-MIT-blue)
![提示词数量](https://img.shields.io/badge/prompts-350%2B-green)
![分类数量](https://img.shields.io/badge/categories-58-orange)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

一个全面的高质量AI提示词库，支持Excel和Markdown格式之间的双向转换。

## 🌟 项目特点

- 📊 **双向转换**: 支持Excel ↔️ Markdown格式互转
- 🗂️ **结构化管理**: 58个分类，350+个精心设计的提示词
- 🔄 **版本控制**: 支持提示词版本迭代和管理
- 🤖 **多平台兼容**: 适用于Claude、GPT、Gemini等主流AI模型
- 🛠️ **自动化工具**: 提供批量转换和管理脚本

## 📂 项目结构

```
prompt-library/
├── prompt_excel/           # Excel源文件目录
│   └── prompt (3).xlsx    # 主要提示词Excel文件
├── prompt_docs/           # 转换后的Markdown文档
│   └── prompt_docs_*/     # 按时间戳命名的文档快照
├── scripts/               # 转换和管理脚本
│   ├── excel_to_docs.py  # Excel转Markdown核心脚本
│   ├── docs_to_excel.py  # Markdown转Excel核心脚本
│   ├── convert_local.py  # 本地转换工具
│   ├── start_convert.py  # 批量转换启动器
│   └── config.yaml       # 配置文件
├── docs/                  # 项目文档
└── tests/                # 测试脚本
```

## 🚀 快速开始

### 安装依赖

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r scripts/requirements.txt
```

### 基础使用

#### Excel → Markdown 转换

```bash
# 转换单个Excel文件
python scripts/start_convert.py --mode excel2docs --select prompt_excel/prompt\ \(3\).xlsx

# 扫描并转换所有Excel文件
python scripts/start_convert.py --mode excel2docs --excel-dir prompt_excel
```

#### Markdown → Excel 转换

```bash
# 转换指定的文档目录
python scripts/start_convert.py --mode docs2excel --select prompt_docs/prompt_docs_2025_0903_055708

# 自动扫描并转换
python scripts/start_convert.py --mode docs2excel
```

## 📚 提示词分类

项目包含58个精心组织的分类，涵盖：

### 核心分类
- 🔧 **元提示词** - 15个高级提示词工程模板
- 📖 **说明文档** - 必看的重要使用说明
- 🏗️ **软件工程** - 专业的编程和架构提示词
- 📊 **分析工具** - 数据分析和可视化提示词

### 专业领域
- 🧠 **哲学工具箱** - 深度思考和哲学分析
- 📈 **行业咨询** - 商业和行业分析模板
- 🎯 **需求解析** - 需求分析和规划工具
- 📐 **序列图生成** - 技术文档和流程图生成

### 创意内容
- ✍️ **写作辅助** - 各类文章和创意写作
- 🎨 **排版工具** - 文档格式化和美化
- 📱 **社交媒体** - Twitter、Reddit等平台内容
- 🎬 **视频处理** - 字幕生成和视频脚本

### 特色工具
- 🔄 **翻译工具** - 多语言翻译和本地化
- 📝 **学术写作** - 论文和学术内容生成
- 🎮 **游戏设计** - 游戏剧情和世界观构建
- 💼 **商业文档** - 商业计划和报告模板

## 🔧 高级功能

### 批量处理

```bash
# 使用main.py进行批量处理
python main.py --select "prompt_excel/prompt (3).xlsx"
```

### 配置文件

编辑 `scripts/config.yaml` 来自定义：
- 输出目录路径
- 文件命名规则
- 转换选项
- 工具链接和资源

### 版本管理

系统自动为每次转换创建时间戳目录：
- 格式：`prompt_docs_YYYY_MMDD_HHMMSS`
- 保留完整的转换历史
- 支持版本对比和回滚

## 📊 统计信息

- **提示词总数**: 350+
- **分类数量**: 58
- **版本总数**: 500+
- **支持格式**: Excel (.xlsx), Markdown (.md), JSON
- **最后更新**: 2025-09-03

## 🤝 贡献指南

欢迎贡献新的提示词或改进现有内容：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/NewPrompt`)
3. 提交更改 (`git commit -m 'Add new prompt category'`)
4. 推送到分支 (`git push origin feature/NewPrompt`)
5. 创建 Pull Request

### 提示词格式规范

- 使用清晰的分类名称
- 包含版本信息（如 v1.0, v1.1）
- 提供使用说明和示例
- 标注适用的AI模型

## 🛠️ 技术栈

- **Python 3.8+** - 核心开发语言
- **pandas** - Excel数据处理
- **openpyxl** - Excel文件读写
- **PyYAML** - 配置文件管理
- **InquirerPy** - 交互式命令行界面
- **python-dotenv** - 环境变量管理

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔗 相关链接

- [GitHub仓库](https://github.com/fud114514/prompt-library)
- [问题反馈](https://github.com/fud114514/prompt-library/issues)
- [贡献指南](https://github.com/fud114514/prompt-library/blob/main/CONTRIBUTING.md)

## 👥 作者

- **fud114514** - [GitHub Profile](https://github.com/fud114514)

## 🙏 致谢

感谢所有贡献者和使用者的支持！

---

⭐ 如果这个项目对你有帮助，请给它一个星标！

📧 有问题或建议？请[创建Issue](https://github.com/fud114514/prompt-library/issues/new)