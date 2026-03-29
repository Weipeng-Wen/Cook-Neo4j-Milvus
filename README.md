# 🍳 Cook-RAG-GraphRAG

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white">
  <img alt="Neo4j" src="https://img.shields.io/badge/Neo4j-GraphDB-4581C3?logo=neo4j&logoColor=white">
  <img alt="Milvus" src="https://img.shields.io/badge/Milvus-VectorDB-00BFA6">
  <img alt="RAG" src="https://img.shields.io/badge/RAG-Graph%2BHybrid-orange">
</p>

<p align="center">
  🥘 图谱 + 向量双检索 ｜ 🧠 智能路由 ｜ ⚡ 流式回答 ｜ 🧾 菜谱知识图谱
</p>

一个面向「做菜问答」场景的 GraphRAG 项目：
- 用 **Neo4j** 存储菜谱知识图谱（菜谱、食材、步骤、分类等）
- 用 **Milvus + Embedding** 做语义检索
- 用 **Hybrid Retrieval + GraphRAG Retrieval** 联合召回
- 用 **Intelligent Query Router** 根据问题复杂度自动选策略
- 用 **LLM** 进行最终答案生成（支持流式输出）

---

## ✨ 项目亮点

- 🍜 **双引擎检索**：传统混合检索（关键词/向量）+ 图结构检索并行支持
- 🧭 **智能路由**：自动判断复杂问题是否需要图推理
- 🕸️ **图推理能力**：支持多跳路径、子图抽取、关系推理
- 🌊 **流式回答**：前端实时显示模型输出，交互体验更丝滑
- 🧱 **模块化设计**：`rag_modules/` 可拆可扩展，便于后续迭代

---

## 🗂️ 项目结构

```text
cook-rag-graphRAG/
├─ app.py                         # FastAPI 服务入口（启动即初始化系统）
├─ main.py                        # 核心系统编排：初始化、建库、问答、交互式 CLI
├─ config.py                      # GraphRAG 配置数据类（Neo4j/Milvus/模型参数）
├─ main.html                      # Web 聊天前端（流式渲染 Markdown）
├─ requirements.txt               # Python 依赖
├─ test.py                        # FastAPI 表单/模型校验示例接口
├─ .env                           # 环境变量（LLM API Key、模型ID、Base URL 等）
│
├─ rag_modules/
│  ├─ __init__.py                 # 模块导出
│  ├─ graph_data_preparation.py   # 从 Neo4j 读图数据并构造成文档、分块
│  ├─ milvus_index_construction.py# 向量化、建 Milvus 集合与索引、相似度检索
│  ├─ graph_indexing.py           # 图实体/关系 K-V 索引构建与去重
│  ├─ hybrid_retrieval.py         # 双层检索 + 向量增强 + round-robin 融合
│  ├─ graph_rag_retrieval.py      # 图查询理解、多跳遍历、子图抽取与图推理
│  ├─ intelligent_query_router.py # 查询分析与检索策略路由（hybrid/graph/combined）
│  └─ generation_integration.py   # LLM 回答生成（普通/流式，含重试与降级）
│
├─ data/
│  ├─ docker-compose.yml          # Neo4j 容器与初始化脚本编排
│  └─ cypher/
│     ├─ nodes.csv                # 图节点数据
│     ├─ relationships.csv        # 图关系数据
│     └─ neo4j_import.cypher      # CSV 导入 Neo4j 的脚本（建约束/索引/关系）
│
└─ agent(代码系ai生成)/
   ├─ recipe_ai_agent.py          # 基于 Kimi API 的菜谱解析 Agent（MD -> 结构化）
   ├─ run_ai_agent.py             # Agent 运行入口（测试/批处理）
   ├─ batch_manager.py            # 批处理进度管理与断点续跑
   ├─ amount_normalizer.py        # 食材用量标准化工具
   ├─ config.json                 # Agent 配置（API/批大小/输出格式）
   ├─ requirements.txt            # Agent 子模块依赖
   ├─ recipe_ontology_design.md   # 菜谱知识图谱本体设计说明
   └─ AI_AGENT_README.md          # Agent 子模块说明文档
```

---

## 🧠 系统工作流

```text
用户问题
  ↓
IntelligentQueryRouter（复杂度/关系密度分析）
  ├─ 简单问题 → HybridRetrieval（关键词/图索引/向量）
  ├─ 复杂问题 → GraphRAGRetrieval（多跳/子图/推理）
  └─ 组合问题 → Combined（两路结果融合）
  ↓
GenerationIntegration（LLM 生成自然语言答案）
  ↓
前端流式展示（main.html）
```

---

## 🛠️ 技术栈

- **后端框架**：FastAPI, Uvicorn
- **图数据库**：Neo4j
- **向量数据库**：Milvus (pymilvus)
- **检索与编排**：LangChain Core / Community / HuggingFace
- **向量模型**：`BAAI/bge-small-zh-v1.5`（默认）
- **大模型调用**：OpenAI SDK 兼容接口（可接入兼容 OpenAI API 的模型服务）
- **前端**：HTML + Vanilla JS + Marked.js（Markdown 渲染）
- **数据处理**：pandas, numpy, scikit-learn 等

---

## 🚀 快速开始

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 配置环境变量

在项目根目录创建 `.env`（或补全已有文件）：

```env
LLM_MODEL_ID=your_model_id
LLM_API_KEY=your_api_key
LLM_BASE_URL=your_base_url
```

### 3) 启动 Neo4j（可选：通过 Docker）

```bash
cd data
docker compose up -d
```

> `data/docker-compose.yml` 中已包含 Neo4j 与初始化导入任务（`neo4j-init`）。

### 4) 启动服务

```bash
uvicorn app:app --reload
```

浏览器访问：`http://127.0.0.1:8000`

---

## 📄 关键文件说明（详细版）

### 根目录

- `app.py`
  - FastAPI 服务层。
  - 在 `lifespan` 启动阶段自动初始化 `AdvancedGraphRAGSystem` 并构建/加载知识库。
  - 提供 `/chat` 流式接口，前端通过 `fetch + reader` 实时拉取回答。

- `main.py`
  - 项目核心 orchestrator（总控）。
  - 负责按顺序初始化：数据准备模块、Milvus索引模块、生成模块、检索模块、路由模块。
  - 支持知识库构建、交互式命令行问答、统计信息输出、资源清理。

- `config.py`
  - `GraphRAGConfig` 数据类，统一管理 Neo4j、Milvus、模型、检索、切块参数。
  - 提供 `to_dict/from_dict`，便于后续做配置文件化。

- `main.html`
  - 单页聊天界面。
  - 特点：消息气泡、打字动画、Markdown 渲染、流式拼接输出。

- `requirements.txt`
  - 主系统依赖，覆盖模型推理、向量检索、图数据库访问、Web 服务。

- `test.py`
  - 独立 FastAPI 示例（简单的表单提交与 Pydantic 校验）。
  - 更像实验文件，不参与主流程。

### `rag_modules/`

- `graph_data_preparation.py`
  - 从 Neo4j 读取 Recipe / Ingredient / CookingStep。
  - 拼装成结构化菜谱文档，再按规则切块（chunk）供检索使用。
  - 提供统计信息（类别分布、文档长度等）。

- `milvus_index_construction.py`
  - 使用 `HuggingFaceEmbeddings` 进行向量化。
  - 建 Milvus collection/schema/index（HNSW + COSINE）。
  - 支持索引构建、增量写入、相似度检索、集合状态管理。

- `graph_indexing.py`
  - 将图中的实体和关系构造成可检索的 K-V 索引。
  - 支持关系键扩展、去重、key-to-entity/relation 映射。

- `hybrid_retrieval.py`
  - 先做“实体层 + 主题层”双层检索，再做向量增强。
  - 使用 round-robin 融合多路召回，统一输出文档结果。

- `graph_rag_retrieval.py`
  - 负责图语义查询理解（QueryType）。
  - 提供多跳遍历、子图抽取、图结构推理、图相关性排序。

- `intelligent_query_router.py`
  - 分析问题复杂度、关系强度、推理需求。
  - 决策使用 `hybrid_traditional` / `graph_rag` / `combined`。
  - 维护路由统计，为优化策略提供依据。

- `generation_integration.py`
  - 将召回文档拼上下文，调用 LLM 生成答案。
  - 支持非流式与流式输出，流式失败时自动降级重试。

### `data/`

- `docker-compose.yml`
  - 用于快速拉起 Neo4j（含 APOC 配置）和初始化导入服务。

- `cypher/nodes.csv`
  - 知识图谱节点数据（根概念、菜谱、食材、步骤、分类等）。

- `cypher/relationships.csv`
  - 节点间关系数据（例如 `REQUIRES`, `CONTAINS_STEP` 等）。

- `cypher/neo4j_import.cypher`
  - 完整导入脚本：建约束、建索引、加载 CSV、创建关系与分类节点。

### `agent(代码系ai生成)/`（可选子系统）

这个目录是“数据生产侧”的 AI 工具链，可用于把大量 Markdown 菜谱自动转成图谱数据：

- `recipe_ai_agent.py`
  - 基于 Kimi API 抽取菜谱结构化信息（食材、步骤、难度、分类等）。

- `run_ai_agent.py`
  - 命令行入口，支持单测和批量处理。

- `batch_manager.py`
  - 支持分批、断点续跑、进度查看与合并结果。

- `amount_normalizer.py`
  - 把“适量/少许/一勺”等中文烹饪用量标准化，便于后续分析。

- `config.json`
  - Agent 的 API 配置、处理参数、输出格式控制。

- `recipe_ontology_design.md`
  - 菜谱知识图谱的本体设计说明。

- `AI_AGENT_README.md`
  - 子系统使用文档。

---

## 📌 运行模式

- **Web 模式（推荐）**

```bash
uvicorn app:app --reload
```

- **CLI 模式**

```bash
python main.py
```

- **Agent 处理模式（可选）**

```bash
cd "agent(代码系ai生成)"
python run_ai_agent.py test
python run_ai_agent.py /path/to/recipes
```

---

## 🧪 后续可优化方向

- 增加自动评测集（问答正确率、召回覆盖率、路由命中率）
- 为 GraphRAG 增加更完整的路径解释可视化
- 引入缓存层（embedding/query/result）降低延迟
- 提供 Docker 一键启动后端 + 前端 + Neo4j + Milvus 的完整编排

---

## 📮 说明

如果你是项目维护者，建议在公开仓库中：
- 不提交真实 API Key（`.env`、`config.json` 里都建议改成占位符）
- 增加 `.gitignore` 保护敏感文件与运行缓存

---

<p align="center">
  做菜不只靠经验，也可以靠图谱和检索 🥢
</p>
