# 开放应用题5A：波的叠加与干涉 - 交互可视化

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 定义波的叠加函数
def wave_superposition(x, t, f1, f2, A1, A2, phi1, phi2):
    """
    计算两个正弦波的叠加
    
    参数:
    x: 空间坐标
    t: 时间
    f1, f2: 两个波的频率
    A1, A2: 两个波的振幅
    phi1, phi2: 两个波的初始相位
    
    返回:
    叠加后的波函数值
    """
    # 波数 k = 2π/λ，假设波长 λ = 1 m，所以 k = 2π
    k = 2 * np.pi
    
    # 单个波
    wave1 = A1 * np.sin(k*x - 2*np.pi*f1*t + phi1)
    wave2 = A2 * np.sin(k*x - 2*np.pi*f2*t + phi2)
    
    # 波的叠加
    superposed = wave1 + wave2
    
    return wave1, wave2, superposed

# 可视化函数
def plot_wave_superposition(f1=1.0, f2=1.0, A1=1.0, A2=1.0, phi1=0.0, phi2=0.0, t=0.0):
    """
    绘制波的叠加与干涉图样
    
    参数:
    f1, f2: 两个波的频率 (Hz)
    A1, A2: 两个波的振幅
    phi1, phi2: 两个波的初始相位 (rad)
    t: 时间 (s)
    """
    # 空间坐标
    x = np.linspace(0, 4, 1000)
    
    # 计算波函数
    wave1, wave2, superposed = wave_superposition(x, t, f1, f2, A1, A2, phi1, phi2)
    
    # 创建图形
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # 绘制单个波
    ax1.plot(x, wave1, 'b-', label=f'波1: f={f1} Hz, A={A1}, φ={phi1:.2f} rad', alpha=0.7)
    ax1.plot(x, wave2, 'r-', label=f'波2: f={f2} Hz, A={A2}, φ={phi2:.2f} rad', alpha=0.7)
    ax1.set_ylabel('振幅')
    ax1.set_title('单个波的波形')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 绘制叠加后的波
    ax2.plot(x, superposed, 'g-', label='叠加后的波', linewidth=2)
    ax2.set_xlabel('位置 x (m)')
    ax2.set_ylabel('振幅')
    ax2.set_title(f'波的叠加 (t={t:.2f} s)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # 设置坐标轴范围
    max_amplitude = max(A1, A2) * 2.5
    ax1.set_ylim(-max_amplitude, max_amplitude)
    ax2.set_ylim(-max_amplitude, max_amplitude)
    
    plt.tight_layout()
    plt.show()

# 创建交互控件
def interactive_wave_superposition():
    """
    创建波的叠加与干涉的交互可视化控件
    """
    interact(
        plot_wave_superposition,
        f1=FloatSlider(min=0.1, max=5.0, step=0.1, value=1.0, description='波1频率 (Hz)'),
        f2=FloatSlider(min=0.1, max=5.0, step=0.1, value=1.0, description='波2频率 (Hz)'),
        A1=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description='波1振幅'),
        A2=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description='波2振幅'),
        phi1=FloatSlider(min=0.0, max=2*np.pi, step=0.1, value=0.0, description='波1相位 (rad)'),
        phi2=FloatSlider(min=0.0, max=2*np.pi, step=0.1, value=0.0, description='波2相位 (rad)'),
        t=FloatSlider(min=0.0, max=2.0, step=0.05, value=0.0, description='时间 (s)')
    )

# 驻波可视化
def standing_wave(x, t, f, A, phi=0.0):
    """
    计算驻波
    
    参数:
    x: 空间坐标
    t: 时间
    f: 频率
    A: 振幅
    phi: 初始相位
    
    返回:
    驻波函数值
    """
    k = 2 * np.pi  # 波数
    omega = 2 * np.pi * f  # 角频率
    
    # 驻波公式：2A cos(ωt) sin(kx)
    standing = 2 * A * np.cos(omega * t + phi) * np.sin(k * x)
    
    return standing

# 绘制驻波
def plot_standing_wave(f=1.0, A=1.0, phi=0.0, t=0.0):
    """
    绘制驻波图样
    """
    x = np.linspace(0, 4, 1000)
    
    # 计算驻波
    wave = standing_wave(x, t, f, A, phi)
    
    # 创建图形
    plt.figure(figsize=(12, 6))
    
    # 绘制驻波
    plt.plot(x, wave, 'purple', linewidth=2, label=f'驻波: f={f} Hz, A={A}, φ={phi:.2f} rad')
    
    # 绘制波节位置
    wave_nodes = np.linspace(0, 4, int(4 * f) + 1)
    plt.scatter(wave_nodes, np.zeros_like(wave_nodes), color='red', s=50, label='波节')
    
    # 设置坐标轴
    plt.xlabel('位置 x (m)')
    plt.ylabel('振幅')
    plt.title(f'驻波 (t={t:.2f} s)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylim(-2.5*A, 2.5*A)
    
    plt.tight_layout()
    plt.show()

# 创建驻波交互控件
def interactive_standing_wave():
    """
    创建驻波的交互可视化控件
    """
    interact(
        plot_standing_wave,
        f=FloatSlider(min=0.1, max=3.0, step=0.1, value=1.0, description='频率 (Hz)'),
        A=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description='振幅'),
        phi=FloatSlider(min=0.0, max=2*np.pi, step=0.1, value=0.0, description='相位 (rad)'),
        t=FloatSlider(min=0.0, max=2.0, step=0.05, value=0.0, description='时间 (s)')
    )

# 波的干涉图样可视化
def wave_interference(x, y, t, f1, f2, A1, A2, phi1, phi2):
    """
    计算二维波的干涉图样
    
    参数:
    x, y: 二维空间坐标
    t: 时间
    f1, f2: 两个波源的频率
    A1, A2: 两个波源的振幅
    phi1, phi2: 两个波源的初始相位
    
    返回:
    干涉图样的强度
    """
    # 波源位置
    x1, y1 = 1.0, 2.0
    x2, y2 = 3.0, 2.0
    
    # 波数和角频率
    k = 2 * np.pi
    omega1 = 2 * np.pi * f1
    omega2 = 2 * np.pi * f2
    
    # 计算到两个波源的距离
    r1 = np.sqrt((x - x1)**2 + (y - y1)**2)
    r2 = np.sqrt((x - x2)**2 + (y - y2)**2)
    
    # 计算两个波的相位
    phase1 = k * r1 - omega1 * t + phi1
    phase2 = k * r2 - omega2 * t + phi2
    
    # 计算两个波的振幅
    wave1 = A1 * np.sin(phase1)
    wave2 = A2 * np.sin(phase2)
    
    # 干涉强度（振幅的平方）
    intensity = (wave1 + wave2)**2
    
    return intensity

# 绘制波的干涉图样
def plot_wave_interference(f1=1.0, f2=1.0, A1=1.0, A2=1.0, phi1=0.0, phi2=0.0, t=0.0):
    """
    绘制二维波的干涉图样
    """
    # 二维网格
    x = np.linspace(0, 4, 200)
    y = np.linspace(0, 4, 200)
    X, Y = np.meshgrid(x, y)
    
    # 计算干涉强度
    intensity = wave_interference(X, Y, t, f1, f2, A1, A2, phi1, phi2)
    
    # 创建图形
    plt.figure(figsize=(10, 8))
    
    # 绘制干涉图样
    contour = plt.contourf(X, Y, intensity, 100, cmap='jet')
    plt.colorbar(contour, label='干涉强度')
    
    # 标记波源位置
    plt.scatter([1.0, 3.0], [2.0, 2.0], color='white', s=100, label='波源')
    plt.scatter([1.0, 3.0], [2.0, 2.0], color='black', s=20)
    
    # 设置坐标轴
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title(f'二维波的干涉图样 (t={t:.2f} s)')
    plt.legend()
    plt.axis('equal')
    
    plt.tight_layout()
    plt.show()

# 创建波的干涉交互控件
def interactive_wave_interference():
    """
    创建二维波的干涉图样交互可视化控件
    """
    interact(
        plot_wave_interference,
        f1=FloatSlider(min=0.1, max=3.0, step=0.1, value=1.0, description='波源1频率 (Hz)'),
        f2=FloatSlider(min=0.1, max=3.0, step=0.1, value=1.0, description='波源2频率 (Hz)'),
        A1=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description='波源1振幅'),
        A2=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description='波源2振幅'),
        phi1=FloatSlider(min=0.0, max=2*np.pi, step=0.1, value=0.0, description='波源1相位 (rad)'),
        phi2=FloatSlider(min=0.0, max=2*np.pi, step=0.1, value=0.0, description='波源2相位 (rad)'),
        t=FloatSlider(min=0.0, max=2.0, step=0.05, value=0.0, description='时间 (s)')
    )

# 主函数
def main():
    """
    主函数，运行波的叠加与干涉交互可视化
    """
    print("波的叠加与干涉交互可视化")
    print("=" * 40)
    print("1. 波的叠加")
    print("2. 驻波")
    print("3. 二维波的干涉")
    print("=" * 40)
    
    # 运行所有交互控件
    print("\n=== 波的叠加 ===")
    interactive_wave_superposition()
    
    print("\n=== 驻波 ===")
    interactive_standing_wave()
    
    print("\n=== 二维波的干涉 ===")
    interactive_wave_interference()

if __name__ == "__main__":
    main()