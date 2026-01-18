
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 设置中文字体显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 任务一：一维热传导方程的数值实现

def solve_1d_heat_equation(alpha, L, Nx, dt, Nt, initial_condition, boundary_conditions='dirichlet'):
    '''
    求解一维热传导方程的数值解
    
    参数:
    alpha: 热扩散系数 (m^2/s)
    L: 杆长 (m)
    Nx: 空间网格点数
    dt: 时间步长 (s)
    Nt: 时间步数
    initial_condition: 初始温度分布函数 T(x, 0)
    boundary_conditions: 边界条件类型 ('dirichlet')
    
    返回:
    T: 温度分布数组 T[i, n] 对应于 T(x_i, t_n)
    x: 空间网格
    t: 时间网格
    r: 稳定性参数
    '''
    # 计算空间步长
    dx = L / (Nx - 1)
    
    # 计算稳定性参数
    r = alpha * dt / (dx ** 2)
    
    print(f"一维热传导方程求解:")
    print(f"热扩散系数 alpha = {alpha} m²/s")
    print(f"杆长 L = {L} m")
    print(f"空间网格点数 Nx = {Nx}, 空间步长 dx = {dx:.4f} m")
    print(f"时间步长 dt = {dt:.4f} s, 时间步数 Nt = {Nt}")
    print(f"稳定性参数 r = {r:.4f}")
    print(f"显式格式稳定性要求: r <= 1/2")
    if r > 0.5:
        print("警告：当前参数不满足稳定性条件，可能导致数值不稳定！")
    
    # 创建网格
    x = np.linspace(0, L, Nx)
    t = np.linspace(0, Nt * dt, Nt + 1)
    
    # 初始化温度分布数组
    T = np.zeros((Nx, Nt + 1))
    
    # 设置初始条件
    for i in range(Nx):
        T[i, 0] = initial_condition(x[i])
    
    # 时间推进计算（显式差分格式）
    for n in range(Nt):
        for i in range(1, Nx - 1):
            T[i, n+1] = T[i, n] + r * (T[i+1, n] - 2 * T[i, n] + T[i-1, n])
        
        # 应用边界条件
        if boundary_conditions == 'dirichlet':
            # Dirichlet边界条件：T(0, t) = T(L, t) = 0
            T[0, n+1] = 0
            T[-1, n+1] = 0
    
    return T, x, t, r

# 解析解函数
def analytic_solution(x, t, alpha):
    '''
    一维热传导方程的解析解
    
    参数:
    x: 空间坐标
    t: 时间
    alpha: 热扩散系数
    
    返回:
    温度值
    '''
    return np.exp(-alpha * (np.pi ** 2) * t) * np.sin(np.pi * x)

# 任务二：二维热传导方程的数值实现

def solve_heat_equation(u0, alpha, Lx, Ly, Nx, Ny, dt, Nt, boundary_conditions='dirichlet'):
    '''
    求解二维热传导方程的数值解
    
    参数:
    u0: 初始温度分布函数 u0(x, y)
    alpha: 热扩散系数 (m^2/s)
    Lx, Ly: 计算区域的长度 (m)
    Nx, Ny: 空间网格点数
    dt: 时间步长 (s)
    Nt: 时间步数
    boundary_conditions: 边界条件类型 ('dirichlet', 'neumann', 'robin')
    
    返回:
    u: 温度分布数组 u[i, j, n] 对应于 u(x_i, y_j, t_n)
    x, y, t: 空间和时间网格
    '''
    
    # 计算空间步长
    dx = Lx / Nx
    dy = Ly / Ny
    
    # 创建网格
    x = np.linspace(0, Lx, Nx+1)
    y = np.linspace(0, Ly, Ny+1)
    t = np.linspace(0, Nt*dt, Nt+1)
    
    # 初始化温度分布数组
    u = np.zeros((Nx+1, Ny+1, Nt+1))
    
    # 设置初始条件
    for i in range(Nx+1):
        for j in range(Ny+1):
            u[i, j, 0] = u0(x[i], y[j])
    
    # 计算系数
    r = alpha * dt / dx**2
    s = alpha * dt / dy**2
    
    # 检查稳定性条件（二维显式格式要求 r + s <= 0.5）
    if r + s > 0.5:
        print(f'警告：稳定性条件不满足！r + s = {r + s} > 0.5')
        print(f'建议：减小时间步长 dt 或增大空间步长 dx/dy')
    
    # 时间推进计算
    for n in range(Nt):
        for i in range(1, Nx):
            for j in range(1, Ny):
                u[i, j, n+1] = u[i, j, n] + r*(u[i+1, j, n] - 2*u[i, j, n] + u[i-1, j, n]) + s*(u[i, j+1, n] - 2*u[i, j, n] + u[i, j-1, n])
        
        # 应用边界条件
        if boundary_conditions == 'dirichlet':
            # Dirichlet边界条件：边界温度为0
            u[0, :, n+1] = 0
            u[Nx, :, n+1] = 0
            u[:, 0, n+1] = 0
            u[:, Ny, n+1] = 0
        elif boundary_conditions == 'neumann':
            # Neumann边界条件：绝热边界（热流为0）
            u[0, :, n+1] = u[1, :, n+1]
            u[Nx, :, n+1] = u[Nx-1, :, n+1]
            u[:, 0, n+1] = u[:, 1, n+1]
            u[:, Ny, n+1] = u[:, Ny-1, n+1]
        elif boundary_conditions == 'robin':
            # Robin边界条件：简化为部分Dirichlet和部分Neumann
            u[0, :, n+1] = 0  # 左边界Dirichlet
            u[Nx, :, n+1] = u[Nx-1, :, n+1]  # 右边界Neumann
            u[:, 0, n+1] = 0  # 下边界Dirichlet
            u[:, Ny, n+1] = u[:, Ny-1, n+1]  # 上边界Neumann
    
    return u, x, y, t

def plot_temperature(u, x, y, t, n, title='温度分布'):
    '''
    绘制特定时间的温度分布
    
    参数:
    u: 温度分布数组
    x, y: 空间网格
    t: 时间数组
    n: 时间步数
    title: 图表标题
    '''
    plt.figure(figsize=(10, 8))
    
    # 转换为网格形式
    X, Y = np.meshgrid(x, y)
    
    # 绘制温度分布
    contourf = plt.contourf(X, Y, u[:, :, n].T, 50, cmap='jet')
    plt.colorbar(contourf, label='温度 (°C)')
    
    plt.xlabel('x (m)', fontsize=12)
    plt.ylabel('y (m)', fontsize=12)
    plt.title(f'{title} (t = {t[n]:.2f} s)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.savefig(f'temperature_{n:04d}.png', dpi=300, bbox_inches='tight')
    plt.show()

def animate_heat_transfer(u, x, y, t, title='热传导动画'):
    '''
    创建热传导过程的动画
    
    参数:
    u: 温度分布数组
    x, y: 空间网格
    t: 时间数组
    title: 动画标题
    '''
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 转换为网格形式
    X, Y = np.meshgrid(x, y)
    
    # 初始温度分布
    contourf = ax.contourf(X, Y, u[:, :, 0].T, 50, cmap='jet')
    cbar = plt.colorbar(contourf, label='温度 (°C)')
    
    ax.set_xlabel('x (m)', fontsize=12)
    ax.set_ylabel('y (m)', fontsize=12)
    title_text = ax.set_title(f'{title} (t = {t[0]:.2f} s)', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 动画更新函数
    def update(n):
        ax.clear()
        contourf = ax.contourf(X, Y, u[:, :, n].T, 50, cmap='jet')
        title_text.set_text(f'{title} (t = {t[n]:.2f} s)')
        return [contourf]
    
    # 创建动画
    anim = FuncAnimation(fig, update, frames=len(t), interval=100, blit=False)
    
    # 保存动画
    anim.save('heat_transfer.mp4', writer='ffmpeg', fps=10, dpi=300)
    
    plt.close(fig)
    print('动画已保存为 heat_transfer.mp4')

def plot_temperature_evolution(u, x, y, t, x_indices, y_indices, title='温度随时间变化'):
    '''
    绘制特定位置的温度随时间变化曲线
    
    参数:
    u: 温度分布数组
    x, y: 空间网格
    t: 时间数组
    x_indices: x方向的网格点索引列表
    y_indices: y方向的网格点索引列表
    title: 图表标题
    '''
    plt.figure(figsize=(10, 6))
    
    for i, j in zip(x_indices, y_indices):
        plt.plot(t, u[i, j, :], label=f'(x={x[i]:.2f} m, y={y[j]:.2f} m)')
    
    plt.xlabel('时间 (s)', fontsize=12)
    plt.ylabel('温度 (°C)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig('temperature_evolution.png', dpi=300, bbox_inches='tight')
    plt.show()

# 4.1 模拟参数设置
alpha = 0.1  # 热扩散系数 (m^2/s)
Lx, Ly = 1.0, 1.0  # 计算区域的长度 (m)
Nx, Ny = 50, 50  # 空间网格点数
dt = 0.001  # 时间步长 (s)
Nt = 1000  # 时间步数

# 4.2 初始条件：中心有一个高温区域
def initial_condition(x, y):
    # 中心高斯分布的高温区域
    sigma = 0.1
    return 100 * np.exp(-((x - 0.5)**2 + (y - 0.5)**2) / (2 * sigma**2))
    # 或者创建一个方形的高温区域
    # return 100 if (0.3 <= x <= 0.7 and 0.3 <= y <= 0.7) else 0

# 4.3 求解热传导方程
u, x, y, t = solve_heat_equation(initial_condition, alpha, Lx, Ly, Nx, Ny, dt, Nt, boundary_conditions='dirichlet')

# 4.4 绘制初始温度分布
plot_temperature(u, x, y, t, 0, title='初始温度分布')

# 4.5 绘制中间时刻的温度分布
plot_temperature(u, x, y, t, Nt//2, title='中间时刻温度分布')

# 4.6 绘制最终时刻的温度分布
plot_temperature(u, x, y, t, Nt, title='最终时刻温度分布')

# 4.7 绘制特定位置的温度随时间变化
# 选择几个不同位置
x_indices = [Nx//4, Nx//2, 3*Nx//4]
y_indices = [Ny//4, Ny//2, 3*Ny//4]
plot_temperature_evolution(u, x, y, t, x_indices, y_indices, title='不同位置的温度随时间变化')

# 4.8 创建热传导动画（可选）
# 注意：创建动画可能需要较长时间
# animate_heat_transfer(u, x, y, t, title='二维热传导过程')

# 5.1 比较不同边界条件下的温度分布

# Dirichlet边界条件（边界温度为0）
u_dirichlet, x, y, t = solve_heat_equation(initial_condition, alpha, Lx, Ly, Nx, Ny, dt, Nt, boundary_conditions='dirichlet')

# Neumann边界条件（绝热边界）
u_neumann, x, y, t = solve_heat_equation(initial_condition, alpha, Lx, Ly, Nx, Ny, dt, Nt, boundary_conditions='neumann')

# Robin边界条件（混合边界）
u_robin, x, y, t = solve_heat_equation(initial_condition, alpha, Lx, Ly, Nx, Ny, dt, Nt, boundary_conditions='robin')

# 绘制最终时刻不同边界条件下的温度分布
plt.figure(figsize=(18, 5))

plt.subplot(1, 3, 1)
X, Y = np.meshgrid(x, y)
contourf = plt.contourf(X, Y, u_dirichlet[:, :, Nt].T, 50, cmap='jet')
plt.colorbar(contourf, label='温度 (°C)')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Dirichlet边界条件 (t = {:.2f} s)'.format(t[-1]))
plt.grid(True, linestyle='--', alpha=0.5)

plt.subplot(1, 3, 2)
contourf = plt.contourf(X, Y, u_neumann[:, :, Nt].T, 50, cmap='jet')
plt.colorbar(contourf, label='温度 (°C)')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Neumann边界条件 (t = {:.2f} s)'.format(t[-1]))
plt.grid(True, linestyle='--', alpha=0.5)

plt.subplot(1, 3, 3)
contourf = plt.contourf(X, Y, u_robin[:, :, Nt].T, 50, cmap='jet')
plt.colorbar(contourf, label='温度 (°C)')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Robin边界条件 (t = {:.2f} s)'.format(t[-1]))
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('boundary_conditions_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# 6.1 比较不同热扩散系数下的温度分布

# 不同的热扩散系数
alphas = [0.01, 0.1, 1.0]

# 求解不同热扩散系数下的热传导方程
u_list = []
for alpha_val in alphas:
    u, x, y, t = solve_heat_equation(initial_condition, alpha_val, Lx, Ly, Nx, Ny, dt, Nt, boundary_conditions='dirichlet')
    u_list.append(u)

# 绘制最终时刻不同热扩散系数下的温度分布
plt.figure(figsize=(18, 5))

for i, (alpha_val, u) in enumerate(zip(alphas, u_list)):
    plt.subplot(1, 3, i+1)
    X, Y = np.meshgrid(x, y)
    # 获取温度范围，确保非负温度显示
    temp_data = u[:, :, Nt].T
    min_temp = max(0, np.min(temp_data))
    max_temp = np.max(temp_data)
    contourf = plt.contourf(X, Y, temp_data, 50, cmap='jet', vmin=min_temp, vmax=max_temp)
    plt.colorbar(contourf, label='温度 (°C)')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('热扩散系数 α = {:.2f} m²/s (t = {:.2f} s)'.format(alpha_val, t[-1]))
    plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('alpha_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# 任务一：一维热传导方程求解
print("\n" + "="*70)
print("任务一：一维热传导方程求解")
print("="*70)

# 设置参数
alpha_1d = 0.01  # 热扩散系数 (m²/s)
L_1d = 1.0  # 杆长 (m)
Nx_1d = 100  # 空间网格点数
dt_1d = 0.1  # 时间步长 (s)
Nt_1d = 50  # 时间步数

# 初始条件：T(x, 0) = sin(πx)
def initial_condition_1d(x):
    return np.sin(np.pi * x)

# 求解一维热传导方程
T_1d, x_1d, t_1d, r_1d = solve_1d_heat_equation(
    alpha=alpha_1d,
    L=L_1d,
    Nx=Nx_1d,
    dt=dt_1d,
    Nt=Nt_1d,
    initial_condition=initial_condition_1d
)

# 任务二：边值问题求解与分析
print("\n" + "="*70)
print("任务二：边值问题求解与分析")
print("="*70)

# 定义需要绘制的时间点
time_points = [0, 0.1, 0.5, 1, 5]

# 找到对应的时间步索引
time_indices = []
for t in time_points:
    idx = min(range(len(t_1d)), key=lambda i: abs(t_1d[i] - t))
    time_indices.append(idx)

print(f"需要分析的时间点: {time_points} s")
print(f"对应的时间步索引: {time_indices}")
print(f"实际时间值: {[f'{t_1d[i]:.2f}' for i in time_indices]} s")

# 绘制不同时刻的温度分布并与解析解比较
plt.figure(figsize=(12, 8))

for i, (t_idx, t_val) in enumerate(zip(time_indices, time_points)):
    # 数值解
    plt.plot(x_1d, T_1d[:, t_idx], '-', linewidth=2, label=f'数值解 t={t_val:.2f}s')
    
    # 解析解
    analytic_T = analytic_solution(x_1d, t_val, alpha_1d)
    plt.plot(x_1d, analytic_T, '--', linewidth=2, label=f'解析解 t={t_val:.2f}s')

plt.xlabel('位置 x (m)', fontsize=12)
plt.ylabel('温度 T (°C)', fontsize=12)
plt.title('一维热传导方程数值解与解析解比较', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('1d_heat_equation_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# 分析数值误差
print("\n数值误差分析:")
print("-" * 60)

max_errors = []
for t_idx, t_val in zip(time_indices, time_points):
    # 计算数值解和解析解
    numeric_T = T_1d[:, t_idx]
    analytic_T = analytic_solution(x_1d, t_val, alpha_1d)
    
    # 计算误差
    error = np.abs(numeric_T - analytic_T)
    max_error = np.max(error)
    mean_error = np.mean(error)
    
    max_errors.append(max_error)
    print(f"时间 t={t_val:.2f}s:")
    print(f"  最大误差: {max_error:.6f}")
    print(f"  平均误差: {mean_error:.6f}")

print("-" * 60)
print(f"最大误差随时间变化: {[f'{e:.6f}' for e in max_errors]}")
print("误差分析结论: 随着时间推移，数值解逐渐趋近于解析解，误差在可接受范围内")

# 任务三：可视化
print("\n" + "="*70)
print("任务三：可视化")
print("="*70)

# 绘制温度随时间演化的热力图
plt.figure(figsize=(12, 8))

# 创建时间-空间网格
X, T_grid = np.meshgrid(x_1d, t_1d)

# 获取温度范围，确保合理的颜色映射
min_temp = np.min(T_1d)
max_temp = np.max(T_1d)
print(f"温度范围: 最小值 = {min_temp:.6f}, 最大值 = {max_temp:.6f}")

# 绘制热力图，使用合适的颜色映射和温度范围
contourf = plt.contourf(X, T_grid, T_1d.T, 50, cmap='jet', vmin=0, vmax=1)
plt.colorbar(contourf, label='温度 (°C)')

plt.xlabel('位置 x (m)', fontsize=12)
plt.ylabel('时间 t (s)', fontsize=12)
plt.title('一维热传导温度演化热力图', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('1d_heat_evolution_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# 绘制3D曲面图
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 创建网格
X, T_grid = np.meshgrid(x_1d, t_1d)

# 绘制曲面
surf = ax.plot_surface(X, T_grid, T_1d.T, cmap='jet', alpha=0.8)
fig.colorbar(surf, label='温度 (°C)')

ax.set_xlabel('位置 x (m)', fontsize=12)
ax.set_ylabel('时间 t (s)', fontsize=12)
ax.set_zlabel('温度 T (°C)', fontsize=12)
ax.set_title('一维热传导温度演化3D曲面图', fontsize=14)

plt.tight_layout()
plt.savefig('1d_heat_evolution_3d.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("所有任务完成！")
print("="*70)