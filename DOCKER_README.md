# Docker 部署說明 — coda-backend

## 快速啟動

### 方法一：docker-compose（推薦）

```bash
# 建置並啟動
docker-compose up --build

# 背景執行
docker-compose up --build -d

# 停止
docker-compose down
```

### 方法二：手動 build + run

```bash
# 建置 image
docker build -t coda-backend .

# 執行容器（讀取 .env 環境變數）
docker run -p 8000:8000 --env-file .env coda-backend
```

## 確認服務正常

```bash
# 查看容器狀態
docker-compose ps

# 查看 logs
docker-compose logs -f

# 測試 API
curl http://localhost:8000/
```

## 環境變數設定

請確保 `.env` 檔案存在於專案根目錄，需包含：

```env
MONGODB_URL=mongodb+srv://...
SECRET_KEY=your_secret_key_here
```

> ⚠️ `.env` 已加入 `.dockerignore`，不會被打包進 image，請妥善保管。

## 架構說明

- **Base image**：`python:3.11-slim`（多階段建置，image 更小）
- **Port**：8000
- **執行身份**：非 root user（appuser）
- **資料庫**：MongoDB Atlas（外部連線，無需本地 DB 容器）
- **Health Check**：每 30 秒確認 `GET /` 是否正常回應
