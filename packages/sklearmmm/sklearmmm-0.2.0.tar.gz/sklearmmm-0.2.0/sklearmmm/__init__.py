import os
from PIL import Image as PILImage
from IPython.display import display, Image

# Получение пути к директории с изображениями
package_dir = os.path.dirname(__file__)
image_dir = os.path.join(package_dir, "images")

def p(option=None):
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
        return task_map.get(option, "Некорректная опция. Попробуйте снова.")


image_map = {
        1: [os.path.join(image_dir, "001_1.png"), os.path.join(image_dir, "001_2.png")],
        2: [os.path.join(image_dir, "002_1.png"), os.path.join(image_dir, "002_2.png")],
        3: [os.path.join(image_dir, "003_1.png"), os.path.join(image_dir, "003_2.png")],
        4: [os.path.join(image_dir, "004_1.png"), os.path.join(image_dir, "004_2.png")],
        5: [os.path.join(image_dir, "005_1.png"), os.path.join(image_dir, "005_2.png"), os.path.join(image_dir, "005_3.png")],
        6: [os.path.join(image_dir, "006_1.png"), os.path.join(image_dir, "006_2.png")],
        7: [os.path.join(image_dir, "007_1.png"), os.path.join(image_dir, "007_2.png")],
        8: [os.path.join(image_dir, "008_1.png"), os.path.join(image_dir, "008_2.png")],
        9: [os.path.join(image_dir, "009_1.png"), os.path.join(image_dir, "009_2.png")],
        10: [os.path.join(image_dir, "010_1.png"), os.path.join(image_dir, "010_2.png")],
        11: [os.path.join(image_dir, "011_1.png")],
        12: [os.path.join(image_dir, "012_1.png"), os.path.join(image_dir, "012_2.png")],
        13: [os.path.join(image_dir, "013_1.png"), os.path.join(image_dir, "013_2.png")],
        14: [os.path.join(image_dir, "014_1.png")],
        15: [os.path.join(image_dir, "015_1.png")],
        16: [os.path.join(image_dir, "016_1.png")],
        17: [os.path.join(image_dir, "017_1.png"), os.path.join(image_dir, "017_2.png")],
        18: [os.path.join(image_dir, "018_1.png")],
        19: [os.path.join(image_dir, "019_1.png"), os.path.join(image_dir, "019_2.png")],
        20: [os.path.join(image_dir, "020_1.png"), os.path.join(image_dir, "020_2.png"), os.path.join(image_dir, "020_3.png")],
        21: [os.path.join(image_dir, "021_1.png")],
        22: [os.path.join(image_dir, "022_1.png"), os.path.join(image_dir, "022_2.png"), os.path.join(image_dir, "022_3.png")],
        23: [os.path.join(image_dir, "023_1.png"), os.path.join(image_dir, "023_2.png")],
        24: [os.path.join(image_dir, "024_1.png"), os.path.join(image_dir, "024_2.png")],
        25: [os.path.join(image_dir, "025_1.png")],
        26: [os.path.join(image_dir, "026_1.png")],
        27: [os.path.join(image_dir, "027_1.png")],
        28: [os.path.join(image_dir, "028_1.png")],
        29: [os.path.join(image_dir, "029_1.png")],
        30: [os.path.join(image_dir, "030_1.png"), os.path.join(image_dir, "030_2.png")],
        31: [os.path.join(image_dir, "031_1.png"), os.path.join(image_dir, "031_2.png"), os.path.join(image_dir, "031_3.png")],
        32: [os.path.join(image_dir, "032_1.png"), os.path.join(image_dir, "032_2.png"), os.path.join(image_dir, "032_3.png")],
        33: [os.path.join(image_dir, "033_1.png")],
        34: [os.path.join(image_dir, "034_1.png"), os.path.join(image_dir, "034_2.png")],
        35: [os.path.join(image_dir, "035_1.png"), os.path.join(image_dir, "035_2.png")],
        36: [os.path.join(image_dir, "036_1.png"), os.path.join(image_dir, "036_2.png")],
        37: [os.path.join(image_dir, "037_1.png"), os.path.join(image_dir, "037_2.png"), os.path.join(image_dir, "037_3.png"), os.path.join(image_dir, "037_4.png")],
        38: [os.path.join(image_dir, "038_1.png")],
        39: [os.path.join(image_dir, "039_1.png"), os.path.join(image_dir, "039_2.png")],
        40: [os.path.join(image_dir, "040_1.png"), os.path.join(image_dir, "040_2.png"), os.path.join(image_dir, "040_3.png")],
        41: [os.path.join(image_dir, "041_1.png")],
        42: [os.path.join(image_dir, "042_1.png")],
        43: [os.path.join(image_dir, "043_1.png")],
        44: [os.path.join(image_dir, "044_1.png"), os.path.join(image_dir, "044_2.png")],
        45: [os.path.join(image_dir, "045_1.png")],
        46: [os.path.join(image_dir, "046_1.png"), os.path.join(image_dir, "046_2.png")],
        47: [os.path.join(image_dir, "047_1.png")],
        48: [os.path.join(image_dir, "048_1.png"), os.path.join(image_dir, "048_2.png")],
        49: [os.path.join(image_dir, "049_1.png"), os.path.join(image_dir, "049_2.png")],
        50: [os.path.join(image_dir, "050_1.png"), os.path.join(image_dir, "050_2.png")],
        51: [os.path.join(image_dir, "051_1.png"), os.path.join(image_dir, "051_2.png")],
        52: [os.path.join(image_dir, "052_1.png"), os.path.join(image_dir, "052_2.png"), os.path.join(image_dir, "052_3.png")],
        53: [os.path.join(image_dir, "053_1.png"), os.path.join(image_dir, "053_2.png")],
        54: [os.path.join(image_dir, "054_1.png"), os.path.join(image_dir, "054_2.png")],
        55: [os.path.join(image_dir, "055_1.png")],
        56: [os.path.join(image_dir, "056_1.png"), os.path.join(image_dir, "056_2.png"), os.path.join(image_dir, "056_3.png")],
        57: [os.path.join(image_dir, "057_1.png"), os.path.join(image_dir, "057_2.png"), os.path.join(image_dir, "057_3.png")],
        58: [os.path.join(image_dir, "058_1.png")],
        59: [os.path.join(image_dir, "059_1.png")],
        60: [os.path.join(image_dir, "060_1.png"), os.path.join(image_dir, "060_2.png")],
        61: [os.path.join(image_dir, "061_1.png")],
        62: [os.path.join(image_dir, "062_1.png"), os.path.join(image_dir, "062_2.png")],
        63: [os.path.join(image_dir, "063_1.png"), os.path.join(image_dir, "063_2.png"), os.path.join(image_dir, "063_3.png"), os.path.join(image_dir, "063_4.png")],
        64: [os.path.join(image_dir, "064_1.png"), os.path.join(image_dir, "064_2.png")],
        65: [os.path.join(image_dir, "065_1.png")],
        66: [os.path.join(image_dir, "066_1.png")],
        67: [os.path.join(image_dir, "067_1.png"), os.path.join(image_dir, "067_2.png")],
        68: [os.path.join(image_dir, "068_1.png"), os.path.join(image_dir, "068_2.png")],
        69: [os.path.join(image_dir, "069_1.png"), os.path.join(image_dir, "069_2.png"), os.path.join(image_dir, "069_3.png")],
        70: [os.path.join(image_dir, "070_1.png"), os.path.join(image_dir, "070_2.png"), os.path.join(image_dir, "070_3.png")],
        71: [os.path.join(image_dir, "071_1.png")],
        72: [os.path.join(image_dir, "072_1.png"), os.path.join(image_dir, "072_2.png")],
        73: [os.path.join(image_dir, "073_1.png"), os.path.join(image_dir, "073_2.png")],
        74: [os.path.join(image_dir, "074_1.png"), os.path.join(image_dir, "074_2.png")],
        75: [os.path.join(image_dir, "075_1.png"), os.path.join(image_dir, "075_2.png")],
        76: [os.path.join(image_dir, "076_1.png"), os.path.join(image_dir, "076_2.png")],
        77: [os.path.join(image_dir, "077_1.png"), os.path.join(image_dir, "077_2.png")],
        78: [os.path.join(image_dir, "078_1.png"), os.path.join(image_dir, "078_2.png")],
        79: [os.path.join(image_dir, "079_1.png")],
        80: [os.path.join(image_dir, "080_1.png"), os.path.join(image_dir, "080_2.png")],
        81: [os.path.join(image_dir, "081_1.png")],
        82: [os.path.join(image_dir, "082_1.png"), os.path.join(image_dir, "082_2.png")],
        83: [os.path.join(image_dir, "083_1.png"), os.path.join(image_dir, "083_2.png"), os.path.join(image_dir, "083_3.png"), os.path.join(image_dir, "083_4.png"), os.path.join(image_dir, "083_5.png")],
        84: [os.path.join(image_dir, "084_1.png"), os.path.join(image_dir, "084_2.png")],
        85: [os.path.join(image_dir, "085_1.png"), os.path.join(image_dir, "085_2.png")],
        86: [os.path.join(image_dir, "086_1.png"), os.path.join(image_dir, "086_2.png")],
        87: [os.path.join(image_dir, "087_1.png"), os.path.join(image_dir, "087_2.png"), os.path.join(image_dir, "087_3.png")],
        88: [os.path.join(image_dir, "088_1.png"), os.path.join(image_dir, "088_2.png")],
        89: [os.path.join(image_dir, "089_1.png"), os.path.join(image_dir, "089_2.png"), os.path.join(image_dir, "089_3.png")],
        90: [os.path.join(image_dir, "090_1.png"), os.path.join(image_dir, "090_2.png")],
        91: [os.path.join(image_dir, "091_1.png")],
        92: [os.path.join(image_dir, "092_1.png"), os.path.join(image_dir, "092_2.png")],
        93: [os.path.join(image_dir, "093_1.png"), os.path.join(image_dir, "093_2.png")],
        94: [os.path.join(image_dir, "094_1.png")],
        95: [os.path.join(image_dir, "095_1.png"), os.path.join(image_dir, "095_2.png")],
        96: [os.path.join(image_dir, "096_1.png"), os.path.join(image_dir, "096_2.png"), os.path.join(image_dir, "096_3.png")],
        97: [os.path.join(image_dir, "097_1.png"), os.path.join(image_dir, "097_2.png")],
        98: [os.path.join(image_dir, "098_1.png"), os.path.join(image_dir, "098_2.png")],
        99: [os.path.join(image_dir, "099_1.png"), os.path.join(image_dir, "099_2.png"), os.path.join(image_dir, "099_3.png")],
        100: [os.path.join(image_dir, "100_1.png")],
        101: [os.path.join(image_dir, "101_1.png")],
        102: [os.path.join(image_dir, "102_1.png")],
        103: [os.path.join(image_dir, "103_1.png"), os.path.join(image_dir, "103_2.png")],
        104: [os.path.join(image_dir, "104_1.png"), os.path.join(image_dir, "104_2.png"), os.path.join(image_dir, "104_3.png"), os.path.join(image_dir, "104_4.png")],
        105: [os.path.join(image_dir, "105_1.png"), os.path.join(image_dir, "105_2.png")],
        106: [os.path.join(image_dir, "106_1.png")],
        107: [os.path.join(image_dir, "107_1.png")],
        108: [os.path.join(image_dir, "108_1.png")],
        109: [os.path.join(image_dir, "109_1.png"), os.path.join(image_dir, "109_2.png")],
        110: [os.path.join(image_dir, "110_1.png")],
        111: [os.path.join(image_dir, "111_1.png")],
        112: [os.path.join(image_dir, "112_1.png"), os.path.join(image_dir, "112_2.png"), os.path.join(image_dir, "112_3.png")],
        113: [os.path.join(image_dir, "113_1.png"), os.path.join(image_dir, "113_2.png")],
        114: [os.path.join(image_dir, "114_1.png"), os.path.join(image_dir, "114_2.png"), os.path.join(image_dir, "114_3.png")],
        115: [os.path.join(image_dir, "115_1.png"), os.path.join(image_dir, "115_2.png"), os.path.join(image_dir, "115_3.png")],
        116: [os.path.join(image_dir, "116_1.png")],
        117: [os.path.join(image_dir, "117_1.png")],
        118: [os.path.join(image_dir, "118_1.png")],
        119: [os.path.join(image_dir, "119_1.png")],
        120: [os.path.join(image_dir, "120_1.png"), os.path.join(image_dir, "120_2.png"), os.path.join(image_dir, "120_3.png"), os.path.join(image_dir, "120_4.png")],
        121: [os.path.join(image_dir, "121_1.png"), os.path.join(image_dir, "121_2.png")]
    }


def t(option=None):
    if option is None:
        return ("""1. Линейная модель множественной регрессии. Основные предпосылки метода наименьших квадратов.
2. Нелинейные модели регрессии. Подходы к оцениванию. Примеры
3. Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Тест Рамсея (тест RESET), условия применения теста.
4. Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Критерий Акаике, Критерий Шварца. условия применения критериев.
5. Гетероскедастичность: определение, причины, последствия. Тест Голдфеда-Квандта и особенности его применения.
6. Гетероскедастичность: определение, причины, последствия. Тест ранговой корреляции Спирмена и особенности его применения.
7. Гетероскедастичность: определение, причины, последствия. Тест Бреуша-Пагана и особенности его применения.
8. Гетероскедастичность: определение, причины, последствия. Тест Глейзера и особенности его применения.
9. Способы корректировки гетероскедастичности: взвешенный метод наименьших квадратов (ВМНК) и особенности его применения.
10. Автокорреляция: определение, причины, последствия. Тест Дарбина-Уотсона и особенности его применения.
11. Автокорреляция: определение, причины, последствия. Тест Бройша – Годфри и особенности его применения.
12.   Автокорреляция: определение, причины, последствия. H – тест и особенности его применения.
13. Автокорреляция: определение, причины, последствия. Метод рядов Сведа-Эйзенхарта и особенности его применения.
14. Модель с автокорреляцией случайного возмущения. Оценка моделей с авторегрессией.
15. Процедура Кохрейна-Оркатта.
16. Процедура Хилдрета – Лу.
17. Оценка влияния факторов, включенных в модель. Коэффициент эластичности, Бета-коэффициент, Дельта – коэффициент.
18. Мультиколлинеарность: понятие, причины и последствия.
19. Алгоритм пошаговой регрессии.
20. Метод главных компонент (PCA) как радикальный метод борьбы с мультиколлинеарностью
21. Выявление мультиколлинеарности: коэффициент увеличения дисперсии (VIF –тест).
22. Выявление мультиколлинеарности: Алгоритм Фаррара-Глобера.
23. Построение гребневой регрессии. Суть регуляризации.
24. Фиктивная переменная и правило её использования.
25. Модель дисперсионного анализа.
26. Модель ковариационного анализа.
27. Фиктивные переменные в сезонном анализе.
28.  Фиктивная переменная сдвига: спецификация регрессионной модели с фиктивной переменной сдвига; экономический смысл параметра при фиктивной переменной; смысл названия.
29. Фиктивная переменная наклона: спецификация регрессионной модели с фиктивной переменной наклона; экономический смысл параметра при фиктивной переменной; смысл названия.
30. Определение структурных изменений в экономике: использование фиктивных переменных, тест Чоу.
31. ​​Модели бинарного выбора. Недостатки линейной модели.
32. Модели множественного выбора: модели с неупорядоченными альтернативными вариантами.
33. Модели усеченных выборок.
34. Модели цензурированных выборок (tobit-модель).
35.   Модели множественного выбора: гнездовые logit-модели.
36.    Модели счетных данных (отрицательная биномиальная модель, hurdle-model)
37. Модели множественного выбора: модели с упорядоченными альтернативными вариантами.
38. Модели случайно усеченных выборок (selection model).
39. Логит-модель. Этапы оценки. Области применения.
40. Пробит-модель. Этапы оценки. Области применения.
41. Метод максимального правдоподобия
42. Свойства оценок метода максимального правдоподобия.
43. Информационная матрица и оценки стандартных ошибок для оценок параметров logit и probit моделей. Интерпретация коэффициентов в моделях бинарного выбора.
44. Мера качества аппроксимации и качества прогноза logit и probit моделей.
45. Временные ряды: определение, классификация, цель и задача моделирования временного ряда.
46.    Исследование структуры одномерного временного ряда.
47.   Процедура выявления аномальных наблюдений на основе метода Ирвина. Особенности применения метода. Анализ аномальных наблюдений.
48. Проверка наличия тренда. Критерий серий, основанный на медиане. Особенности применения метода.
49. Процедура выявления аномальных наблюдений. Причины аномальных значений. Блочные диаграммы по типу «ящика с усами».
50. Проверка наличия тренда. Метод проверки разности средних уровней. Особенности применения метода.
51. Проверка наличия тренда. Метод Фостера-Стьюарта. Особенности применения метода.
52.   Сглаживание временных рядов. Простая (среднеарифметическая) скользящая средняя. Взвешенная (средневзвешенная) скользящая средняя. Среднехронологическая. Экспоненциальное сглаживание.
53. Функциональные зависимости временного ряда. Предварительный анализ временных рядов.
54. Трендовые модели. Без предела роста. Примеры функций. Содержательная интерпретация параметров.
55. Процедура выявления аномальных наблюдений на основе распределения Стьюдента. Особенности применения метода. Анализ аномальных наблюдений.
56. Трендовые модели. С пределом роста без точки перегиба. Примеры функций. Содержательная интерпретация параметров.
57. Трендовые модели. С пределом роста и точкой перегиба или кривые насыщения. Примеры функций. Содержательная интерпретация параметров.
58.  Выбор кривой роста.
59. Прогнозирование с помощью кривой роста.
60.    Прогнозирование временного ряда на основе трендовой модели.
61. Модель Тейла-Вейджа (мультипликативная модель).
62. Метод Четверикова.
63. Моделирование тренд-сезонных процессов. Типы функциональных зависимостей.
64.Мультипликативная (аддитивная) модель ряда динамики при наличии тенденции: этапы построения.
65. Моделирование периодических колебаний (гармоники Фурье).
66. Прогнозирование одномерного временного ряда случайной компоненты (распределение Пуассона).
67. Функциональные преобразования переменных в линейной регрессионной модели. Метод Зарембки. Особенности применения.
68. Функциональные преобразования переменных в линейной регрессионной модели. Тест Бокса-Кокса. Особенности применения.
69. Адаптивная модель прогнозирования Брауна.
70. Функциональные преобразования переменных в линейной регрессионной модели. Критерий Акаике  и Шварца. Особенности применения.
71. Модель Хольта-Уинтерса (адаптивная модель).
72. Функциональные преобразования переменных в линейной регрессионной модели. Тест Бера. Особенности применения.
73. Функциональные преобразования переменных в линейной регрессионной модели. Тест МакАлера. Особенности применения.
74. Функциональные преобразования переменных в линейной регрессионной модели. Тест МакКиннона. Особенности применения.
75. Функциональные преобразования переменных в линейной регрессионной модели. Тест Уайта. Особенности применения.
76. Функциональные преобразования переменных в линейной регрессионной модели. Тест Дэвидсона. Особенности применения.
77. Модели с распределенными лаговыми переменными.
78. Оценка моделей с лагами в независимых переменных. Преобразование Койка
79. ​​Полиномиально распределенные лаги Алмон
80. Авторегрессионные модели.
81. Авторегрессионные модели с распределенными лагами.
82. Стационарные временные ряды. Определения стационарности, лаговой переменной, автоковариационной функции временного ряда, автокоррляционной функции, коррелограммы,  коэффициенты корреляции между разными элементами стационарного временного ряда с временным лагом.
83. Стационарные временные ряды. Определения частной автокорреляционной функции, белого шума, автоковариационная функция для белого шума, ACF для белого шума, частная автокорреляционная функция для белого шума.
84. Модели стационарных временных рядов: модель ARMA(p,q) (классический вид и через лаговый оператор). Авторегрессионный многочлен, авторегрессионная часть и часть скользящего среднего.
85. Модели стационарных временных рядов: модель ARMA(1, q). Доказательство утверждения: Модель ARMA(1, q) стационарна тогда и только тогда, когда |a|<1.
86. Модели стационарных временных рядов: Модель MA(q), Среднее, дисперсия и ACF для MA(q). Модель MA(∞).
87.  Модели стационарных временных рядов: Модель AR(p). Доказательство утверждения: Модель AR(p) определяет стационарный ряд ⇐⇒ выполнено условие стационарности: все корни многочлена a(z) по модулю больше единицы. Модель AR(1).
88. Прогнозирование для модели ARMA. Условия прогнозирования. Периоды прогнозирования. Информативность прогнозов.
89. Оценка и тестирование модели: Предварительное тестирование на белый шум.
90.  Оценка модели и тестирование гипотез временного ряда.
91. Информационные критерии для сравнения моделей и выбора порядка временного ряда: Акаике, Шварца, Хеннана-Куина. Условия их применения.
92. Проверка адекватности модели: тесты на автокорреляцию временного ряда Дарбина-Уотсона, Льюинга-Бокса.
93.    Линейная регрессия для стационарных рядов: Модель FDL.
94. Линейная регрессия для стационарных рядов. Модель ADL.
95. Понятие TS-ряда. Модель линейного тренда. Модель экспоненциального тренда.
96. Нестационарные временные ряды: случайное блуждание, стохастический тренд, случайное блуждание со сносом.
97. Дифференцирование ряда: определение, DS-ряды.
98. Подход Бокса-Дженкинса.
99. Модель ARIMA.
100.   Тест ADF на единичный корень.
101. Модель ARCH.
102. Модель GARCH.
103.  Область применения панельных данных. Преимущества использования панельных данных.
104. Модели панельных данных и основные обозначения.
105. Модель пула (Pool model).
106.  Модель регрессии с фиксированным эффектом (fixed effect model)
107. Модель регрессии со случайным эффектом (random effect model).
108. Тест Бройша-Пагана для панельных данных
109.    Тест Хаусмана для панельных данных.
110. Тест Лагранжа для панельных данных.
111. Вычисление значения оценок параметров β и а в модели с фиксированным эффектом.
112. Отражение пространственных эффектов. Бинарная матрица граничных соседей. Приведите пример.
113. Отражение пространственных эффектов. Бинарная матрица ближайших соседей. Приведите пример.
114. Отражение пространственных эффектов. Матрица расстояний. Приведите пример.
115. Отражение пространственных эффектов. Матрица расстояний с учетом размера объекта. Приведите пример.
117. Пространственная автокорреляция по методологии А. Гетиса и Дж. Орда. Недостатки методологии.
118. Пространственная автокорреляция по методологии Роберта Джири.
119. Пространственная автокорреляция по методологии Морана П.
120. Пространственная кластеризация территорий. Локальный индекс автокорреляции П. Морана (Ili)
121. Матрица взаимовлияния Л. Анселина (LISA).""")




    else:

            try:

                    # Получаем список путей к изображениям для задачи

                    image_paths = image_map.get(option)

                    if image_paths:

                            # Выводим каждое изображение в ячейке Jupyter Notebook

                            for image_path in image_paths:
                                    display(Image(filename=image_path))  # Отображаем изображение

                            return f"Показаны изображения для задачи {option}."

                    else:

                            return "Изображения для данной задачи не найдены."

            except ValueError:

                    return "Некорректная опция. Попробуйте снова."
