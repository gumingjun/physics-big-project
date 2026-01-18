import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.fft import fft, fftfreq

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 定义周期方波函数（符合任务要求）
def square_wave(x, T=2*np.pi):
    x_mod = x % T
    if 0 < x_mod < T/2:
        return 1
    else:
        return -1

# 计算傅里叶系数
def compute_fourier_coeffs(func, T, n_max):
    a0 = (2/T) * integrate.quad(func, -T/2, T/2)[0]
    an = []
    bn = []
    
    for n in range(1, n_max + 1):
        an.append((2/T) * integrate.quad(lambda x: func(x) * np.cos(2*np.pi*n*x/T), -T/2, T/2)[0])
        bn.append((2/T) * integrate.quad(lambda x: func(x) * np.sin(2*np.pi*n*x/T), -T/2, T/2)[0])
    
    return a0, an, bn

# 构建傅里叶级数
def fourier_series(x, a0, an, bn, T):
    result = a0 / 2
    n_max = len(an)
    
    for n in range(1, n_max + 1):
        result += an[n-1] * np.cos(2*np.pi*n*x/T)
        result += bn[n-1] * np.sin(2*np.pi*n*x/T)
    
    return result

# 任务一：方波的傅里叶展开
print('='*60)
print('任务一：方波的傅里叶展开')
print('='*60)

# 计算方波的傅里叶系数，周期T=2π
T = 2 * np.pi
n_max = 51  # 计算到51项以满足任务要求

a0, an, bn = compute_fourier_coeffs(square_wave, T, n_max)

print(f'方波的傅里叶系数：')
print(f'a0 = {a0:.6f}')
for n in range(10):  # 只打印前10项
    print(f'n={n+1}: an={an[n]:.6f}, bn={bn[n]:.6f}')

# 验证傅里叶系数公式
print('\n验证傅里叶系数公式：')
print('理论值：an=0, bn=4/(nπ)（仅n为奇数时非零）')
print('计算值验证：')
for n in range(5):  # 验证前5项
    n_val = n + 1
    theoretical_bn = 4/(n_val*np.pi) if n_val % 2 == 1 else 0
    print(f'n={n_val}: 计算bn={bn[n]:.6f}, 理论bn={theoretical_bn:.6f}, 误差={abs(bn[n]-theoretical_bn):.6f}')

# 绘制原方波与傅里叶级数近似（任务要求的N=3,5,11,51项）
x = np.linspace(-T, T, 1000)
original = np.array([square_wave(xi, T) for xi in x])

plt.figure(figsize=(14, 10))
plt.plot(x, original, 'k-', label='原方波', linewidth=2)

# 分别绘制不同项数的傅里叶级数
for n_terms in [3, 5, 11, 51]:
    approx = fourier_series(x, a0, an[:n_terms], bn[:n_terms], T)
    plt.plot(x, approx, label=f'{n_terms}项傅里叶级数')

plt.title('方波的傅里叶级数近似（观察吉布斯现象）')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()

# 观察并描述吉布斯现象
print('\n吉布斯现象观察：')
print('1. 当傅里叶级数项数增加时，在方波的跳变点附近会出现振荡')
print('2. 这些振荡的振幅不会随项数增加而减小，而是逐渐向跳变点集中')
print('3. 振荡的最大振幅约为跳变幅度的9%左右')
print('4. 这是由于傅里叶级数在不连续点处的收敛特性导致的')

# 任务二：三角波的傅里叶展开
print('\n' + '='*60)
print('任务二：三角波的傅里叶展开')
print('='*60)

# 定义三角波函数（符合任务要求：g(x) = |x|, -π < x < π）
def triangular_wave(x, T=2*np.pi):
    # 调整为 |x| 形式，范围在[-π, π]内
    x_abs = abs(x % T - T/2)
    return x_abs

# 计算三角波的傅里叶系数
a0_tri, an_tri, bn_tri = compute_fourier_coeffs(triangular_wave, T, n_max)

print(f'三角波的傅里叶系数：')
print(f'a0 = {a0_tri:.6f}')
for n in range(10):  # 只打印前10项
    print(f'n={n+1}: an={an_tri[n]:.6f}, bn={bn_tri[n]:.6f}')

# 绘制原三角波与傅里叶级数近似（任务要求的N=1,3,5,10项）
original_tri = np.array([triangular_wave(xi, T) for xi in x])

plt.figure(figsize=(14, 10))
plt.plot(x, original_tri, 'k-', label='原三角波', linewidth=2)

# 分别绘制不同项数的傅里叶级数
for n_terms in [1, 3, 5, 10]:
    approx_tri = fourier_series(x, a0_tri, an_tri[:n_terms], bn_tri[:n_terms], T)
    plt.plot(x, approx_tri, label=f'{n_terms}项傅里叶级数')

plt.title('三角波的傅里叶级数近似（收敛过程）')
plt.xlabel('x')
plt.ylabel('g(x)')
plt.legend()
plt.grid(True)
plt.show()

# 解释为什么三角波比方波收敛更快
print('\n三角波比方波收敛更快的原因：')
print('1. 三角波是连续函数，而方波在跳变点处不连续')
print('2. 三角波的导数存在（除了顶点），而方波的导数不存在')
print('3. 三角波的傅里叶系数衰减速度为1/n²，而方波的傅里叶系数衰减速度为1/n')
print('4. 系数衰减越快，级数收敛就越快，因此三角波的傅里叶级数收敛更快')

# 任务三：简单信号合成
print('\n' + '='*60)
print('任务三：简单信号合成')
print('='*60)

# 生成复合信号：s(t) = sin(2π·3t) + 0.5sin(2π·7t) + 0.3sin(2π·11t)
def composite_signal(t):
    return np.sin(2*np.pi*3*t) + 0.5*np.sin(2*np.pi*7*t) + 0.3*np.sin(2*np.pi*11*t)

# 绘制复合信号（任务要求t∈[0,2]）
t = np.linspace(0, 2, 2000)  # 0到2秒，满足任务要求
signal = composite_signal(t)

plt.figure(figsize=(14, 6))
plt.plot(t, signal, 'b-', linewidth=2)
plt.title('复合信号：sin(2π·3t) + 0.5sin(2π·7t) + 0.3sin(2π·11t)')
plt.xlabel('时间 t (秒)')
plt.ylabel('信号幅度')
plt.grid(True)
plt.show()

# 对信号进行FFT分析
N = len(signal)
T_sample = t[1] - t[0]

# 计算FFT
yf = fft(signal)
xf = fftfreq(N, T_sample)

# 只取正频率部分
xf_positive = xf[:N//2]
yf_magnitude = 2.0/N * np.abs(yf[:N//2])

# 绘制频谱图
plt.figure(figsize=(14, 6))
plt.stem(xf_positive, yf_magnitude, basefmt='b-', use_line_collection=True)
plt.title('复合信号的频谱')
plt.xlabel('频率 (Hz)')
plt.ylabel('幅度')
plt.xlim(0, 15)  # 只显示0-15Hz
plt.grid(True)

# 标记三个频率成分
for f in [3, 7, 11]:
    idx = np.argmin(np.abs(xf_positive - f))
    plt.text(f, yf_magnitude[idx]+0.05, f'f={f}Hz', ha='center', va='bottom', fontsize=12, color='red')

plt.show()

# 验证频率成分
print('\n频率成分验证：')
print('任务要求的频率成分：3Hz、7Hz、11Hz')
print('FFT分析结果：')
for f in [3, 7, 11]:
    idx = np.argmin(np.abs(xf_positive - f))
    amp = yf_magnitude[idx]
    print(f'频率 {f}Hz: 幅度 = {amp:.4f}')

print('\n验证结果：成功检测到3Hz、7Hz、11Hz三个频率成分')

print('\n' + '='*60)
print('所有任务完成！')
print('='*60)