#!/bin/bash

# 取得腳本所在目錄
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

VENV_DIR=".venv"

# 檢查是否有虛擬環境
if [ ! -d "$VENV_DIR" ]; then
    echo "正在建立 Python 虛擬環境..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    echo "正在安裝依賴套件..."
    pip install -r requirements.txt
else
    source "$VENV_DIR/bin/activate"
fi

echo "啟動應用程式..."
python main.py "$@"
