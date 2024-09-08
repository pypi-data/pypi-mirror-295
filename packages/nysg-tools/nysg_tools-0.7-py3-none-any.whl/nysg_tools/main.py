import numpy as np
import sympy as sym
from typing import Union, Tuple, Dict
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.odr import ODR, Model, RealData
import inspect


def propagate(
    expr: str,
    N: int = 1000000,
    return_values: bool = False,
    **kwargs: Dict[str, Tuple[float, float]]
) -> Union[Tuple[float, float], np.ndarray]:
    """
    Propaga errores de una operación utilizando el método de Monte Carlo.

    Parámetros:
    -----------
    expr : str
        Expresión de la operación a realizar.

    **kwargs : dict
        Diccionario con los valores de las variables y sus respectivos errores. Cada clave es el nombre de la variable y cada valor es una tupla con el valor y el error de la variable.

    N : int, opcional
        Número de muestras a generar. Por defecto es 1000000.

    return_values : bool, opcional
        Si es True, retorna el array de los valores calculados. Por defecto es False, por ende devuelve el promedio y la desviacion estandar de los mismos.

    Retorna:
    --------
    mu : float
        Promedio de los valores calculados.

    std : float
        Desviación estándar de los valores calculados.


    """

    # Enabling broadcasting for single values of uncertaities
    for var in tuple(kwargs):
        if np.shape(kwargs[var][1]) == (1,):
            short = list(kwargs[var])
            number = short[1]
            short[1] = np.full_like(short[0], number, dtype=np.double)
            kwargs[var] = tuple(short)

    expr = sym.parse_expr(expr)

    variables = tuple(kwargs)

    symbols = sym.symbols(variables)

    a = np.transpose(np.array(tuple(v[0] for v in kwargs.values())))
    b = np.transpose(np.array(tuple(v[1] for v in kwargs.values())))

    dims = np.insert(np.shape(a), 0, N)

    vals = np.random.normal(a, b, dims)

    fval = sym.lambdify(symbols, expr, "numpy")

    calculated = fval(*np.transpose(vals))

    if np.shape(calculated) == (N,):
        mu = np.mean(calculated)
        std = np.std(calculated)
    else:
        mu = np.mean(calculated, axis=1)
        std = np.std(calculated, axis=1)

    if return_values == True:
        return calculated

    return mu, std

    pass


def cont(x, a=1000):
    """Devuelve un array "continuo" del array especificado,
    efectivamente solamente retorna linspace(min(x),max(a),step=a)
    defualt a = 1000
    """
    return np.linspace(np.min(x), np.max(x), a)


def fit_lsq(
    x, y, func, p0=None, a=1000, maxfev=1000, yerr=None, n=3, yap=True, see_res=False
):
    """Realiza un ajuste LSQ a los datos
    parametros:
    x : datax
    y : datay
    func : función a evaluar
    La función debe ser en formato lsq

    yerr : error en y
    p0 : guess inicial de los parametros
    maxfev: iteraciones maximas, default 1000
    a : metodo de ODR utilizado: 0-> ODR explicito, 1-> ODR implicito, 2 -> Lsq comun
    yap : Imprime los valores del ajuste en la terminal (True or False)
    see_res: True or False -> Printea los residuos del ajuste, y un histograma de los mismos

    returns:
    La función devuelve un diccionario con entradas params, err, chi2 y DF

    EJEMPLO DE USO
    x = data_x
    y = data_y
    xerr = data_x_err
    yerr = data_y_err

    def Lineal(x,a,b):
      return a*x + b

    p = Fit_Lsq(x,y,Lineal,yerr = yerr)

    se pueden acceder a los parametros con p['params']
    a los errores con p['err']
    """

    popt, pcov = curve_fit(func, x, y, p0=p0, maxfev=maxfev, sigma=yerr)
    perr = np.sqrt(np.diag(pcov))

    y_pred = func(x, *popt)

    args, *_ = inspect.getfullargspec(func)

    # Ploteo de parámetros:
    if yap == True:

        print("La función es:")  # Ver que función se ajustó
        print(func.__doc__)

        print("Resultados del ajuste:")

        for i in range(len(popt)):
            print(
                "Parámetro "
                + str(args[i + 1])
                + ": "
                + str(np.round(popt[i], n))
                + " ± "
                + str(np.round(perr[i], n))
            )

    # Printeo de histogrma
    if see_res is not False:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.errorbar(x, y - y_pred, fmt="o", label="Datos", yerr=yerr)

        data_hist = ax2.hist(y - y_pred, bins="auto")

        ax2.set_xticks(data_hist[1])
        plt.show()

    # Chi 2 y reducido:

    puntos = len(x)
    params = len(popt)
    v = puntos - params - 1

    if yerr is not None:
        chi2 = np.sum(((y - y_pred) / yerr) ** 2)
        chi2_red = chi2 / v
        if yap == True:
            print("Parametros de bondad:")
            print("ν: " + str(np.round(v, n)))
            print("χ²: " + str(np.round(chi2, n)))
            print("χ²/ν:" + str(np.round(chi2_red, n)))
            print(
                "Criterio 5%: "
                + str(
                    (
                        np.round(v - 1.65 * np.sqrt(2 * v), n),
                        np.round(v + 1.65 * np.sqrt(2 * v), n),
                    )
                )
                + ""
            )
        return {"params": popt, "err": perr, "chi2": chi2, "degrees": v}

    return {"params": popt, "err": perr}


def fit_odr(
    x, y, func, xerr, yerr, p0, maxit=50000, a=0, yap=True, debug_yap=False, n=3
):
    """Realiza un ajuste ODR a los datos
    parametros:
    x : datax
    y : datay
    func : función a evaluar
    La función debe ser en formato odr
    xerr : error en x
    yerr : error en y
    p0 : guess inicial de los parametros
    maxit: iteraciones maximas, default 50000
    a : metodo de ODR utilizado: 0-> ODR explicito, 1-> ODR implicito, 2 -> Lsq comun
    yap : Imprime los valores del ajuste en la terminal (True or False)
    debug_yap : Imprime valores mas especificos del ajutse
    n : Numero de a cuanto se redondea lo que se printea


    returns:
    La función devuelve un diccionario con entradas params, err, chi2 y DF

    EJEMPLO DE USO
    x = data_x
    y = data_y
    xerr = data_x_err
    yerr = data_y_err

    def Lineal(a,x):
      return a[0]*x +a[1]

    p = Fit_ODR(x,y,Lineal,xerr,yerr,p0=[1,1])

    se pueden acceder a los parametros con p['params']
    a los errores con p['err']
    """

    # MODEL
    model = Model(func)
    data = RealData(x, y, sx=xerr, sy=yerr)
    odr = ODR(data, model, p0, maxit=maxit)
    odr.set_job(fit_type=a)
    output = odr.run()
    beta = output.beta
    beta_err = output.sd_beta
    y_pred = func(beta, x)

    # Chi2 y pvalue
    puntos = len(x)
    params = len(beta)
    v = puntos - params - 1

    chi2 = np.sum(((y - y_pred) / yerr) ** 2)
    chi2_red = chi2 / v

    if yap == True:
        print("La función es:")  # Ver que función se ajustó
        print(func.__doc__)

        print("Resultados del ajuste:")
        for i in range(len(beta)):
            print(
                "Parámetro "
                + str(i)
                + ": "
                + str(np.round(beta[i], n))
                + " ± "
                + str(np.round(beta_err[i], n))
            )

        print("Parametros de bondad:")
        print("ν: " + str(np.round(v, n)))
        print("χ²: " + str(np.round(chi2, n)))
        print("χ²/ν:" + str(np.round(chi2_red, n)))
        print(
            "Criterio 5%: "
            + str(
                (
                    np.round(v - 1.65 * np.sqrt(2 * v), n),
                    np.round(v + 1.65 * np.sqrt(2 * v), n),
                )
            )
            + ""
        )

    if debug_yap == True:
        output.pprint()

    return {"params": beta, "err": beta_err, "chi2": chi2, "DF": v}


def fft(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calcula la transformada de Fourier de una señal discreta.

    Parámetros:
    - x: np.ndarray: Vector de tiempo.
    - y: np.ndarray: Vector de amplitud.

    Retorna:
    - frecuencia: np.ndarray: Vector de frecuencia.
    - transformada: np.ndarray: Vector de amplitud de la transformada de Fourier.
    """
    transformada_0 = np.fft.fft(y)
    largo = len(x)  # miro la cantidad de elementos que tiene el vector de tiempos
    d_tiempo = np.mean(np.diff(x))  # miro los diferenciales de tiempo entre mediciones
    frecuencia = np.fft.fftfreq(largo, d_tiempo)  # crea el vector de frecuencias
    transformada = np.abs(
        transformada_0
    )  # le tomo el valor absoluto a la transformada,
    frecuencia = frecuencia[np.arange(largo // 2)]
    transformada = transformada[np.arange(largo // 2)]
    return frecuencia, transformada
