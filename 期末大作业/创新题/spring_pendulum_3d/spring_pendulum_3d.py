# spring_pendulum_3d.py - 3D弹簧-单摆耦合系统模拟

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk

# 设置Matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class SpringPendulum3D:
    def __init__(self, M=1.0, m=0.5, k=1.0, l=1.0, x0=1.0, theta0=np.pi/4, phi0=0.0):
        """
        初始化3D弹簧-单摆耦合系统
        M: 滑块质量
        m: 单摆小球质量
        k: 弹簧刚度
        l: 单摆长度
        x0: 滑块初始位移
        theta0: 单摆初始极角
        phi0: 单摆初始方位角
        """
        self.M = M
        self.m = m
        self.k = k
        self.l = l
        self.x = x0
        self.theta = theta0
        self.phi = phi0
        self.g = 9.8  # 重力加速度
    
    def get_pendulum_position(self):
        """
        计算小球位置
        """
        pendulum_x = self.x + self.l * np.sin(self.theta) * np.cos(self.phi)
        pendulum_y = self.l * np.sin(self.theta) * np.sin(self.phi)
        pendulum_z = -self.l * np.cos(self.theta)
        return pendulum_x, pendulum_y, pendulum_z

def create_interactive_3d_model():
    """
    创建3D交互模型，包含可调整的参数控件
    """
    # 初始化系统
    spring_pendulum = SpringPendulum3D()
    
    # 创建主窗口
    root = tk.Tk()
    root.title("3D弹簧-单摆耦合系统交互模型")
    root.geometry("1000x600")
    
    # 创建3D可视化框架
    viz_frame = ttk.LabelFrame(root, text="3D可视化")
    viz_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # 创建参数调整框架
    control_frame = ttk.LabelFrame(root, text="参数调整")
    control_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)
    
    # 创建控制容器，用于放置三个滑块
    control_container = ttk.Frame(control_frame)
    control_container.pack(padx=10, pady=10, fill=tk.X)
    
    # 初始参数
    x_value = tk.DoubleVar(value=1.0)  # 滑块离左边的长度
    theta_value = tk.DoubleVar(value=np.pi/4)  # 小球极角
    phi_value = tk.DoubleVar(value=0.0)  # 小球方位角
    
    # 创建用于显示参数值的标签变量
    x_label_var = tk.StringVar(value=f"{x_value.get():.2f}")
    theta_label_var = tk.StringVar(value=f"{theta_value.get():.2f}")
    phi_label_var = tk.StringVar(value=f"{phi_value.get():.2f}")
    
    # 更新系统状态的函数
    def update_system(event=None):
        # 更新系统参数
        spring_pendulum.x = x_value.get()
        spring_pendulum.theta = theta_value.get()
        spring_pendulum.phi = phi_value.get()
        
        # 更新标签显示
        x_label_var.set(f"{x_value.get():.2f}")
        theta_label_var.set(f"{theta_value.get():.2f}")
        phi_label_var.set(f"{phi_value.get():.2f}")
        
        # 重新绘制3D模型
        draw_3d_model()
    
    # 绘制3D模型的函数
    def draw_3d_model():
        # 清除之前的画布
        for widget in viz_frame.winfo_children():
            widget.destroy()
        
        # 创建Figure和Axes
        fig = plt.Figure(figsize=(8, 5))
        ax = fig.add_subplot(111, projection='3d')
        
        # 设置坐标轴范围
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-3, 3)
        ax.set_title('3D弹簧-单摆耦合系统')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        
        # 获取当前系统状态
        x = spring_pendulum.x
        theta = spring_pendulum.theta
        phi = spring_pendulum.phi
        
        # 计算小球位置
        pendulum_x, pendulum_y, pendulum_z = spring_pendulum.get_pendulum_position()
        
        # 绘制固定点
        ax.plot([0], [0], [0], 'ro', markersize=10, label='固定点')
        
        # 绘制弹簧
        spring_x = np.linspace(0, x, 50)
        spring_y = np.zeros_like(spring_x)
        spring_z = np.zeros_like(spring_x)
        # 添加弹簧波形
        num_coils = 10
        spring_y = 0.1 * np.sin(np.linspace(0, 2 * np.pi * num_coils, 50))
        ax.plot(spring_x, spring_y, spring_z, 'b-', linewidth=2, label='弹簧')
        
        # 绘制滑块
        ax.plot([x], [0], [0], 'bo', markersize=20, label='滑块')
        
        # 绘制单摆线
        ax.plot([x, pendulum_x], [0, pendulum_y], [0, pendulum_z], 'g-', linewidth=2, label='单摆线')
        
        # 绘制小球
        ax.plot([pendulum_x], [pendulum_y], [pendulum_z], 'go', markersize=15, label='小球')
        
        # 添加图例
        ax.legend()
        
        # 将Figure添加到Tkinter窗口
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # 创建滑块离左边长度的控件
    x_frame = ttk.Frame(control_container)
    x_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    ttk.Label(x_frame, text="滑块离左边长度 (m):").pack(padx=5, pady=5, anchor=tk.W)
    x_scale = ttk.Scale(x_frame, from_=-2, to=2, variable=x_value, length=200)
    x_scale.pack(padx=5, pady=5)
    x_scale.bind("<ButtonRelease-1>", update_system)  # 只在释放鼠标时更新
    ttk.Label(x_frame, textvariable=x_label_var).pack(padx=5, pady=5)
    
    # 创建小球极角的控件
    theta_frame = ttk.Frame(control_container)
    theta_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    ttk.Label(theta_frame, text="小球极角 (rad):").pack(padx=5, pady=5, anchor=tk.W)
    theta_scale = ttk.Scale(theta_frame, from_=0, to=np.pi, variable=theta_value, length=200)
    theta_scale.pack(padx=5, pady=5)
    theta_scale.bind("<ButtonRelease-1>", update_system)  # 只在释放鼠标时更新
    ttk.Label(theta_frame, textvariable=theta_label_var).pack(padx=5, pady=5)
    
    # 创建小球方位角的控件
    phi_frame = ttk.Frame(control_container)
    phi_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
    ttk.Label(phi_frame, text="小球方位角 (rad):").pack(padx=5, pady=5, anchor=tk.W)
    phi_scale = ttk.Scale(phi_frame, from_=-np.pi, to=np.pi, variable=phi_value, length=200)
    phi_scale.pack(padx=5, pady=5)
    phi_scale.bind("<ButtonRelease-1>", update_system)  # 只在释放鼠标时更新
    ttk.Label(phi_frame, textvariable=phi_label_var).pack(padx=5, pady=5)
    
    # 初始绘制3D模型
    draw_3d_model()
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    # 确保screenshots目录存在
    import os
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    # 启动3D交互模型
    print("启动3D弹簧-单摆耦合系统交互模型...")
    create_interactive_3d_model()