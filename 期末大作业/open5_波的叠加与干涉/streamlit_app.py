# 开放应用题5A：波的叠加与干涉 - Streamlit交互网站

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

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

# 创建基于Streamlit的交互图像网站
def main():
    """
    创建基于Streamlit的交互图像网站
    """
    # 设置页面配置
    st.set_page_config(
        page_title="波的叠加与干涉 - 交互可视化",
        page_icon="🌊",
        layout="wide"
    )
    
    # 设置中文字体
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Noto Sans SC', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 页面标题
    st.title("波的叠加与干涉 - 交互可视化")
    st.write("---")
    
    # 选择可视化类型
    visualization_type = st.sidebar.selectbox(
        "选择可视化类型",
        ["波的叠加", "驻波", "二维波的干涉"]
    )
    
    st.sidebar.write("---")
    
    # 根据选择的可视化类型创建不同的控件
    if visualization_type == "波的叠加":
        st.subheader("波的叠加与干涉")
        
        # 创建参数控件
        col1, col2 = st.columns(2)
        
        with col1:
            f1 = st.slider("波1频率 (Hz)", min_value=0.1, max_value=5.0, step=0.1, value=1.0)
            f2 = st.slider("波2频率 (Hz)", min_value=0.1, max_value=5.0, step=0.1, value=1.0)
            A1 = st.slider("波1振幅", min_value=0.1, max_value=2.0, step=0.1, value=1.0)
            A2 = st.slider("波2振幅", min_value=0.1, max_value=2.0, step=0.1, value=1.0)
        
        with col2:
            phi1 = st.slider("波1相位 (rad)", min_value=0.0, max_value=2*np.pi, step=0.1, value=0.0)
            phi2 = st.slider("波2相位 (rad)", min_value=0.0, max_value=2*np.pi, step=0.1, value=0.0)
            t = st.slider("时间 (s)", min_value=0.0, max_value=2.0, step=0.05, value=0.0)
        
        # 计算波函数
        x = np.linspace(0, 4, 1000)
        wave1, wave2, superposed = wave_superposition(x, t, f1, f2, A1, A2, phi1, phi2)
        
        # 绘制图形
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
        st.pyplot(fig)
        
    elif visualization_type == "驻波":
        st.subheader("驻波可视化")
        
        # 创建参数控件
        col1, col2 = st.columns(2)
        
        with col1:
            f = st.slider("频率 (Hz)", min_value=0.1, max_value=3.0, step=0.1, value=1.0)
            A = st.slider("振幅", min_value=0.1, max_value=2.0, step=0.1, value=1.0)
        
        with col2:
            phi = st.slider("相位 (rad)", min_value=0.0, max_value=2*np.pi, step=0.1, value=0.0)
            t = st.slider("时间 (s)", min_value=0.0, max_value=2.0, step=0.05, value=0.0)
        
        # 计算驻波
        x = np.linspace(0, 4, 1000)
        wave = standing_wave(x, t, f, A, phi)
        
        # 绘制图形
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制驻波
        ax.plot(x, wave, 'purple', linewidth=2, label=f'驻波: f={f} Hz, A={A}, φ={phi:.2f} rad')
        
        # 绘制波节位置
        wave_nodes = np.linspace(0, 4, int(4 * f) + 1)
        ax.scatter(wave_nodes, np.zeros_like(wave_nodes), color='red', s=50, label='波节')
        
        # 设置坐标轴
        ax.set_xlabel('位置 x (m)')
        ax.set_ylabel('振幅')
        ax.set_title(f'驻波 (t={t:.2f} s)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_ylim(-2.5*A, 2.5*A)
        
        plt.tight_layout()
        st.pyplot(fig)
        
    elif visualization_type == "二维波的干涉":
        st.subheader("二维波的干涉图样")
        
        # 创建参数控件
        col1, col2 = st.columns(2)
        
        with col1:
            f1 = st.slider("波源1频率 (Hz)", min_value=0.1, max_value=3.0, step=0.1, value=1.0)
            f2 = st.slider("波源2频率 (Hz)", min_value=0.1, max_value=3.0, step=0.1, value=1.0)
            A1 = st.slider("波源1振幅", min_value=0.1, max_value=2.0, step=0.1, value=1.0)
            A2 = st.slider("波源2振幅", min_value=0.1, max_value=2.0, step=0.1, value=1.0)
        
        with col2:
            phi1 = st.slider("波源1相位 (rad)", min_value=0.0, max_value=2*np.pi, step=0.1, value=0.0)
            phi2 = st.slider("波源2相位 (rad)", min_value=0.0, max_value=2*np.pi, step=0.1, value=0.0)
            t = st.slider("时间 (s)", min_value=0.0, max_value=2.0, step=0.05, value=0.0)
        
        # 计算干涉强度
        x = np.linspace(0, 4, 200)
        y = np.linspace(0, 4, 200)
        X, Y = np.meshgrid(x, y)
        intensity = wave_interference(X, Y, t, f1, f2, A1, A2, phi1, phi2)
        
        # 绘制图形
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 绘制干涉图样
        contour = ax.contourf(X, Y, intensity, 100, cmap='jet')
        fig.colorbar(contour, ax=ax, label='干涉强度')
        
        # 标记波源位置
        ax.scatter([1.0, 3.0], [2.0, 2.0], color='white', s=100, label='波源')
        ax.scatter([1.0, 3.0], [2.0, 2.0], color='black', s=20)
        
        # 设置坐标轴
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title(f'二维波的干涉图样 (t={t:.2f} s)')
        ax.legend()
        ax.axis('equal')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # 添加物理原理说明
    st.write("---")
    st.subheader("物理原理说明")
    
    if visualization_type == "波的叠加":
        st.write("""
        **波的叠加原理**：几列波在同一介质中传播时，在相遇区域内，任一质点的振动是各列波单独存在时在该点引起的振动的矢量和。
        
        **相长干涉**：两列波在某点同相位，振幅相加，强度增强。条件：相位差为 2π 的整数倍。
        
        **相消干涉**：两列波在某点反相位，振幅相减，强度减弱。条件：相位差为 π 的奇数倍。
        
        **拍现象**：当两列频率相近的波叠加时，会产生振幅随时间周期性变化的现象，称为拍。拍频等于两列波频率之差。
        """)
    
    elif visualization_type == "驻波":
        st.write("""
        **驻波**：由两列振幅相同、频率相同、传播方向相反的波叠加形成的波形。
        
        **波节**：振幅始终为零的位置，间隔为半个波长。
        
        **波腹**：振幅最大的位置，位于波节之间。
        
        **特点**：波形不移动，仅在原地振动；能量不传播，而是在波节和波腹之间来回传递。
        
        **应用**：弦乐器、管乐器、激光谐振腔等。
        """)
    
    elif visualization_type == "二维波的干涉":
        st.write("""
        **二维波的干涉**：两个相干波源发出的波在空间叠加形成的现象。
        
        **干涉条纹**：形成明暗相间的条纹，明条纹对应相长干涉，暗条纹对应相消干涉。
        
        **明条纹条件**：到两个波源的距离差为波长的整数倍。
        
        **暗条纹条件**：到两个波源的距离差为半波长的奇数倍。
        
        **应用**：双缝干涉实验、薄膜干涉、全息摄影等。
        """)

if __name__ == "__main__":
    main()