# Audio Delay Loopback (語音延遲回放)

這是一個簡單的工具，可以「監聽」麥克風的聲音，並在設定的延遲時間（預設 3 秒）後從喇叭播放出來。這對於語言學習（聽自己的發音）、測試回音消除或音響系統調試非常有用。

## 快速開始 (Linux)

只需執行專案目錄下的 `run.sh` 腳本：

```bash
./run.sh
```

若需列出音訊裝置：
```bash
./run.sh --list
```

## 手動安裝與執行

### 1. 安裝依賴
確保你有 Python 3.x。
```bash
pip install -r requirements.txt
```

### 2. 執行
```bash
python main.py
```

## 進階選項

| 參數 | 說明 | 範例 |
|------|------|------|
| `-d` | 設定延遲秒數 (預設 3.0) | `python main.py -d 5.5` |
| `-l` | 列出所有可用音訊裝置 | `python main.py -l` |
| `-i` | 指定輸入裝置 ID (麥克風) | `python main.py -i 1` |
| `-o` | 指定輸出裝置 ID (喇叭) | `python main.py -o 3` |
| `-c` | 設定聲道數 (預設 1) | `python main.py -c 2` |

**範例：使用裝置 ID 1 作為麥克風，ID 3 作為喇叭，延遲 1 秒：**
```bash
python main.py -i 1 -o 3 -d 1.0
```

## 常見問題

**Q: 執行後聽不到聲音？**
A: 請先確認喇叭音量。接著使用 `python main.py -l` 查看裝置列表，確認程式是否抓到正確的裝置。如果是筆電，有時候預設裝置會是 HDMI 輸出而非內建喇叭。

**Q: 聲音爆音或斷斷續續？**
A: 嘗試調整取樣率，例如加上 `-r 48000` 參數。

## 技術細節
- 使用 `sounddevice` 進行低延遲音訊存取 (PortAudio binding)。
- 使用 `numpy` 實作高效的環形緩衝區 (Ring Buffer)。