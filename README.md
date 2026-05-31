# Coda Backend

> 演唱會票務平台 **CODA** 的後端服務 — FastAPI + MongoDB
> User authentication backend (JWT) for a concert-ticketing platform. Containerized with Docker.

前端 Demo：https://coda-henna.vercel.app ・ 前端原始碼：https://github.com/henryliu3033-afk/coda

---

## 解決什麼問題

CODA 前端是演唱會票務平台，需要會員系統才能綁定「誰買了哪張票」。這個後端提供註冊、登入與「取得當前使用者」的受保護端點，採無狀態 JWT 驗證，並用 Docker 容器化方便部署。

## 技術選型

| 選擇 | 為什麼 |
|------|--------|
| **FastAPI** | 內建驗證、自動 Swagger 文件、async。 |
| **MongoDB（motor）** | 使用者文件結構單純、欄位彈性，文件型資料庫起步快；`motor` 提供非同步存取，搭配 FastAPI 的 async 不阻塞。 |
| **JWT（python-jose）** | 無狀態驗證，後端免存 session。 |
| **bcrypt** | 密碼雜湊，自帶 salt。 |
| **Docker** | `Dockerfile` + `docker-compose.yml`，一鍵起後端與資料庫，環境一致。 |

## 架構

```
FastAPI ── routers/user.py   註冊 / 登入 / 取得當前使用者
        ├─ auth.py           JWT 簽發、get_current_user 依賴注入
        ├─ models.py         Pydantic 模型（含 EmailStr 驗證）
        └─ database.py       MongoDB（motor 非同步）連線
```

`get_current_user` 是一個 FastAPI **依賴（Depends）**，任何需要登入的端點掛上它即可自動驗證 token、取出使用者，邏輯不重複。

## API 端點

| Method | Path | 說明 | 需登入 |
|--------|------|------|:--:|
| POST | `/api/user/register` | 註冊 | – |
| POST | `/api/user/login` | 登入，回傳 JWT | – |
| GET | `/api/user/me` | 取得當前登入使用者 | ✅ |

互動式文件：啟動後 `http://localhost:8000/docs`。

## 本機啟動

```bash
pip install -r requirements.txt
cp .env.example .env          # 填入 MONGODB_URL、SECRET_KEY
uvicorn main:app --reload
```

或用 Docker：

```bash
docker compose up --build
```

## 環境變數

| 變數 | 說明 |
|------|------|
| `MONGODB_URL` | MongoDB 連線字串 |
| `SECRET_KEY` | JWT 密鑰（隨機 hex，勿寫死） |
| `ALLOWED_ORIGINS` | 允許的前端來源，逗號分隔 |

`.env` 已列入 `.gitignore`；請參考 `.env.example`。

## 測試

以 pytest + **mongomock_motor** 撰寫整合測試（模擬 MongoDB，免真實資料庫即可執行）：

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q          # 8 個測試
```

覆蓋：註冊／重複 email／email 格式驗證、登入成功與失敗、`/me` 受保護端點需登入、JWT 驗證。

---

## 面試可能會被問

**Q：為什麼 CODA 用 MongoDB，PULSE 用 PostgreSQL？**
看資料形狀。CODA 這版只有使用者文件、沒有複雜關聯，MongoDB 彈性、起步快；PULSE 有「使用者—書籤」一對多關聯與一致性需求，關聯式資料庫較合適。我刻意用兩種來理解各自的取捨。

**Q：`get_current_user` 怎麼運作？**
它是 FastAPI 的 Depends。端點宣告 `payload = Depends(get_current_user)`，框架會先跑它：從 `Authorization` header 取 token、`jwt.decode` 驗證，失敗丟 401，成功把 payload 注入端點。好處是驗證邏輯集中一處、可重用。

**Q：bcrypt 為什麼安全？**
它每次雜湊都加隨機 salt，相同密碼也會得到不同雜湊，讓彩虹表失效；而且刻意慢，增加暴力破解成本。

## 已知可改進
- 已有 pytest 整合測試（8 個，mongomock）；可再補 token 過期等邊界案例。
- token 過期時間（目前 7 天）可縮短並搭配 refresh token。
