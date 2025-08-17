import time
import vgamepad
import pygame
import ctypes
import ctypes.wintypes

# 加载Windows多媒体库
winmm = ctypes.WinDLL('winmm')

# 定义多媒体定时器函数原型
winmm.timeBeginPeriod.argtypes = [ctypes.wintypes.UINT]
winmm.timeBeginPeriod.restype = ctypes.c_uint
winmm.timeEndPeriod.argtypes = [ctypes.wintypes.UINT]
winmm.timeEndPeriod.restype = ctypes.c_uint

# 设置高精度计时器
def enable_high_precision():
    winmm.timeBeginPeriod(1)  # 设置1ms分辨率

def disable_high_precision():
    winmm.timeEndPeriod(1)  # 恢复默认分辨率

# 高精度等待函数
def precise_wait(duration_ms):
    start = time.perf_counter()
    duration_sec = duration_ms / 1000.0
    while (time.perf_counter() - start) < duration_sec:
        pass

# 定义手柄按键常量
UP = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
DOWN = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
LEFT = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
RIGHT = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT

START = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START
BACK = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK
GUIDE = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

LEFT_THUMB = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
RIGHT_THUMB = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
LEFT_SHOULDER = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
RIGHT_SHOULDER = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER

A = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A
B = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B
X = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X
Y = vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y

# 执行手柄操作序列
def execute_sequence(gamepad):
    # 右肩键按下 (对应鼠标左键)
    gamepad.press_button(RIGHT_SHOULDER)
    gamepad.update()
    precise_wait(7)
    
    # 右肩键抬起
    gamepad.release_button(RIGHT_SHOULDER)
    gamepad.update()
    precise_wait(7)
    
    # 左扳机按下 (对应R键)
    gamepad.left_trigger(255)  # 255表示完全按下
    gamepad.update()
    # precise_wait(1)
    
    # 左扳机抬起
    # gamepad.left_trigger(0)
    # gamepad.update()
    precise_wait(7)
    
    # 右肩键再次按下
    gamepad.press_button(RIGHT_SHOULDER)
    gamepad.update()
    precise_wait(1)
    
    # 右肩键再次抬起
    gamepad.release_button(RIGHT_SHOULDER)
    gamepad.update()
    precise_wait(2)
    
    # 左扳机再次按下
    # gamepad.left_trigger(255)
    # gamepad.update()
    # precise_wait(7)
    
    # 左扳机再次抬起
    gamepad.left_trigger(0)
    gamepad.update()
    precise_wait(1)

def main():
    # 初始化pygame用于读取真实手柄
    pygame.init()
    pygame.joystick.init()
    
    # 尝试连接真实手柄
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Detected joystick: {joystick.get_name()}")
    except pygame.error:
        print("No joystick found.")
        return
    
    # 创建虚拟手柄
    gamepad = vgamepad.VX360Gamepad()
    
    # 启用高精度定时器
    enable_high_precision()
    print("Program started. Press LEFT THUMB (左摇杆按下) to toggle sequence loop. Press RIGHT THUMB (右摇杆按下) to exit.")
    
    # 开关状态变量
    sequence_active = False
    left_thumb_prev_state = False
    running = True
    
    try:
        while running:
            # 处理pygame事件
            pygame.event.pump()
            
            # 获取左摇杆按下状态
            current_left_thumb = joystick.get_button(8)  # 左摇杆按下（左摇杆序号8）
            
            # 检测左摇杆按下事件（切换开关）
            if current_left_thumb and not left_thumb_prev_state:
                sequence_active = not sequence_active
                print(f"Sequence loop {'ENABLED' if sequence_active else 'DISABLED'}")
            
            # 更新左摇杆状态
            left_thumb_prev_state = current_left_thumb
            
            # 获取右摇杆按下状态
            current_right_thumb = joystick.get_button(9)  # 右摇杆按下（右摇杆序号9）
            
            # 检测右摇杆按下事件（退出程序）
            if current_right_thumb:
                print("Exiting program...")
                running = False
            
            # 如果序列激活，执行操作
            if sequence_active:
                execute_sequence(gamepad)
            
            # 短暂休眠以降低CPU使用率
            time.sleep(0.001)
    
    finally:
        # 确保恢复系统定时器设置
        disable_high_precision()
        pygame.quit()
        print("High precision timer disabled. Program exited.")

if __name__ == "__main__":
    main()