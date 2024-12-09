# **项目名: Hello_World**

## **团队名称:**

MoFa团队

**组员：**

- 睿类文特 (GitCode用户名: zonghuanwu)
- ChenZi (GitCode用户名: chenzi00103)

## **项目地址:**

[GitCode Repo 地址](https://gitcode.com/moxin-org/mofa/overview)

------

## **安装与运行手册**

### **环境依赖:**

1. **Rust** (用于运行 Dora-RS 框架)
2. **MoFa 框架库**

### **安装步骤:**

### **运行程序:**

1. **运行智能体框架:**
   ```bash
   dora up && dora build hello_world_dataflow.yml && dora start hello_world_dataflow.yml
   ```

2. **启动任务输入端:**
   - 打开另一个终端窗口，运行 `terminal-input`。
   - 在 `terminal-input` 中输入任务指令即可与智能体交互。

------

## **案例介绍**

**Hello_World** 是一个用于测试项目是否运行的工具，展示了如何使用 MoFa 框架构建智能体。它实现了最基本的智能体设计模式：定制的大语言模型提示与大语言模型推理。

### **突破点:**

- **简化智能体开发流程：** 通过模板化配置，用户可以快速生成定制化智能体。
- **分布式计算支持：** 使用 Dora-RS 框架，确保多个智能体之间的高效协作。
- **灵活的提示定制：** 允许用户通过编辑配置文件轻松定制智能体的行为和响应。

------

## **技术开发介绍**

### **使用的框架与工具:**

- **Dora-RS 框架:** 负责智能体间的分布式计算，确保多个智能体在任务执行中的顺畅协作。
- **MoFa 框架 (MoXin智能体组合框架):** 为智能体之间的交互和编排提供了强大的基础设施。

### **技术难点:**

### **技术难点**

- **通过 Dora 连接不同节点进行协作：**
  实现多个智能体在分布式环境下的高效协作，确保各节点之间的数据同步与通信稳定。需要解决网络延迟、节点故障恢复以及任务分配的优化问题，以保证整体系统的高可用性和一致性。

- **创建一个可自由运行的 Agent：**
  设计智能体架构，使其具备独立运行的能力，能够根据不同任务需求动态调整资源分配和执行策略。确保 Agent 的高效性和灵活性，同时支持多种运行环境和扩展接口，以适应不断变化的应用场景。

- **用户自定义配置的灵活性与安全性：**
  提供强大的配置接口，允许用户自由定制提示词和参数设置，以满足多样化的应用需求。同时，必须确保配置过程的安全性，防止潜在的配置错误或安全漏洞，通过权限控制和验证机制保障系统的稳定运行。

------

## **功能说明**

Hello_World 是 MoFa 中最基本的智能体，设计模式为定制的大语言模型提示加上大语言模型推理。它主要用于测试框架的运行情况以及演示智能体的基本功能。

### **使用场景**

在需要定制大语言模型提示的情况下使用 Hello_World。例如：

- 创建一个以“爱因斯坦”口吻与用户聊天的智能体。
- 创建一个将一个复杂问题拆分成五个小问题的智能体。

### **配置方法**

基本的配置原理是通过修改 hello_world 模板中的配置信息，生成一个定制的智能体。

#### **方法一：使用文本编辑器编辑 MoFa 配置文件**

1. **模板拷贝：**
   - 将包含 hello_world 模板的子目录拷贝到指定目录（例如 `hello_world`）。
   - 目录结构如下：

     | 文件                          | 说明                                                         |
     |-------------------------------|--------------------------------------------------------------|
     | `hello_world_dataflow.yml`    | Dora 数据流配置文件                                           |
     | `configs/agent.yml`           | MoFa 配置文件，包括大语言模型相关参数配置和定制提示参数配置等 |
     | `scripts/agent.py`            | 智能体功能实现的 Python Operator 工具                        |


2. **修改配置：**

   | 文件                            | 说明                                                         |
   |---------------------------------|--------------------------------------------------------------|
   | `hello_world_dataflow.yml`      | 更改 `build: pip install -e ../../../node-hub/terminal-input` 的路径（可使用绝对路径）。 |
   | `configs/agent.yml`             | 根据定制需求，修改 Prompts 和大语言模型参数配置，包括 Rag。 |
   | `scripts/agent.py`              | 修改 `yaml_file_path` 变量对应的 `configs` 的 yml 文件路径。   |



## **运行 Agent**

1. **启动智能体框架：**
   ```bash
   dora up && dora build hello_world_dataflow.yml && dora start hello_world_dataflow.yml
   ```

2. **启动任务输入端：**
   - 打开另一个终端窗口，运行 `terminal-input`。
   - 在 `terminal-input` 中输入任务指令，与智能体进行交互。


## **案例展示**

### **案例 1: 描写自然的诗词**

**提示:** 你是谁？

**Hello_World 案例输出:**
```
Hello, World!
```

**ChatGPT 输出:**
```
你好！我是ChatGPT，由OpenAI开发的人工智能语言模型。我可以帮助回答问题、提供信息、协助完成各种任务。如果你有任何问题或需要帮助，请随时告诉我！
```

**分析:**

- **Hello_World** 通过简单的提示回应 "Hello, World!"，验证了基本的运行状态。
- **ChatGPT** 则生成了生动的自然描写，展示了更高层次的语言生成能力。

### **案例 2: 历史典故的诗词**

**提示:** 关于英雄的历史感怀诗

**Hello_World 输出:**
```
Hello, World!
```

**ChatGPT 输出:**
```
英雄万里行，铁马踏沙场，古今皆壮志，山河共荣光。
```

**分析:**

- **Hello_World** 依然返回 "Hello, World!"，未能完成复杂任务。
- **ChatGPT** 则生成了富有历史感怀的诗句，展现出深刻的历史反思和英雄主义情怀。

