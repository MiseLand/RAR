import time
import win32api  # type: ignore
import win32con  # type: ignore
import ctypes
import ctypes.wintypes

# 加载Windows多媒体库
winmm = ctypes.WinDLL('winmm')

# 定义多媒体定时器函数原型，使用c_uint替代MMRESULT
winmm.timeBeginPeriod.argtypes = [ctypes.wintypes.UINT]
winmm.timeBeginPeriod.restype = ctypes.c_uint  # 修正此处的类型

winmm.timeEndPeriod.argtypes = [ctypes.wintypes.UINT]
winmm.timeEndPeriod.restype = ctypes.c_uint  # 修正此处的类型

# 设置高精度计时器
def enable_high_precision():
    winmm.timeBeginPeriod(1)  # 设置1ms分辨率

def disable_high_precision():
    winmm.timeEndPeriod(1)  # 恢复默认分辨率

# 高精度等待函数（使用Windows多媒体定时器）
def precise_wait(duration_ms):
    start = time.perf_counter()
    # 将毫秒转换为秒
    duration_sec = duration_ms / 1000.0
    while (time.perf_counter() - start) < duration_sec:
        pass  # 忙等待直到达到指定时间

# 执行完整操作序列
def execute_sequence():
    # 鼠标左键按下
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    precise_wait(7)  # 7ms
    
    # 鼠标左键抬起
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    precise_wait(7)  # 7ms
    
    # R键按下
    win32api.keybd_event(ord('R'), 0, 0, 0)
    precise_wait(1)  # 1ms
    
    # R键抬起
    win32api.keybd_event(ord('R'), 0, win32con.KEYEVENTF_KEYUP, 0)
    precise_wait(7)  # 7ms
    
    # 鼠标左键按下（第二次）
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    precise_wait(1)  # 7ms
    
    # 鼠标左键抬起（第二次）
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    precise_wait(1)  # 7ms
    
    # R键按下（第二次）
    win32api.keybd_event(ord('R'), 0, 0, 0)
    precise_wait(7)  # 7ms
    
    # R键抬起（第二次）
    win32api.keybd_event(ord('R'), 0, win32con.KEYEVENTF_KEYUP, 0)
    precise_wait(3) 

# 主函数
def main():
    try:
        # 启用高精度定时器
        enable_high_precision()
        print("Program started. Hold 'X' to activate the sequence. Press 'P' to exit.")
        
        sequence_active = False
        
        while True:
            # 检查P键是否按下（退出程序）
            if win32api.GetAsyncKeyState(ord('P')) < 0:
                print("Program exited by user.")
                break
            
            # 检查x键状态（仅在序列之间检查）
            if win32api.GetAsyncKeyState(ord('X')) < 0:
                if not sequence_active:
                    sequence_active = True
                # 执行完整序列（无中断检查）
                execute_sequence()
            else:
                sequence_active = False
                time.sleep(0.001)  # 极短等待降低CPU占用
    finally:
        # 确保恢复系统定时器设置
        disable_high_precision()
        print("High precision timer disabled.")

if __name__ == "__main__":
    main()
