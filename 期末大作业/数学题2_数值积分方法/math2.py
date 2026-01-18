import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# 设置中文字体显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 任务一：基本数值积分方法
print("="*70)
print("任务一：基本数值积分方法")
print("="*70)

# 定义被积函数和精确值
def f1(x):
    return np.sin(x)

# 积分区间和精确值
a1 = 0
b1 = np.pi
exact_value1 = 2  # 精确积分值

# 梯形法（Trapezoidal Rule）实现
def trapezoidal_rule(f, a, b, n):
    '''
    梯形法数值积分
    
    参数:
    f: 被积函数
    a: 积分下限
    b: 积分上限
    n: 分割数
    
    返回:
    积分近似值
    '''
    h = (b - a) / n  # 步长
    x = np.linspace(a, b, n + 1)  # 节点
    y = f(x)
    
    # 梯形法公式: h/2 * [f(a) + 2*sum(f(x_i)) + f(b)]
    integral = h / 2 * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral

# 辛普森法（Simpson's Rule）实现
def simpson_rule(f, a, b, n):
    '''
    辛普森法数值积分
    
    参数:
    f: 被积函数
    a: 积分下限
    b: 积分上限
    n: 分割数（必须为偶数）
    
    返回:
    积分近似值
    '''
    if n % 2 != 0:
        n += 1  # 确保n为偶数
    
    h = (b - a) / n  # 步长
    x = np.linspace(a, b, n + 1)  # 节点
    y = f(x)
    
    # 辛普森法公式: h/3 * [f(a) + 4*sum(f(x_odd)) + 2*sum(f(x_even)) + f(b)]
    integral = h / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2]) + y[-1])
    return integral

# 测试题目要求的分割数
n_values = [4, 8, 16, 32, 64]
trapezoidal_errors = []
simpson_errors = []

for n in n_values:
    # 计算梯形法的近似值和误差
    trapezoidal_approx = trapezoidal_rule(f1, a1, b1, n)
    trapezoidal_error = abs(trapezoidal_approx - exact_value1)
    trapezoidal_errors.append(trapezoidal_error)
    
    # 计算辛普森法的近似值和误差
    simpson_approx = simpson_rule(f1, a1, b1, n)
    simpson_error = abs(simpson_approx - exact_value1)
    simpson_errors.append(simpson_error)

# 输出结果表
print("分割数(n) | 梯形法近似值 | 梯形法误差 | 辛普森法近似值 | 辛普森法误差")
print("-" * 65)
for i, n in enumerate(n_values):
    print(f"{n:8d} | {trapezoidal_rule(f1, a1, b1, n):12.8f} | {trapezoidal_errors[i]:12.8f} | {simpson_rule(f1, a1, b1, n):14.8f} | {simpson_errors[i]:14.8f}")
print("-" * 65)
print(f"精确值: {exact_value1:12.8f}")

# 创建双对数图
plt.figure(figsize=(10, 6))

# 绘制误差曲线
plt.loglog(n_values, trapezoidal_errors, 'o-', label='梯形法误差', color='blue')
plt.loglog(n_values, simpson_errors, 's-', label='辛普森法误差', color='red')

# 计算理论误差阶数参考线
h_values = [(b1 - a1)/n for n in n_values]
# 梯形法理论误差 O(h²)
k_trap = trapezoidal_errors[0] / (h_values[0]**2)
theory_trap = [k_trap * h**2 for h in h_values]
# 辛普森法理论误差 O(h⁴)
k_simp = simpson_errors[0] / (h_values[0]**4)
theory_simp = [k_simp * h**4 for h in h_values]

# 绘制理论误差线
plt.loglog(n_values, theory_trap, 'b--', label='理论误差 O(h²)', alpha=0.7)
plt.loglog(n_values, theory_simp, 'r--', label='理论误差 O(h⁴)', alpha=0.7)

# 设置图例和标签
plt.legend(fontsize=12)
plt.xlabel('分割数 n', fontsize=12)
plt.ylabel('积分误差 |I - I_n|', fontsize=12)
plt.title('数值积分误差与分割数的双对数关系', fontsize=14)

# 设置网格
plt.grid(True, which='both', linestyle='--', alpha=0.7)

# 保存图像
plt.savefig('error_analysis.png', dpi=300, bbox_inches='tight')

# 显示图像
plt.show()

# 计算收敛阶
def compute_convergence_order(errors, n_values):
    '''
    计算收敛阶
    
    参数:
    errors: 误差列表
    n_values: 分割数列表
    
    返回:
    收敛阶列表
    '''
    orders = []
    for i in range(1, len(errors)):
        if errors[i] == 0:
            orders.append(np.inf)
        else:
            # 收敛阶 p = log(error[i-1]/error[i]) / log(n[i]/n[i-1])
            p = np.log(errors[i-1]/errors[i]) / np.log(n_values[i]/n_values[i-1])
            orders.append(p)
    return orders

# 计算梯形法和辛普森法的收敛阶
trapezoidal_orders = compute_convergence_order(trapezoidal_errors, n_values)
simpson_orders = compute_convergence_order(simpson_errors, n_values)

# 输出收敛阶
print("\n梯形法收敛阶：")
for i, order in enumerate(trapezoidal_orders):
    print(f"n={n_values[i]}-{n_values[i+1]}: {order:.4f}")

print("\n辛普森法收敛阶：")
for i, order in enumerate(simpson_orders):
    print(f"n={n_values[i]}-{n_values[i+1]}: {order:.4f}")

# 计算平均收敛阶
avg_trapezoidal_order = np.mean(trapezoidal_orders)
avg_simpson_order = np.mean(simpson_orders)

print(f"\n梯形法平均收敛阶：{avg_trapezoidal_order:.4f} (理论值: 2.0)")
print(f"辛普森法平均收敛阶：{avg_simpson_order:.4f} (理论值: 4.0)")

# 任务二：高斯积分应用
print("\n" + "="*70)
print("任务二：高斯积分应用")
print("="*70)

# 计算高斯积分 ∫₋∞^∞ e^(-x²)dx = √π
def gaussian_integral(L, n):
    '''
    计算高斯积分，使用变量变换将无限区间映射到[-1,1]
    
    参数:
    L: 截断区间长度
    n: 分割数
    
    返回:
    积分近似值
    '''
    # 定义被积函数
    def integrand(x):
        return np.exp(-x**2)
    
    # 方法1：直接截断到[-L,L]
    direct_approx = 2 * trapezoidal_rule(integrand, 0, L, n)
    
    # 方法2：使用变量变换 t = x/√(1-x²) 将无限区间映射到[-1,1]
    def transformed_integrand(t):
        return integrand(t/np.sqrt(1-t**2)) / (1-t**2)**(3/2)
    
    transformed_approx = trapezoidal_rule(transformed_integrand, -1, 1, n)
    
    return direct_approx, transformed_approx

# 分析不同L值对精度的影响
L_values = [1, 2, 3, 4, 5]
n = 1000
exact_gaussian = np.sqrt(np.pi)

print("L值    | 直接截断法近似值 | 直接截断法误差 | 变量变换法近似值 | 变量变换法误差")
print("-" * 70)
for L in L_values:
    direct_approx, transformed_approx = gaussian_integral(L, n)
    direct_error = abs(direct_approx - exact_gaussian)
    transformed_error = abs(transformed_approx - exact_gaussian)
    print(f"{L:6.1f} | {direct_approx:16.10f} | {direct_error:14.10f} | {transformed_approx:18.10f} | {transformed_error:18.10f}")
print("-" * 70)
print(f"精确值: {exact_gaussian:16.10f}")

# 任务三：蒙特卡洛积分（选做）
print("\n" + "="*70)
print("任务三：蒙特卡洛积分（选做）")
print("="*70)

def monte_carlo_integral(f, a, b, N):
    '''
    蒙特卡洛积分
    
    参数:
    f: 被积函数
    a: 积分下限
    b: 积分上限
    N: 随机点数
    
    返回:
    积分估计值, 误差估计
    '''
    # 生成N个均匀随机点
    x = np.random.uniform(a, b, N)
    # 计算函数值
    y = f(x)
    # 计算积分估计值
    integral = (b - a) * np.mean(y)
    # 计算误差估计
    error_estimate = (b - a) * np.std(y) / np.sqrt(N)
    return integral, error_estimate

# 计算 ∫₀¹ e^(-x²)dx
def f2(x):
    return np.exp(-x**2)

a2 = 0
b2 = 1

# 使用不同的随机点数
N_values = [1000, 10000, 100000, 1000000]
monte_carlo_results = []
monte_carlo_errors = []

for N in N_values:
    integral, error = monte_carlo_integral(f2, a2, b2, N)
    monte_carlo_results.append(integral)
    monte_carlo_errors.append(error)

# 与确定性方法比较
deterministic_result = trapezoidal_rule(f2, a2, b2, 10000)
print(f"确定性方法（梯形法，n=10000）结果: {deterministic_result:.10f}")
print("\n随机点数(N) | 蒙特卡洛积分估计 | 误差估计")
print("-" * 40)
for i, N in enumerate(N_values):
    print(f"{N:12d} | {monte_carlo_results[i]:16.10f} | {monte_carlo_errors[i]:10.10f}")
print("-" * 40)

# 绘制蒙特卡洛积分误差收敛曲线
plt.figure(figsize=(10, 6))
plt.loglog(N_values, monte_carlo_errors, 'o-', label='蒙特卡洛积分误差', color='green')

# 添加理论误差参考线 (1/√N)
theory_error = [1/np.sqrt(N) for N in N_values]
# 调整比例常数以匹配实际误差
k = monte_carlo_errors[0] / theory_error[0]
adjusted_theory = [k/np.sqrt(N) for N in N_values]
plt.loglog(N_values, adjusted_theory, 'g--', label='理论误差 O(1/√N)', alpha=0.7)

plt.legend(fontsize=12)
plt.xlabel('随机点数 N', fontsize=12)
plt.ylabel('误差估计', fontsize=12)
plt.title('蒙特卡洛积分误差收敛曲线', fontsize=14)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.savefig('monte_carlo_error.png', dpi=300, bbox_inches='tight')
plt.show()

# 比较分析
print("\n方法比较分析：")
print("- 梯形法：收敛阶 O(h²)，计算稳定，适用于一般函数")
print("- 辛普森法：收敛阶 O(h⁴)，精度更高，计算量与梯形法相近")
print("- 高斯积分：通过变量变换处理无限区间，提高计算效率")
print("- 蒙特卡洛法：收敛慢 (O(1/√N))，但适用于高维积分，实现简单")

print("\n" + "="*70)
print("所有任务完成！")
print("="*70)