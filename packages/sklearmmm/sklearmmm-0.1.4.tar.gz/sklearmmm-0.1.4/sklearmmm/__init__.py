def get_task(option=None):
    task_map = {
        1: """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
import sympy as sp
import math
import warnings
import statsmodels.api as sm
warnings.filterwarnings('ignore')

data = pd.read_excel('C:\\Users\\Mikhail\\Downloads\\Пересдача по эконометрике.xlsx', sheet_name='Вариант 1', skiprows=[1], usecols='A:B')
data.head()

plt.figure(figsize=(15, 10))

plt.plot(data['T'], data['EMPLDEC_Y'])

plt.title('График исходного ряда')
plt.xlabel('T')
plt.ylabel('EMPLDEC_Y')
plt.grid()

plt.show()

----------------------------------------------

По исходному ряду можно сказать о наличии тренда и сделать вывод о будущем росте
заявленной потребности в рабочих. Сезоннность в ряде не наблюдается,
но присутствуют реские всплески в 2008, 2014, 2021 годах.
Можно сделать предположение о том, что это связанно
с кризисным мировым положением. Экономический кризис
в начале второго десятка 21 века, кризисная ситуация
в 14 и 21 году в западной Европе.
А также можно сказать о росте в 2018 - 2020 годах свзанных с пандемией


По исходному ряду можно сказать о наличии тренда и сделать вывод о будущем росте заявленной потребности в рабочих. Сезоннность в ряде не наблюдается, но присутствуют реские всплески в 2008, 2014, 2021 годах. Можно сделать предположение о том, что это связанно с кризисным мировым положением. Экономический кризис в начале второго десятка 21 века, кризисная ситуация в 14 и 21 году 
в западной Европе. А также можно сказать о росте в 2018 - 2020 годах свзанных с пандемией

----------------------------------------------

y1, y2 = np.array_split(data['EMPLDEC_Y'], 2)
n1, n2 = y1.shape[0], y2.shape[0]

y1_mean, y2_mean = y1.mean(), y2.mean()
sigma_1, sigma_2 = y1.var(), y2.var()

F = sigma_1/sigma_2
F_crit = sts.f(n1-1, n2-1).isf(0.05)

print('Гипотеза принимается') if F < F_crit else print('Гипотеза отвергается')


sigma = np.sqrt(((n1 - 1) * sigma_1 + (n2 - 1) * sigma_2)/(n1 + n2 - 2))
t = abs(y1_mean - y2_mean)/(sigma * np.sqrt(1/n1 + 1/n2))
t_crit = sts.t(n1 + n2 - 2).isf(0.05/2)

print('Тренд отсутствует') if t < t_crit else print('Тренд присутствует')

----------------------------------------------

3. Провести проверку наличия тренда с помощью метода Фостера-Стьюарта. Сравнить выводы двух тестов. (9 баллов)

----------------------------------------------

kt = []
lt = []

for i in range(1, len(data['EMPLDEC_Y'])):
    kt.append(int(data['EMPLDEC_Y'][i] > data['EMPLDEC_Y'][:i].max()))
    lt.append(int(data['EMPLDEC_Y'][i] < data['EMPLDEC_Y'][:i].min()))
    
s = sum(kt) + sum(lt)
d = sum(kt) - sum(lt)

sigma_1 = np.sqrt(2*np.log(data.shape[0]) - 3.4253)
sigma_2 = np.sqrt(2*np.log(data.shape[0]) - 0.8456)

mu = (1.693872*np.log(data.shape[0]) - 0.299015)/(1 - 0.035092*np.log(data.shape[0]) + 0.002705 * data.shape[0])

ts = abs(s - mu)/sigma_1
td = abs(s - 0)/sigma_2


t_crit = sts.t(data.shape[0]-1).isf(0.05/2)

print('Тренд ряда присутствует') if ts > t_crit else print('Тренд ряда отсутствует')

print('Тренд дисперсии присутствует') if td > t_crit else print('Тренд дисперсии отсутствует')

----------------------------------------------

Оба теста показывают наличие тренда.

----------------------------------------------

4. Провести прогнозирование с помощью кривой роста. Рассчитать точечный и интервальный прогноз на 4 периода вперед. (7 баллов)

Y = data['EMPLDEC_Y'].rolling(window=3).mean().dropna().reset_index(drop=True)

delta_y = ((Y.shift(1) - Y.shift(-1))/2).dropna()
delta_2y = ((delta_y.shift(1) - delta_y.shift(-1))/2).dropna()
exp = delta_y/Y.dropna()
ln = np.log(delta_y)
gp = np.log(exp)
lg = np.log(delta_y/Y**2).dropna()

plt.scatter(np.arange(1, len(exp)+1), exp)
plt.scatter(np.arange(1, len(ln)+1), ln)
plt.scatter(np.arange(1, len(gp)+1), gp)
plt.scatter(np.arange(1, len(lg)+1), lg)

data_train, data_test = data.iloc[:-4, :], data.iloc[-4:, :]

X = sm.add_constant(data['T'])
y = np.log(data['EMPLDEC_Y'])

model = sm.OLS(y, X).fit()

print(model.summary())

----------------------------------

X_forecast = np.arange(2022, 2026+1)
forecast = np.exp(model.predict(sm.add_constant(pd.Series(X_forecast))))

Se = np.sqrt(sum((data['EMPLDEC_Y'] - np.exp(model.predict(X)))**2)/(data.shape[0] - 1 - 1))
t = sts.t(data.shape[0] - 2).isf(0.05/2)

upper = []
lower = []

for i in range(len(forecast)):
  Sy = Se * np.sqrt(1 + 1/data.shape[0] + (X_forecast[i] - data['T'].mean())**2/
   (sum((data['T'] - data['T'].mean())**2)))
  U = Sy * t
  upper.append(forecast[i] + U)
  lower.append(forecast[i] - U)
upper = np.array(upper, dtype='float')
lower = np.array(lower, dtype='float')

----------------------------

plt.figure(figsize=(15, 10))
plt.plot(data['T'], data['EMPLDEC_Y'], label = 'Исходный ряд', color='blue')
plt.plot(data['T'], np.exp(model.predict(X)), label = 'Смоделированный ряд', color='green', linestyle='--')
plt.plot(data['T'][2:], Y, label='Сглаженный ряд', color='orange')
plt.plot(X_forecast, forecast, label = 'Предсказание', color='red', linestyle='--')
plt.fill_between(X_forecast, lower, upper, color='grey', alpha=0.6, label='Доверительный интервал')

plt.title('Прогнозирование с помощью кривой роста')
plt.legend(loc='upper left')
plt.grid()
plt.show()""",
        2: "Стьюдента, Ирвина, критерия на медиане, разности средних уровней, Фостера-Стьюарта, средневзвешенной скользящей средней, экспоненциальное сглаживание",
        3: "Системы",
        4: "Панельки, Фишера, Хаусмана, Бреуша-Пагана",
        5: "Логит, пробит",
        6.1: "ARIMA, ARMA",
        6.2: "AR(), MA(3)",
        6.3: "AR(1), MA(2), ARMA(2,3)"
    }

    if option is None:
        return ('1: (Предварительный анализ временных рядов)\n'
                '2: (Стьюдента, Ирвина, критерия на медиане, разности средних уровней, '
                'Фостера-Стьюарта, средневзвешенной скользящей средней, экспоненциальное сглаживание)\n'
                '3: (системы)\n'
                '4: (панельки, Фишера, Хаусмана, Бреуша-Пагана)\n'
                '5: (логит, пробит)\n'
                '6.1: (arima, arma)\n'
                '6.2: (ar(), ma(3))\n'
                '6.3: (ar(1), ma(2), arma(2,3))')
    else:
        print(task_map.get(option, "Некорректная опция. Попробуйте снова."))