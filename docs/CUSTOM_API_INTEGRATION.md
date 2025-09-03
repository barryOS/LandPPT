# 自定义API集成指南

本指南将帮助您将LandPPT与您自己的AI API集成，无论是自建的模型服务还是第三方API。

## 目录

- [快速开始](#快速开始)
- [支持的API类型](#支持的api类型)
- [配置说明](#配置说明)
- [高级配置](#高级配置)
- [示例配置](#示例配置)
- [故障排查](#故障排查)
- [API要求](#api要求)

## 快速开始

### 1. 基本配置

最简单的配置只需要两个环境变量：

```bash
# .env 文件
CUSTOM_API_URL=https://your-api.com/v1/chat/completions
CUSTOM_API_KEY=your-api-key-here
DEFAULT_AI_PROVIDER=custom
```

### 2. 测试连接

```bash
# 运行测试脚本
python test_custom_api.py
```

### 3. 在项目中使用

```python
from landppt.ai import get_ai_provider

# 自动使用配置的自定义API
provider = get_ai_provider("custom")
response = await provider.chat_completion(messages)
```

## 支持的API类型

### 1. OpenAI兼容API（推荐）

如果您的API兼容OpenAI格式，无需额外配置：

- **通义千问 (Qwen)**
- **文心一言 (ERNIE)**
- **ChatGLM**
- **Moonshot AI**
- **DeepSeek**
- **任何兼容OpenAI的API**

配置示例：

```bash
CUSTOM_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
CUSTOM_API_KEY=sk-your-api-key
CUSTOM_API_MODEL=qwen-turbo
```

### 2. 完全自定义API

对于不兼容OpenAI格式的API，可以自定义请求和响应格式。

## 配置说明

### 基础配置

| 环境变量 | 说明 | 必需 | 默认值 |
|---------|------|------|--------|
| `CUSTOM_API_URL` | API端点URL | ✅ | - |
| `CUSTOM_API_KEY` | API密钥 | ✅ | - |
| `CUSTOM_API_MODEL` | 模型名称 | ❌ | custom-model |
| `DEFAULT_AI_PROVIDER` | 设为`custom`以默认使用自定义API | ❌ | openai |

### 认证配置

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `CUSTOM_API_KEY_HEADER` | API密钥的请求头名称 | Authorization |
| `CUSTOM_API_KEY_PREFIX` | API密钥的前缀 | Bearer |

示例：

```bash
# 标准Bearer Token（默认）
CUSTOM_API_KEY_HEADER=Authorization
CUSTOM_API_KEY_PREFIX=Bearer
# 请求头：Authorization: Bearer your-api-key

# 自定义头部
CUSTOM_API_KEY_HEADER=X-API-Key
CUSTOM_API_KEY_PREFIX=
# 请求头：X-API-Key: your-api-key
```

### 请求/响应格式

| 环境变量 | 说明 | 选项 | 默认值 |
|---------|------|------|--------|
| `CUSTOM_REQUEST_FORMAT` | 请求格式类型 | openai, custom | openai |
| `CUSTOM_RESPONSE_FORMAT` | 响应格式类型 | openai, custom | openai |

## 高级配置

### 自定义请求格式

当`CUSTOM_REQUEST_FORMAT=custom`时，使用自定义请求模板：

```bash
CUSTOM_REQUEST_TEMPLATE='{
  "prompt": "{{messages}}",
  "parameters": {
    "max_length": {{max_tokens}},
    "temperature": {{temperature}}
  }
}'
```

可用占位符：
- `{{messages}}` - 消息列表
- `{{model}}` - 模型名称
- `{{max_tokens}}` - 最大token数
- `{{temperature}}` - 温度参数
- `{{top_p}}` - Top-p参数

### 自定义响应解析

当`CUSTOM_RESPONSE_FORMAT=custom`时，指定数据提取路径：

```bash
# 使用点号分隔的路径
CUSTOM_RESPONSE_CONTENT_PATH=data.generated_text
CUSTOM_RESPONSE_MODEL_PATH=metadata.model_id
CUSTOM_RESPONSE_USAGE_PATH=statistics.tokens
```

路径示例：
- `data.text` - 提取 `response["data"]["text"]`
- `choices.0.content` - 提取 `response["choices"][0]["content"]`
- `result` - 提取 `response["result"]`

## 示例配置

### 示例1：通义千问

```bash
DEFAULT_AI_PROVIDER=custom
CUSTOM_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
CUSTOM_API_KEY=sk-your-api-key
CUSTOM_API_MODEL=qwen-turbo
CUSTOM_REQUEST_FORMAT=openai
CUSTOM_RESPONSE_FORMAT=openai
```

### 示例2：文心一言

```bash
DEFAULT_AI_PROVIDER=custom
CUSTOM_API_URL=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions
CUSTOM_API_KEY=your-api-key
CUSTOM_API_MODEL=ERNIE-Bot-4
CUSTOM_REQUEST_FORMAT=openai
CUSTOM_RESPONSE_FORMAT=openai
```

### 示例3：完全自定义API

```bash
DEFAULT_AI_PROVIDER=custom
CUSTOM_API_URL=https://api.example.com/generate
CUSTOM_API_KEY=custom-key-123
CUSTOM_API_KEY_HEADER=X-API-Key
CUSTOM_API_KEY_PREFIX=
CUSTOM_REQUEST_FORMAT=custom
CUSTOM_REQUEST_TEMPLATE='{"input": "{{messages}}", "config": {"max_len": {{max_tokens}}}}'
CUSTOM_RESPONSE_FORMAT=custom
CUSTOM_RESPONSE_CONTENT_PATH=output.text
CUSTOM_RESPONSE_MODEL_PATH=model_info.name
CUSTOM_RESPONSE_USAGE_PATH=usage_stats
```

### 示例4：本地部署的模型

```bash
DEFAULT_AI_PROVIDER=custom
CUSTOM_API_URL=http://localhost:8000/v1/chat/completions
CUSTOM_API_KEY=local-key
CUSTOM_API_MODEL=local-model
CUSTOM_REQUEST_FORMAT=openai
CUSTOM_RESPONSE_FORMAT=openai
```

## 故障排查

### 常见问题

1. **连接错误**
   - 检查API URL是否正确
   - 确认网络连接正常
   - 验证是否需要代理

2. **认证失败**
   - 检查API密钥是否正确
   - 确认认证头配置正确
   - 验证密钥是否过期

3. **格式错误**
   - 确认请求格式与API要求匹配
   - 检查响应解析路径是否正确
   - 查看日志了解详细错误

### 调试技巧

1. **启用详细日志**
   ```bash
   LOG_LEVEL=DEBUG
   LOG_AI_REQUESTS=true
   ```

2. **使用测试脚本**
   ```bash
   python test_custom_api.py
   ```

3. **手动测试API**
   ```bash
   curl -X POST https://your-api.com/v1/chat/completions \
     -H "Authorization: Bearer your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"model": "your-model", "messages": [{"role": "user", "content": "Hello"}]}'
   ```

## API要求

### OpenAI兼容模式

如果使用`openai`格式，您的API应该：

**请求格式：**
```json
{
  "model": "model-name",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**响应格式：**
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "响应内容"
    },
    "finish_reason": "stop"
  }],
  "model": "model-name",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### 自定义格式

您可以定义任何格式，只需正确配置请求模板和响应路径。

## 性能优化

1. **设置合理的超时时间**
   ```bash
   CUSTOM_API_TIMEOUT=60  # 秒
   ```

2. **启用重试机制**
   ```bash
   CUSTOM_API_MAX_RETRIES=3
   ```

3. **使用连接池**
   - 系统自动管理连接池，无需额外配置

## 安全建议

1. **不要在代码中硬编码API密钥**
2. **使用环境变量或密钥管理服务**
3. **定期轮换API密钥**
4. **限制API密钥的权限范围**
5. **使用HTTPS确保传输安全**

## 扩展开发

如果需要更复杂的集成，可以继承`CustomAPIProvider`类：

```python
from landppt.ai.custom_provider import CustomAPIProvider

class MySpecialAPIProvider(CustomAPIProvider):
    def __init__(self, config):
        super().__init__(config)
        # 自定义初始化
    
    async def chat_completion(self, messages, **kwargs):
        # 自定义实现
        pass
```

## 获取帮助

如果遇到问题：

1. 查看[测试脚本](../test_custom_api.py)
2. 查看[示例配置](../.env.custom.example)
3. 提交Issue到项目仓库
4. 查看源代码：`src/landppt/ai/custom_provider.py`