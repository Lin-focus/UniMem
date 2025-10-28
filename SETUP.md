# UniMem AI 设置指南

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
创建 `.env` 文件并配置以下**必需**变量：

```bash
# NVIDIA API 配置（必需）
NVIDIA_API_KEY=your_actual_nvidia_api_key

# AWS 配置（必需）
AWS_ACCESS_KEY_ID=your_actual_aws_access_key
AWS_SECRET_ACCESS_KEY=your_actual_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-actual-s3-bucket-name

# 环境设置
ENVIRONMENT=development

# 生产环境 NIM 配置（可选）
# NIM_EMBEDDING_URL=http://your-nim-service:8000/v1
```

### 3. 检查配置
```bash
python check_config.py
```

### 4. 启动服务器
```bash
python main.py
```

### 5. 测试API
```bash
python test_api.py
```

## ⚠️ 重要说明

**系统不再支持模拟模式**，所有服务都需要真实配置：

- **Embedding**: 必须配置NVIDIA API密钥
- **存储**: 必须配置AWS DynamoDB和S3
- **功能**: 需要所有环境变量正确配置才能运行

## 📖 API文档

启动后访问：http://localhost:8000/docs

## 🧪 测试功能

1. **健康检查**: `GET /health`
2. **上传文本**: `POST /api/upload/text`
3. **语义搜索**: `POST /api/search/semantic`
4. **AI对话**: `POST /api/agent/chat`
5. **记忆列表**: `GET /api/search/memories`

## 🔑 获取API密钥

### NVIDIA API密钥
1. 访问 [NVIDIA Developer](https://developer.nvidia.com/)
2. 注册账户并获取API密钥
3. 将密钥添加到 `.env` 文件

### AWS配置
1. 创建AWS账户
2. 创建S3存储桶
3. 创建DynamoDB表（系统会自动创建）
4. 获取访问密钥并添加到 `.env` 文件

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   - 检查 `.env` 文件中的密钥是否正确
   - 系统会自动切换到模拟模式

2. **AWS连接失败**
   - 检查AWS凭证和区域设置
   - 系统会自动切换到内存存储模式

3. **端口被占用**
   - 修改 `main.py` 中的端口号
   - 或停止占用8000端口的其他服务

### 日志信息
- `✅` 成功操作
- `⚠️` 警告（自动降级到模拟模式）
- `❌` 错误
- `🔧` 模拟模式操作

## 📝 注意事项

- 开发模式下数据存储在内存中，重启后会丢失
- 生产模式需要正确配置AWS和NVIDIA服务
- 建议先在开发模式下测试功能
