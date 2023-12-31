import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def evaluate_function(function, point):
    """
    функция для вычисления значения функции в заданной точке
    :param function: функция, записанная как строка
    :param point: точка, в которой
    :return: значение функции
    """
    return eval(str(function) + "(" + str(point) + ")")


def progonka(A):
    """
    метод прогонки
    решает систему уравнений
    :param A: система уравнений в виде матрицы
    :return: массив решений уравнения, где на месте с индексом 0 - значение x0
    """
    n = len(A) - 1

    Q = [0] * n
    P = [0] * n
    x = [0] * (n + 1)

    P[0] = A[0][1] / -A[0][0]
    Q[0] = -A[0][-1] / -A[0][0]

    for i in range(1, len(A) - 1):
        P[i] = A[i][1 + i] / (-A[i][i] - A[i][i - 1] * P[i - 1])
        Q[i] = (A[i][i - 1] * Q[i - 1] - A[i][-1]) / (-A[i][i] - A[i][i - 1] * P[i - 1])

    x[n] = (A[n][n - 1] * Q[n - 1] - A[n][-1]) / (-A[n][n] - A[n][n - 1] * P[n - 1])
    for i in range(n - 1, -1, -1):
        x[i] = round(P[i] * x[i + 1] + Q[i], 5)
    return (x)


def cubic_splain(x, f):
    """
    Метод для нахождения интерполяционного дифференциального кубического сплайна
    :param x: массив со значениями агруметов x0, x1,..., xn
    :param f: массив со значениями функций f0, f1,..., fn в соотв. точках
    :return: вывод сплайн-функции в виде массива полинномов
             вывод графика с начальными точками и значениями, а так же с получившейся сплайн-функцией
    """
    n = len(x) - 1
    # f = []
    h = []
    m = [0] * (n + 1)
    for i in range(n + 1):
        # fi = evaluate_function(y, x[i])
        # f.append(round(fi, 7))
        if i != n:
            h.append(round(x[i + 1] - x[i], 7))
    h.append(h[-1])
    flag = 1
    for i in range(n - 1):
        if h[i] != h[i + 1]:
            flag = 0
            break
    if flag:
        m[0] = round((2 * f[0] - 5 * f[1] + 4 * f[2] - f[3]) / (h[0] ** 2), 7)
        m[n] = round((-f[n - 3] + 4 * f[n - 2] - 5 * f[n - 1] + 2 * f[n]) / (h[0] ** 2), 7)
        A = mas = [[0] * (n + 2) for i in range(n + 1)]
        for i in range(1, n):
            A[i][i - 1] = h[i - 1] / 6
            A[i][i] = (h[i - 1] + h[i]) / 3
            A[i][i + 1] = h[i] / 6
            A[i][-1] = (f[i + 1] - f[i]) / h[i] - (f[i] - f[i - 1]) / h[i - 1]
        A[0][0] = 1
        A[0][-1] = m[0]
        A[n][n] = 1
        A[n][-1] = m[n]
        m = progonka(A)
    S = [0] * n
    """for i in range(n):
        S[i] = f[i] + np.poly1d([x[i]], True) * (1/h[i+1]*(f[i+1]-f[i]) - h[i+1]/2*m[i] - h[i+1]/6*(m[i+1]-m[i])) + m[i]/2*np.poly1d([x[i], x[i]], True) + 1/(6*h[i+1])*(m[i+1] - m[i])*np.poly1d([x[i], x[i], x[i]], True)"""
    for i in range(n):
        S[i] = np.poly1d([1 / (6 * h[i + 1]) * (m[i + 1] - m[i]), m[i] / 2,
                          (1 / h[i + 1] * (f[i + 1] - f[i]) - h[i + 1] / 2 * m[i] - h[i + 1] / 6 * (m[i + 1] - m[i])),
                          f[i]])
    print(S)
    for i in range(n):
        print(
            f"{S[i][0]} + {S[i][0 + 1]} * (x - {x[i]}) + {S[i][0 + 2]} * (x - {x[i]})^2 + {S[i][0 + 3]} * (x - {x[i]})^3")

    plt.title("Интерполяционный кубический сплайн")
    x_interp = np.linspace(np.min(x), np.max(x), 5000)
    plt.plot(x, f, "o", label="Data points")
    plt.plot(x, f, "red", label="First line")

    for i in range(len(S)):
        t = np.linspace(x[i], x[i + 1], 1000)
        plt.plot(t, S[i](t - x[i]), "green")
    plt.plot(0, 0, "green", label="Cubic splain")

    plt.legend()
    plt.show()


def quadratic_spline(x, y):
    """
    Метод для нахождения интерполяционного дифференциального параболического сплайна
    :param x: массив со значениями агруметов x0, x1,..., xn
    :param y: массив со значениями функций y0, y1,..., yn в соотв. точках
    :return: вывод сплайн-функции в виде полинномов
             вывод графика с начальными точками и значениями, а так же с получившейся сплайн-функцией
    """
    n = len(x)
    h = np.diff(x)

    # Создание трехдиагональной матрицы
    A = np.zeros((n, n))
    A[0, 0] = 1
    A[n - 1, n - 1] = 1

    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]

    # Создание вектора свободных членов
    B = np.zeros(n)

    for i in range(1, n - 1):
        B[i] = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])

    # Решение системы линейных уравнений
    c = np.linalg.solve(A, B)

    # Вычисление коэффициентов a, b и c
    a = np.zeros(n - 1)
    b = np.zeros(n - 1)

    for i in range(n - 1):
        a[i] = (c[i + 1] - c[i]) / (3 * h[i])
        b[i] = (y[i + 1] - y[i]) / h[i] - (h[i] / 3) * (2 * c[i] + c[i + 1])
        # d[i] = y[i]


    for i in range(len(a)):
        print(f"Уравнение сплайна {i + 1}: {a[i]}x^2 + {b[i]}x + {c[i]}")

    plt.title("Интерполяционный параболический сплайн")
    x_interp = np.linspace(np.min(x), np.max(x), 5000)
    plt.plot(x, y, "o", label="Data points")
    plt.plot(x, y, "red", label="First line")
    x_interp = np.linspace(np.min(x), np.max(x), 50)
    y_parabolic = interp1d(x, y, kind="quadratic")
    plt.plot(x_interp, y_parabolic(x_interp), "green", label="Parabolic spline")

    plt.legend()
    plt.show()


def restoring(x, I, funk = None, f =None, y_min = None, y_max = None):
    """
    метод для нахождения восстанавливающего интегрально-дифференциального параболического сплайна
    :param x: массив со значениями агруметов x0, x1,..., xn
    :param I: массив со значениями интегралов I{0,1}, I{1, 2},..., I{n-2, n-1}
    :param funk: используется при вызове данного метода из методов interpolated и smothing
                 необходим для распознования названия метода, из которого его вызывают
    :param f: используется при вызове данного метода из метода interpolated.
              массив со значениями функций f0, f1,..., fn в соотв. точках
    :param y_min: используется при вызове данного метода из метода smothing.
                  массив со значениями функций y_min в соотв. точках
    :param y_max: используется при вызове данного метода из метода smothing.
                  массив со значениями функций y_max в соотв. точках
    :return: вывод сплайн-функции в виде массива полинномов
             вывод графика с начальными точками и значениями интегралов, а так же с получившейся сплайн-функцией
    """
    n = len(x) - 1
    h = x[1] - x[0]
    A = [[0] * (n + 2) for i in range(n + 1)]
    for i in range(1, n):
        A[i][i - 1] = 1 / h
        A[i][i] = 4 / h
        A[i][i + 1] = 1 / h
        A[i][-1] = 3 * (I[i - 1] + I[i])
    A[0][0] = 1
    A[0][1] = 2
    A[0][-1] = (5 / h ** 2 * I[0] + 1 / h ** 2 * I[1]) / 2
    A[n][n] = 1
    A[n][n - 1] = 2
    A[n][-1] = (5 / h ** 2 * I[n-1] + 1 / h ** 2 * I[n-2]) / 2
    for a in A:
        print(a)
    m = progonka(A)
    S = [0] * n
    """for i in range(n):
        S[i] = f[i] + np.poly1d([x[i]], True) * (1/h[i+1]*(f[i+1]-f[i]) - h[i+1]/2*m[i] - h[i+1]/6*(m[i+1]-m[i])) + m[i]/2*np.poly1d([x[i], x[i]], True) + 1/(6*h[i+1])*(m[i+1] - m[i])*np.poly1d([x[i], x[i], x[i]], True)"""
    for i in range(n):
        S[i] = np.poly1d([-6 / h ** 3 * (I[i] - h * m[i]) + 3 / h ** 2 * (m[i + 1] - m[i]),
                          6 / h ** 2 * (I[i] - h * m[i]) - 2 / h * (m[i + 1] - m[i]), m[i]])
    for i in range(n):
        print(f"{S[i][0]} + {S[i][0 + 1]} * (x - {x[i]}) + {S[i][0 + 2]} * (x - {x[i]})^2")

    if funk == None:
        plt.title("Интерполяционный восстанавливающий сплайн")
        x_interp = np.linspace(np.min(x), np.max(x), 5000)
        # plt.plot(x, I, "o", label="Data points")
        for i in range(len(I)):
            xi = np.linspace(x[i], x[i + 1])
            plt.plot(x[i], I[i], "o", color="pink")
            plt.plot(x[i + 1], I[i], "o", color="pink")
            plt.plot([x[i], x[i + 1]], [I[i], I[i]], "red")
        plt.plot(0, 0, "o", label="Data  points", color="pink")
        plt.plot(0, 0, "red", label="First line")

        for i in range(len(S)):
            t = np.linspace(x[i], x[i + 1], 1000)
            plt.plot(t, S[i](t - x[i]), "green")
        plt.plot(0, 0, "green", label="Restoring spline")

    elif funk == "interpolated":
        plt.title("Интерполяционный сплайн")
        x_interp = np.linspace(np.min(x), np.max(x), 5000)
        plt.plot(x, f, "o", label="Data points")
        plt.plot(x, f, "red", label="First line")

        for i in range(len(I)):
            plt.plot(x[i + 1], I[i], "o", color="pink")
            plt.plot([x[i], x[i + 1]], [I[i], I[i]], "red")
        plt.plot(0, 0, "red", label="Integral")

        for i in range(len(S)):
            t = np.linspace(x[i], x[i + 1], 1000)
            plt.plot(t, S[i](t - x[i]), "green")
        plt.plot(0, 0, "green", label="Interpolated splain")

    elif funk =="smothing":
        plt.title("Сглаживающий сплайн")
        x_interp = np.linspace(np.min(x), np.max(x), 5000)
        plt.plot(x, y_min, "o", label="Data points")
        plt.plot(x, y_min, "red", label="First min line")
        plt.plot(x, y_max, "o", label="Data points")
        plt.plot(x, y_max, "red", label="First max line")

        for i in range(len(I)):
            plt.plot(x[i + 1], I[i], "o", color="pink")
            plt.plot([x[i], x[i + 1]], [I[i], I[i]], "red")
        plt.plot(0, 0, "red", label="Integral")

        for i in range(len(S)):
            t = np.linspace(x[i], x[i + 1], 1000)
            plt.plot(t, S[i](t - x[i]), "green")
        plt.plot(0, 0, "green", label="Smothing splain")

    plt.legend()
    plt.show()


def interpolated(x, f, flag = None):
    """
    метод для нахождения интерполяционного интегрально-дифференциального параболического сплайна
    :param x: массив со значениями агруметов x0, x1,..., xn
    :param f: массив со значениями функций f0, f1,..., fn в соотв. точках
    :param flag: используется при вызове данного метода из метода smothing.
                 если flag = 1, значит метод был вызван из метода smothing
    :return: вывод сплайн-функции в виде массива полинномов
             вывод графика с начальными точками и значениями, а так же с получившейся сплайн-функцией и найденными значениями интегралов
    """
    n = len(x) - 1
    h = []
    for i in range(n):
        h.append(round(x[i + 1] - x[i], 7))
    h.append(h[-1])
    A = [[0] * (n + 1) for i in range(n + 1)]

    for i in range(1, n):
        A[i][i - 1] = (h[i + 1] / h[i]) ** 2
        A[i][i] = 1
        A[i][-1] = (h[i + 1]) ** 3 / 3 * (f[i - 1] / h[i] + 2 * (1 / h[i] + 1 / h[i + 1]) * f[i] + f[i + 1] / h[i + 1])
    A[0][0] = 1
    A[0][-1] = h[i] ** 3 / (6 * (h[i] + h[i + 1])) * (
            (2 * h[i] + 3 * h[i + 1]) / h[i] * f[i - 1] + (h[i] + h[i + 1]) * (h[i] + 3 * h[i + 1]) / (
            h[i] ** 2 * h[i + 1]) * f[i] - f[i + 1] / h[i + 1])
    A[n][n] = 1
    A[n][-1] = h[i] ** 3 / (6 * (h[i] + h[i + 1])) * (
            (3 * h[i] + 2 * h[i + 1]) / h[i + 1] * f[i + 1] + (h[i] + h[i + 1]) * (3 * h[i] + h[i + 1]) / (
            h[i] * h[i + 1] ** 2) * f[i] - f[i - 1] / h[i] ** 2)

    I = progonka(A)
    I = I[0:-1]
    if flag == 1:
        return (I)
    else:
        restoring(x, I, funk = "interpolated", f = f)


def smothing(x, f, eps):
    """
    метод для нахождения сглаживающего интегрально-дифференциального параболического сплайна
    :param x: массив со значениями агруметов x0, x1,..., xn
    :param f: массив со значениями функций f0, f1,..., fn в соотв. точках
    :param eps: массив со значеними погрешностей eps0, eps1, ..., epsn
    :return: вывод сплайн-функции в виде массива полинномов
             вывод графика с начальными точками и  максимальными и минимальными значениями,
             а так же с получившейся сплайн-функцией и найденными максимальными и минимальными значениями интегралов
    """
    n = len(x)
    y_min = [0] * n
    y_max = [0] * n
    for i in range(n):
        y_min[i] = f[i] - eps[i]
        y_max[i] = f[i] + eps[i]
    I_min = interpolated(x, y_min, flag = 1)
    I_max = interpolated(x, y_max, flag = 1)
    I_avg = np.array([])
    for i in range(len(I_max)):
        I_avg = np.append(I_avg, (I_max[i] + I_min[i]) / 2)
    restoring(x, I_avg, funk = "smothing", f = f, y_min = y_min, y_max = y_max)


#ТЕСТЫ
#ИНТЕРПОЛЯЦИОННО-ДИФФЕРЕНЦИАЛЬНЫЙ КУБИНСКИЙ СПЛАЙН
x = np.array([0, math.pi/6, math.pi/3, math.pi/2, 2*math.pi/3, 5*math.pi/6, math.pi])
f = np.array([1, math.sqrt(3)/2, 1/2, 0, -1/2, -math.sqrt(3)/2, -1])
#cubic_splain(x, f)

#ИНТЕРПОЛЯЦИОННО-ДИФФЕРЕНЦИАЛЬНЫЙ ПАРАБОЛИЧЕСКИЙ СПЛАЙН
x = np.array([0,1, 2, 3, 4])
f = np.array([7, 6, 8, 9, 3])
#quadratic_spline(x, f)

#ВОССТАНАВЛИВАЮЩИЙ ИНТЕГРАЛЬНО-ДИФФЕРЕНЦИАЛЬНЫЙ ПАРАБОЛИЧЕСКИЙ СПЛАЙН
x = np.array([0, 1, 2, 3, 4])
I = np.array([-0.6666666666, 7.3333333333, 44.3333333333, 159.363])
#restoring(x, I)

#ИНТЕРПОЛЯЦИОННЫЙ ИНТЕГРАЛЬНО-ДИФФЕРЕНЦИАЛЬНЫЙ ПАРАБОЛИЧЕСКИЙ СПЛАЙН
x = np.array([0, 1, 2, 3, 4])
f = np.array([3, 5, 8, 12, 15])
#interpolated(x, f)

#СГЛАЖИВАЮЩИЙ ИНТЕГРАЛЬНО-ДИФФЕРЕНЦИАЛЬНЫЙ ПАРАБОЛИЧЕСКИЙ СПЛАЙН
x = [0, 1, 2, 3, 4]
f = [5, 12, -3, 7, 9]
eps = [1, 2, 1, 2, 1]
#smothing(x, f, eps)

