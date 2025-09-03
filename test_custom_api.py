#!/usr/bin/env python3
"""
测试自定义API集成的脚本

使用方法：
1. 复制 .env.custom.example 为 .env
2. 在 .env 中配置您的自定义API信息
3. 运行此脚本：python test_custom_api.py
"""

import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from landppt.ai import AIProviderFactory, AIMessage, MessageRole
from landppt.core.config import ai_config


async def test_custom_api():
    """测试自定义API功能"""
    
    print("=" * 60)
    print("自定义API集成测试")
    print("=" * 60)
    
    # 检查配置
    if not ai_config.is_provider_available("custom"):
        print("\n❌ 错误：自定义API未配置")
        print("\n请按以下步骤配置：")
        print("1. 复制 .env.custom.example 为 .env")
        print("2. 编辑 .env 文件，填入您的API信息：")
        print("   - CUSTOM_API_URL: 您的API端点")
        print("   - CUSTOM_API_KEY: 您的API密钥")
        print("3. 重新运行此脚本")
        return
    
    # 获取配置信息
    config = ai_config.get_provider_config("custom")
    print("\n✅ 自定义API已配置")
    print(f"API URL: {config.get('api_url')}")
    print(f"Model: {config.get('model')}")
    print(f"Request Format: {config.get('request_format')}")
    print(f"Response Format: {config.get('response_format')}")
    
    try:
        # 创建自定义API provider
        provider = AIProviderFactory.create_provider("custom")
        print("\n✅ Provider创建成功")
        
        # 准备测试消息
        messages = [
            AIMessage(
                role=MessageRole.SYSTEM,
                content="你是一个友好的助手"
            ),
            AIMessage(
                role=MessageRole.USER,
                content="请用一句话介绍你自己"
            )
        ]
        
        print("\n正在调用API...")
        print("-" * 40)
        
        # 调用API
        response = await provider.chat_completion(messages)
        
        print("\n✅ API调用成功！")
        print("\n响应内容：")
        print("-" * 40)
        print(response.content)
        print("-" * 40)
        
        print("\n响应元数据：")
        print(f"Model: {response.model}")
        print(f"Usage: {response.usage}")
        if response.finish_reason:
            print(f"Finish Reason: {response.finish_reason}")
        
        # 测试流式响应
        print("\n测试流式响应...")
        print("-" * 40)
        
        messages.append(AIMessage(
            role=MessageRole.USER,
            content="请说'Hello World'"
        ))
        
        async for chunk in provider.stream_chat_completion(messages):
            print(chunk, end="", flush=True)
        print("\n" + "-" * 40)
        
        print("\n✅ 所有测试通过！")
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n可能的原因：")
        print("1. API URL不正确")
        print("2. API密钥无效")
        print("3. 请求/响应格式不匹配")
        print("4. 网络连接问题")
        print("\n请检查您的配置并重试")


async def test_multiple_formats():
    """测试不同的请求/响应格式"""
    
    print("\n" + "=" * 60)
    print("测试不同的API格式")
    print("=" * 60)
    
    # 示例：自定义请求格式
    custom_config = {
        "api_url": "https://api.example.com/generate",
        "api_key": "test-key",
        "model": "custom-model",
        "request_format": "custom",
        "response_format": "custom",
        "custom_request_template": {
            "prompt": "{{messages}}",
            "config": {
                "max_tokens": "{{max_tokens}}",
                "temperature": "{{temperature}}"
            }
        },
        "response_content_path": "data.text",
        "response_model_path": "meta.model",
        "response_usage_path": "stats"
    }
    
    print("\n自定义格式配置示例：")
    print("-" * 40)
    print(f"请求模板：{custom_config['custom_request_template']}")
    print(f"响应内容路径：{custom_config['response_content_path']}")
    print(f"响应模型路径：{custom_config['response_model_path']}")
    print(f"响应使用路径：{custom_config['response_usage_path']}")
    
    print("\n这种配置适用于不兼容OpenAI格式的API")


def print_integration_guide():
    """打印集成指南"""
    
    print("\n" + "=" * 60)
    print("自定义API集成指南")
    print("=" * 60)
    
    print("\n## 支持的API类型")
    print("-" * 40)
    print("1. OpenAI兼容API（推荐）")
    print("   - 通义千问 (Qwen)")
    print("   - 文心一言 (ERNIE)")
    print("   - ChatGLM")
    print("   - 任何兼容OpenAI格式的API")
    
    print("\n2. 完全自定义API")
    print("   - 自建模型服务")
    print("   - 私有API")
    print("   - 特殊格式的API")
    
    print("\n## 配置步骤")
    print("-" * 40)
    print("1. 设置环境变量")
    print("   export CUSTOM_API_URL=https://your-api.com/v1/chat")
    print("   export CUSTOM_API_KEY=your-api-key")
    
    print("\n2. 或使用.env文件")
    print("   CUSTOM_API_URL=https://your-api.com/v1/chat")
    print("   CUSTOM_API_KEY=your-api-key")
    
    print("\n3. 在代码中使用")
    print("   provider = get_ai_provider('custom')")
    print("   response = await provider.chat_completion(messages)")
    
    print("\n## 高级配置")
    print("-" * 40)
    print("- 自定义认证头：CUSTOM_API_KEY_HEADER")
    print("- 自定义请求格式：CUSTOM_REQUEST_FORMAT")
    print("- 自定义响应解析：CUSTOM_RESPONSE_FORMAT")
    print("- 请求模板：CUSTOM_REQUEST_TEMPLATE")
    
    print("\n## 故障排查")
    print("-" * 40)
    print("1. 检查API URL是否正确")
    print("2. 验证API密钥是否有效")
    print("3. 确认请求/响应格式匹配")
    print("4. 查看日志了解详细错误")
    print("5. 使用curl或Postman测试API")


if __name__ == "__main__":
    print("\n🚀 LandPPT 自定义API集成测试工具\n")
    
    # 打印集成指南
    print_integration_guide()
    
    # 运行测试
    try:
        asyncio.run(test_custom_api())
        asyncio.run(test_multiple_formats())
    except KeyboardInterrupt:
        print("\n\n测试中断")
    except Exception as e:
        print(f"\n错误：{e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)