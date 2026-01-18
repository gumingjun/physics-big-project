import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 设置中文字体显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 1.2 解析解实现

def projectile_motion_no_drag(v0, theta, g=9.8, t_max=None):
    '''
    无空气阻力抛体运动的解析解
    
    参数:
    v0: 初速度大小 (m/s)
    theta: 发射角度 (度)
    g: 重力加速度 (m/s^2), 默认9.8
    t_max: 模拟时间上限 (s), 默认自动计算
    
    返回:
    t: 时间数组 (s)
    x: x坐标数组 (m)
    y: y坐标数组 (m)
    vx: x方向速度数组 (m/s)
    vy: y方向速度数组 (m/s)
    '''
    theta_rad = np.radians(theta)
    
    # 计算初速度分量
    vx0 = v0 * np.cos(theta_rad)
    vy0 = v0 * np.sin(theta_rad)
    
    # 计算飞行时间（到达地面的时间）
    if t_max is None:
        t_flight = 2 * vy0 / g
    else:
        t_flight = t_max
    
    # 创建时间数组
    t = np.linspace(0, t_flight, 1000)
    
    # 计算位置和速度
    x = vx0 * t
    y = vy0 * t - 0.5 * g * t**2
    vx = np.full_like(t, vx0)
    vy = vy0 - g * t
    
    return t, x, y, vx, vy

# 2.2 数值解实现

def projectile_motion_with_drag(v0, theta, g=9.8, k=0.01, t_max=None):
    '''
    有空气阻力抛体运动的数值解
    
    参数:
    v0: 初速度大小 (m/s)
    theta: 发射角度 (度)
    g: 重力加速度 (m/s^2), 默认9.8
    k: 空气阻力系数 (1/m), 默认0.01
    t_max: 模拟时间上限 (s), 默认自动计算
    
    返回:
    t: 时间数组 (s)
    x: x坐标数组 (m)
    y: y坐标数组 (m)
    vx: x方向速度数组 (m/s)
    vy: y方向速度数组 (m/s)
    '''
    theta_rad = np.radians(theta)
    
    # 计算初速度分量
    vx0 = v0 * np.cos(theta_rad)
    vy0 = v0 * np.sin(theta_rad)
    
    # 定义微分方程组
    def derivatives(t, y):
        x, y_pos, vx, vy = y
        v = np.sqrt(vx**2 + vy**2)
        ax = -k * v * vx
        ay = -g - k * v * vy
        return [vx, vy, ax, ay]
    
    # 初始条件
    y0 = [0, 0, vx0, vy0]
    
    # 设置时间范围
    if t_max is None:
        t_max = 2 * vy0 / g  # 无空气阻力时的飞行时间作为初始猜测
    
    # 求解微分方程
    sol = solve_ivp(derivatives, [0, t_max], y0, method='RK45', dense_output=True)
    
    # 检查是否落地，如果没有则延长模拟时间
    max_iterations = 10  # 设置最大迭代次数
    iterations = 0
    
    while iterations < max_iterations:
        iterations += 1
        t_eval = np.linspace(0, sol.t[-1], 1000)
        y_values = sol.sol(t_eval)[1]
        
        # 寻找y=0的点（落地）
        if np.any(y_values < 0):
            # 使用线性插值找到精确的落地时间
            idx = np.where(y_values < 0)[0][0]
            t_land = t_eval[idx-1] - y_values[idx-1] * (t_eval[idx] - t_eval[idx-1]) / (y_values[idx] - y_values[idx-1])
            t_max = t_land
            sol = solve_ivp(derivatives, [0, t_max], y0, method='RK45', dense_output=True)
            break
        
        # 如果没有落地，延长模拟时间
        t_max *= 2
        sol = solve_ivp(derivatives, [0, t_max], y0, method='RK45', dense_output=True)
        
        # 防止无限循环
        if t_max > 1000:
            break
    
    # 生成结果
    t = np.linspace(0, t_max, 1000)
    x, y, vx, vy = sol.sol(t)
    
    return t, x, y, vx, vy

def calculate_range_and_max_height(x, y):
    '''
    计算抛体运动的射程和最大高度
    
    参数:
    x: x坐标数组 (m)
    y: y坐标数组 (m)
    
    返回:
    range: 射程 (m)
    max_height: 最大高度 (m)
    '''
    range_value = x[-1]
    max_height = np.max(y)
    return range_value, max_height

def plot_trajectory(x_no_drag, y_no_drag, x_with_drag=None, y_with_drag=None, title='抛体运动轨迹'):
    '''
    绘制抛体运动轨迹
    
    参数:
    x_no_drag: 无空气阻力的x坐标数组 (m)
    y_no_drag: 无空气阻力的y坐标数组 (m)
    x_with_drag: 有空气阻力的x坐标数组 (m), 可选
    y_with_drag: 有空气阻力的y坐标数组 (m), 可选
    title: 图表标题
    '''
    plt.figure(figsize=(10, 6))
    
    # 绘制无空气阻力的轨迹
    plt.plot(x_no_drag, y_no_drag, 'b-', linewidth=2, label='无空气阻力')
    
    # 绘制有空气阻力的轨迹（如果提供）
    if x_with_drag is not None and y_with_drag is not None:
        plt.plot(x_with_drag, y_with_drag, 'r--', linewidth=2, label='有空气阻力')
    
    plt.xlabel('x (m)', fontsize=12)
    plt.ylabel('y (m)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig('trajectory.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_velocity(t_no_drag, vx_no_drag, vy_no_drag, t_with_drag=None, vx_with_drag=None, vy_with_drag=None):
    '''
    绘制速度随时间的变化
    
    参数:
    t_no_drag: 无空气阻力的时间数组 (s)
    vx_no_drag: 无空气阻力的x方向速度数组 (m/s)
    vy_no_drag: 无空气阻力的y方向速度数组 (m/s)
    t_with_drag: 有空气阻力的时间数组 (s), 可选
    vx_with_drag: 有空气阻力的x方向速度数组 (m/s), 可选
    vy_with_drag: 有空气阻力的y方向速度数组 (m/s), 可选
    '''
    plt.figure(figsize=(12, 6))
    
    # 绘制x方向速度
    plt.subplot(1, 2, 1)
    plt.plot(t_no_drag, vx_no_drag, 'b-', linewidth=2, label='无空气阻力')
    if t_with_drag is not None and vx_with_drag is not None:
        plt.plot(t_with_drag, vx_with_drag, 'r--', linewidth=2, label='有空气阻力')
    plt.xlabel('时间 (s)', fontsize=12)
    plt.ylabel('v_x (m/s)', fontsize=12)
    plt.title('x方向速度随时间变化', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    # 绘制y方向速度
    plt.subplot(1, 2, 2)
    plt.plot(t_no_drag, vy_no_drag, 'b-', linewidth=2, label='无空气阻力')
    if t_with_drag is not None and vy_with_drag is not None:
        plt.plot(t_with_drag, vy_with_drag, 'r--', linewidth=2, label='有空气阻力')
    plt.xlabel('时间 (s)', fontsize=12)
    plt.ylabel('v_y (m/s)', fontsize=12)
    plt.title('y方向速度随时间变化', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig('velocity.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_different_angles(v0, angles, g=9.8, k=0.01):
    '''
    绘制不同发射角度下的轨迹
    
    参数:
    v0: 初速度大小 (m/s)
    angles: 发射角度列表 (度)
    g: 重力加速度 (m/s^2), 默认9.8
    k: 空气阻力系数 (1/m), 默认0.01
    '''
    plt.figure(figsize=(10, 6))
    
    for angle in angles:
        # 无空气阻力
        t, x, y, vx, vy = projectile_motion_no_drag(v0, angle, g)
        plt.plot(x, y, '-', linewidth=2, label=f'θ={angle}° (无阻力)')
        
        # 有空气阻力
        t_drag, x_drag, y_drag, vx_drag, vy_drag = projectile_motion_with_drag(v0, angle, g, k)
        plt.plot(x_drag, y_drag, '--', linewidth=2, label=f'θ={angle}° (有阻力)')
    
    plt.xlabel('x (m)', fontsize=12)
    plt.ylabel('y (m)', fontsize=12)
    plt.title(f'不同发射角度下的抛体运动轨迹 (v0={v0} m/s)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('different_angles.png', dpi=300, bbox_inches='tight')
    plt.show()

# 任务一：无空气阻力的抛体运动
print("="*70)
print("任务一：无空气阻力的抛体运动")
print("="*70)

# 设置参数
v0_task1 = 20  # 初速度 (m/s)
g = 9.8  # 重力加速度 (m/s^2)
angles_task1 = [15, 30, 45, 60, 75]  # 不同的发射角度 (度)

# 计算并绘制不同发射角度的轨迹
plt.figure(figsize=(12, 8))

ranges = []
for angle in angles_task1:
    t, x, y, vx, vy = projectile_motion_no_drag(v0_task1, angle, g)
    range_value, max_height = calculate_range_and_max_height(x, y)
    ranges.append(range_value)
    plt.plot(x, y, '-', linewidth=2, label=f'θ={angle}° (射程: {range_value:.2f}m)')

# 找到最大射程及其对应的角度
max_range = max(ranges)
max_range_angle = angles_task1[ranges.index(max_range)]

print(f"无空气阻力抛体运动分析 (v0={v0_task1} m/s):")
print("-" * 60)
print(f"发射角度: {angles_task1}")
print(f"对应射程: {[f'{r:.2f}' for r in ranges]} m")
print(f"最大射程: {max_range:.2f} m (对应角度: {max_range_angle}°)")
print(f"验证结果: {'θ=45°时射程最大' if max_range_angle == 45 else f'θ={max_range_angle}°时射程最大'}")
print("-" * 60)

# 标注最大射程
plt.axvline(x=max_range, color='k', linestyle='--', alpha=0.7, label=f'最大射程: {max_range:.2f}m')

plt.xlabel('水平位移 x (m)', fontsize=12)
plt.ylabel('垂直位移 y (m)', fontsize=12)
plt.title(f'不同发射角度的抛体运动轨迹 (v0={v0_task1} m/s)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('trajectory_different_angles.png', dpi=300, bbox_inches='tight')
plt.show()

# 任务二：考虑空气阻力的抛体运动
print("\n" + "="*70)
print("任务二：考虑空气阻力的抛体运动")
print("="*70)

# 设置参数
m = 1.0  # 质量 (kg)
v0_task2 = 20  # 初速度 (m/s)
theta_task2 = 45  # 发射角度 (度)
b_over_m_values = [0, 0.1, 0.3, 0.5]  # b/m 值

# 绘制不同阻力系数下的轨迹
plt.figure(figsize=(12, 8))

for b_over_m in b_over_m_values:
    # 使用修正后的空气阻力系数（与速度成正比）
    k = b_over_m  # 因为 F_drag = -b v，所以 k = b/m
    t, x, y, vx, vy = projectile_motion_with_drag(v0_task2, theta_task2, g, k)
    range_value, max_height = calculate_range_and_max_height(x, y)
    plt.plot(x, y, '-', linewidth=2, label=f'b/m={b_over_m} (射程: {range_value:.2f}m)')

print(f"有空气阻力抛体运动分析 (v0={v0_task2} m/s, θ={theta_task2}°):")
print("-" * 60)
print(f"b/m 值: {b_over_m_values}")
print("-" * 60)

plt.xlabel('水平位移 x (m)', fontsize=12)
plt.ylabel('垂直位移 y (m)', fontsize=12)
plt.title(f'不同阻力系数下的抛体运动轨迹 (v0={v0_task2} m/s, θ={theta_task2}°)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('trajectory_with_drag.png', dpi=300, bbox_inches='tight')
plt.show()

# 分析最佳发射角
print("\n最佳发射角分析:")
print("-" * 60)
print("无空气阻力时，最佳发射角为 45°")
print("有空气阻力时，最佳发射角通常小于 45°，因为空气阻力会使水平速度衰减")
print("-" * 60)

# 任务三：能量分析
print("\n" + "="*70)
print("任务三：能量分析")
print("="*70)

def calculate_energy(t, x, y, vx, vy, m, g):
    '''
    计算抛体运动的能量
    
    参数:
    t: 时间数组 (s)
    x: x坐标数组 (m)
    y: y坐标数组 (m)
    vx: x方向速度数组 (m/s)
    vy: y方向速度数组 (m/s)
    m: 质量 (kg)
    g: 重力加速度 (m/s^2)
    
    返回:
    kinetic_energy: 动能数组 (J)
    potential_energy: 势能数组 (J)
    total_energy: 总能量数组 (J)
    '''
    kinetic_energy = 0.5 * m * (vx**2 + vy**2)
    potential_energy = m * g * y
    total_energy = kinetic_energy + potential_energy
    return kinetic_energy, potential_energy, total_energy

# 无空气阻力的能量分析
t_no_drag, x_no_drag, y_no_drag, vx_no_drag, vy_no_drag = projectile_motion_no_drag(v0_task2, theta_task2, g)
ke_no_drag, pe_no_drag, te_no_drag = calculate_energy(t_no_drag, x_no_drag, y_no_drag, vx_no_drag, vy_no_drag, m, g)

# 有空气阻力的能量分析
k_drag = 0.1  # b/m = 0.1
t_with_drag, x_with_drag, y_with_drag, vx_with_drag, vy_with_drag = projectile_motion_with_drag(v0_task2, theta_task2, g, k_drag)
ke_with_drag, pe_with_drag, te_with_drag = calculate_energy(t_with_drag, x_with_drag, y_with_drag, vx_with_drag, vy_with_drag, m, g)

# 绘制能量变化
plt.figure(figsize=(12, 8))

# 无空气阻力
plt.subplot(2, 1, 1)
plt.plot(t_no_drag, ke_no_drag, 'r-', linewidth=2, label='动能')
plt.plot(t_no_drag, pe_no_drag, 'g-', linewidth=2, label='势能')
plt.plot(t_no_drag, te_no_drag, 'b-', linewidth=2, label='总能量')
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('能量 E (J)', fontsize=12)
plt.title(f'无空气阻力时的能量变化 (v0={v0_task2} m/s, θ={theta_task2}°)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# 有空气阻力
plt.subplot(2, 1, 2)
plt.plot(t_with_drag, ke_with_drag, 'r-', linewidth=2, label='动能')
plt.plot(t_with_drag, pe_with_drag, 'g-', linewidth=2, label='势能')
plt.plot(t_with_drag, te_with_drag, 'b-', linewidth=2, label='总能量')
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('能量 E (J)', fontsize=12)
plt.title(f'有空气阻力时的能量变化 (b/m={k_drag})', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

plt.tight_layout()
plt.savefig('energy_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 能量分析结果
print("能量分析结果:")
print("-" * 60)
print(f"无空气阻力:")
print(f"  初始总能量: {te_no_drag[0]:.2f} J")
print(f"  最终总能量: {te_no_drag[-1]:.2f} J")
print(f"  能量变化: {abs(te_no_drag[-1] - te_no_drag[0]):.2f} J (机械能守恒)")
print()
print(f"有空气阻力 (b/m={k_drag}):")
print(f"  初始总能量: {te_with_drag[0]:.2f} J")
print(f"  最终总能量: {te_with_drag[-1]:.2f} J")
print(f"  能量损失: {te_with_drag[0] - te_with_drag[-1]:.2f} J (转化为热能)")
print("-" * 60)

print("\n" + "="*70)
print("所有任务完成！")
print("="*70)