import argparse
import numpy as np
import sounddevice as sd
import sys
import math

class AudioDelayLoopback:
    def __init__(self, delay, rate, channels, device_in=None, device_out=None):
        self.delay = delay
        self.rate = rate
        self.channels = channels
        self.device_in = device_in
        self.device_out = device_out
        
        # 計算 Buffer 大小
        self.delay_samples = int(self.delay * self.rate)
        # 初始化 Buffer
        self.buffer = np.zeros((self.delay_samples, self.channels), dtype='float32')
        self.write_idx = 0
        self.stream = None

    def callback(self, indata, outdata, frames, time, status):
        """音訊處理回呼函式"""
        if status:
            print(f"Stream Status: {status}", file=sys.stderr)

        # 簡單的視覺回饋 (計算音量 RMS，若有聲音則印出標記)
        # 為了避免 console 刷太快，我們可以只在特定條件下印出，或者簡單地：
        # volume = np.linalg.norm(indata) * 10
        # if volume > 1.0:
        #     sys.stdout.write('.')
        #     sys.stdout.flush()

        remaining_space = self.buffer.shape[0] - self.write_idx

        if frames <= remaining_space:
            # 情況 1: 直接寫入與讀取
            outdata[:] = self.buffer[self.write_idx : self.write_idx + frames]
            self.buffer[self.write_idx : self.write_idx + frames] = indata
            self.write_idx += frames
        else:
            # 情況 2: 跨越邊界 (Wrap around)
            part1_len = remaining_space
            outdata[:part1_len] = self.buffer[self.write_idx:]
            self.buffer[self.write_idx:] = indata[:part1_len]
            
            part2_len = frames - part1_len
            outdata[part1_len:] = self.buffer[:part2_len]
            self.buffer[:part2_len] = indata[part1_len:]
            
            self.write_idx = part2_len

        if self.write_idx >= self.buffer.shape[0]:
            self.write_idx = 0

    def start(self):
        print(f"=== Audio Delay Loopback 啟動 ===")
        print(f"  延遲: {self.delay} 秒")
        print(f"  格式: {self.rate} Hz, {self.channels} 聲道")
        
        device_info_in = sd.query_devices(self.device_in, 'input') if self.device_in is not None else "Default"
        device_info_out = sd.query_devices(self.device_out, 'output') if self.device_out is not None else "Default"
        
        print(f"  輸入裝置: {self.device_in if self.device_in is not None else '系統預設'} ({device_info_in['name'] if isinstance(device_info_in, dict) else device_info_in})")
        print(f"  輸出裝置: {self.device_out if self.device_out is not None else '系統預設'} ({device_info_out['name'] if isinstance(device_info_out, dict) else device_info_out})")
        print(f"-----------------------------------")
        print(f"正在運作中... (按 Ctrl+C 停止)")
        print(f"提示: 對著麥克風說話，{self.delay} 秒後會聽到回音。")

        try:
            with sd.Stream(samplerate=self.rate, 
                           channels=self.channels, 
                           device=(self.device_in, self.device_out),
                           callback=self.callback, 
                           dtype='float32', 
                           latency='low'):
                while True:
                    sd.sleep(1000)
        except KeyboardInterrupt:
            print("\n\n使用者停止程式。")
        except Exception as e:
            print(f"\n[錯誤] 無法啟動音訊串流: {e}")
            print("建議: 使用 --list 檢查裝置 ID，並確認麥克風權限已開啟。")

def list_devices():
    print("=== 可用音訊裝置列表 ===")
    print(sd.query_devices())
    print("\n提示: 請使用裝置列表左側的 '數字 ID' 搭配 -i 或 -o 參數。")
    print("範例: python main.py -i 1 -o 3")

def main():
    parser = argparse.ArgumentParser(description="Audio Delay Loopback (語音延遲回放工具)")
    parser.add_argument("-d", "--delay", type=float, default=3.0, help="延遲秒數 (預設: 3.0)")
    parser.add_argument("-r", "--rate", type=int, default=44100, help="取樣率 (預設: 44100)")
    parser.add_argument("-c", "--channels", type=int, default=1, help="聲道數 (建議: 1 為單聲道麥克風, 2 為立體聲)")
    
    # 新增裝置選擇參數
    parser.add_argument("-l", "--list", action="store_true", help="列出所有可用音訊裝置並離開")
    parser.add_argument("-i", "--input-device", type=int, help="輸入裝置 ID (麥克風)")
    parser.add_argument("-o", "--output-device", type=int, help="輸出裝置 ID (喇叭/耳機)")

    args = parser.parse_args()

    if args.list:
        list_devices()
        return

    # 建立並執行應用
    app = AudioDelayLoopback(
        delay=args.delay, 
        rate=args.rate, 
        channels=args.channels,
        device_in=args.input_device,
        device_out=args.output_device
    )
    app.start()

if __name__ == "__main__":
    main()
