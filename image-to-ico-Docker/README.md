# 高清图片转ICO工具 (Docker版)

一个简单易用的图片转ICO转换工具，支持单个文件转换和批量转换，可生成多种尺寸的图标文件。本项目已适配 Docker 部署，提供更便捷的安装和使用方式。

## 功能特性

- 🖼️ 支持常见图片格式转换（PNG, JPG, JPEG, BMP, GIF）
- 🎯 可选择多种输出尺寸（16x16 到 512x512）
- 📦 支持单个文件转换和批量转换
- 💾 自定义输出目录
- 🔍 高质量转换，使用 LANCZOS 算法
- 🌐 基于Web界面，使用方便
- ✨ 支持生成多尺寸ICO文件
- 🐳 支持 Docker 部署，跨平台兼容

## 系统要求

- Docker Desktop (Windows/MacOS) 或 Docker Engine (Linux)
- 2GB 以上可用内存
- 1GB 以上可用磁盘空间

## 快速开始

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/image-to-ico.git
cd image-to-ico
```

2. 使用 docker-compose 启动服务：
```bash
docker-compose up -d
```

3. 访问Web界面：
   - 打开浏览器访问：http://localhost:7860

就是这么简单！🎉

## 使用说明

### 单个文件转换

1. 打开Web界面 (http://localhost:7860)
2. 选择"单个文件转换"标签页
3. 点击"上传图片"选择要转换的图片文件
4. 选择需要的图标尺寸（可多选）
5. 可选：指定输出目录
6. 点击"转换"按钮
7. 转换完成后可直接下载或到输出目录查看文件

### 批量转换

1. 打开Web界面 (http://localhost:7860)
2. 选择"批量转换"标签页
3. 在输入框中填写包含图片的文件夹路径
4. 选择需要的图标尺寸（可多选）
5. 可选：指定输出目录
6. 点击"开始批量转换"按钮
7. 等待转换完成，查看输出目录中的转换结果

## 支持的格式

### 输入格式
- PNG
- JPG/JPEG
- BMP
- GIF

### 输出格式
- ICO（Windows图标文件）

## 容器管理

### 常用命令
```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 重建镜像
docker-compose build --no-cache
```

### 自定义端口
如需修改默认端口(7860)，请编辑 `docker-compose.yml` 文件：
```yaml
ports:
  - "新端口:7860"
```

## 注意事项

1. 文件权限
   - 确保 output 目录具有适当的读写权限
   - Docker 运行时会自动创建必要的目录

2. 性能优化
   - 建议上传方形图片以获得最佳效果
   - 批量转换时，建议图片数量不超过100张

3. 安全建议
   - 建议在内网环境使用
   - 如需外网访问，请配置适当的安全措施

4. 常见问题
   - 如果网页无法访问，请检查防火墙设置
   - 如果转换失败，请检查图片格式和尺寸是否符合要求

## 更新维护

### 更新步骤
1. 拉取最新代码：
```bash
git pull
```

2. 重新构建并启动：
```bash
docker-compose up -d --build
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件