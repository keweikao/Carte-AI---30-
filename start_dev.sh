#!/bin/bash

# OderWhat 開發環境快速啟動腳本
# 使用方法: ./start_dev.sh [backend|frontend|both]

set -e

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 專案根目錄
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 顯示說明
show_help() {
    echo -e "${BLUE}OderWhat 開發環境啟動腳本${NC}"
    echo ""
    echo "使用方法:"
    echo "  ./start_dev.sh [backend|frontend|both]"
    echo ""
    echo "選項:"
    echo "  backend   - 只啟動後端服務器 (FastAPI)"
    echo "  frontend  - 只啟動前端服務器 (Next.js)"
    echo "  both      - 同時啟動前端和後端 (預設)"
    echo "  help      - 顯示此說明"
    echo ""
}

# 檢查虛擬環境
check_venv() {
    if [ ! -d "$PROJECT_ROOT/venv" ]; then
        echo -e "${YELLOW}⚠️  未找到 Python 虛擬環境${NC}"
        echo -e "${BLUE}正在建立虛擬環境...${NC}"
        python3 -m venv "$PROJECT_ROOT/venv"
        echo -e "${GREEN}✅ 虛擬環境建立完成${NC}"

        echo -e "${BLUE}正在安裝 Python 依賴套件...${NC}"
        "$PROJECT_ROOT/venv/bin/pip" install -r "$PROJECT_ROOT/requirements.txt"
        echo -e "${GREEN}✅ Python 依賴套件安裝完成${NC}"
    fi
}

# 檢查前端依賴
check_frontend_deps() {
    if [ ! -d "$PROJECT_ROOT/frontend/node_modules" ]; then
        echo -e "${YELLOW}⚠️  未找到前端依賴${NC}"
        echo -e "${BLUE}正在安裝前端依賴套件...${NC}"
        cd "$PROJECT_ROOT/frontend"
        npm install
        echo -e "${GREEN}✅ 前端依賴套件安裝完成${NC}"
        cd "$PROJECT_ROOT"
    fi
}

# 檢查環境變數
check_env() {
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        echo -e "${YELLOW}⚠️  未找到 .env 檔案${NC}"
        echo -e "${BLUE}請根據 .env.example 建立 .env 檔案${NC}"
        exit 1
    fi

    if [ ! -f "$PROJECT_ROOT/frontend/.env.local" ]; then
        echo -e "${YELLOW}⚠️  未找到 frontend/.env.local 檔案${NC}"
        echo -e "${BLUE}請根據 frontend/.env.example 建立 frontend/.env.local 檔案${NC}"
        exit 1
    fi
}

# 啟動後端
start_backend() {
    echo -e "${GREEN}🚀 啟動後端服務器...${NC}"
    echo -e "${BLUE}後端服務器將運行在 http://localhost:8000${NC}"
    echo -e "${BLUE}API 文檔: http://localhost:8000/docs${NC}"
    echo ""

    cd "$PROJECT_ROOT"
    source venv/bin/activate
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# 啟動前端
start_frontend() {
    echo -e "${GREEN}🚀 啟動前端服務器...${NC}"
    echo -e "${BLUE}前端應用將運行在 http://localhost:3000${NC}"
    echo ""

    cd "$PROJECT_ROOT/frontend"
    npm run dev
}

# 同時啟動前端和後端
start_both() {
    echo -e "${GREEN}🚀 同時啟動前端和後端服務器...${NC}"
    echo -e "${BLUE}後端: http://localhost:8000${NC}"
    echo -e "${BLUE}前端: http://localhost:3000${NC}"
    echo ""
    echo -e "${YELLOW}提示: 按 Ctrl+C 停止所有服務器${NC}"
    echo ""

    # 啟動後端在背景
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!

    # 等待後端啟動
    sleep 3

    # 啟動前端
    cd "$PROJECT_ROOT/frontend"
    npm run dev &
    FRONTEND_PID=$!

    # 處理 Ctrl+C
    trap "echo -e '\n${YELLOW}正在停止服務器...${NC}'; kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

    # 等待進程
    wait
}

# 主程式
main() {
    MODE="${1:-both}"

    case "$MODE" in
        help)
            show_help
            exit 0
            ;;
        backend)
            echo -e "${BLUE}=== OderWhat 開發環境 (後端) ===${NC}\n"
            check_venv
            check_env
            start_backend
            ;;
        frontend)
            echo -e "${BLUE}=== OderWhat 開發環境 (前端) ===${NC}\n"
            check_frontend_deps
            check_env
            start_frontend
            ;;
        both)
            echo -e "${BLUE}=== OderWhat 開發環境 (全端) ===${NC}\n"
            check_venv
            check_frontend_deps
            check_env
            start_both
            ;;
        *)
            echo -e "${RED}❌ 無效的選項: $MODE${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 執行主程式
main "$@"
