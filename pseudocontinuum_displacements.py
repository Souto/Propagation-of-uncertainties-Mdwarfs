import pandas as pd
import numpy as np

# Dados da tabela para A(Fe) from Fe I lines
table_feI_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.147, -0.072, 0.072, 0.137],
    3900: [-0.181, -0.088, 0.084, 0.157],
    3800: [-0.209, -0.098, 0.088, 0.168],
    3700: [-0.335, -0.160, 0.119, 0.209],
    3600: [-0.287, -0.135, 0.119, 0.206],
    3500: [-0.334, -0.163, 0.136, 0.226],
    3400: [-0.227, -0.113, 0.111, 0.211],
    3300: [-0.316, -0.155, 0.085, 0.156],
    3200: [-0.316, -0.155, 0.085, 0.156]
}

# Dados da tabela para A(Fe) from FeH lines
table_feH_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.224, -0.124, 0.100, 0.178],
    3900: [-0.226, -0.119, 0.099, 0.177],
    3800: [-0.227, -0.118, 0.098, 0.176],
    3700: [-0.252, -0.132, 0.101, 0.180],
    3600: [-0.226, -0.115, 0.079, 0.137],
    3500: [-0.190, -0.112, 0.083, 0.144],
    3400: [-0.196, -0.107, 0.083, 0.143],
    3300: [-0.202, -0.098, 0.099, 0.175],
    3200: [-0.177, -0.099, 0.078, 0.158]
}

table_oh_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.033, -0.015, 0.027, 0.060],
    3900: [-0.031, -0.015, 0.026, 0.061],
    3800: [-0.027, -0.012, 0.028, 0.072],
    3700: [-0.033, -0.016, 0.037, 0.081],
    3600: [-0.040, -0.023, 0.036, 0.075],
    3500: [-0.057, -0.030, 0.022, 0.062],
    3400: [-0.056, -0.024, 0.017, 0.059],
    3300: [-0.055, -0.024, 0.030, 0.068],
    3200: [-0.065, -0.029, 0.025, 0.056]
}

table_h2o_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [0, 0, 0, 0],
    3900: [-0.087, -0.020, 0.037, 0.100],
    3800: [-0.087, -0.020, 0.037, 0.100],
    3700: [-0.073, -0.019, 0.019, 0.063],
    3600: [-0.068, -0.016, 0.014, 0.048],
    3500: [-0.049, -0.021, 0.013, 0.043],
    3400: [-0.049, -0.021, 0.013, 0.043],
    3300: [-0.039, -0.013, 0.021, 0.056],
    3200: [-0.039, -0.013, 0.021, 0.056]
}

table_co_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [0.024, -0.001, 0.018, 0.034],
    3900: [-0.107, -0.131, 0.017, 0.033],
    3800: [-0.363, -0.132, 0.018, 0.035],
    3700: [-0.123, -0.059, 0.046, 0.075],
    3600: [-0.093, -0.047, 0.046, 0.079],
    3500: [-0.099, -0.043, 0.047, 0.096],
    3400: [-0.082, -0.031, 0.034, 0.084],
    3300: [-0.070, -0.024, 0.023, 0.062],
    3200: [-0.011, -0.007, 0.009, 0.023]
}

table_na_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.455, -0.223, 0.061, 0.111],
    3900: [-0.428, -0.170, 0.064, 0.116],
    3800: [-0.417, -0.172, 0.063, 0.117],
    3700: [-0.199, -0.138, 0.099, 0.139],
    3600: [-0.199, -0.138, 0.099, 0.139],
    3500: [-0.199, -0.138, 0.099, 0.139],
    3400: [-0.417, -0.172, 0.063, 0.117],
    3300: [-0.111, -0.073, 0.145, 0.295],
    3200: [-0.067, -0.039, 0.064, 0.162]
}

table_mg_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.108, -0.028, 0.061, 0.122],
    3900: [-0.088, -0.026, 0.094, 0.158],
    3800: [-0.113, -0.021, 0.112, 0.182],
    3700: [-0.201, -0.041, 0.010, 0.088],
    3600: [-0.172, -0.084, 0.081, 0.156],
    3500: [-0.184, -0.090, 0.105, 0.205],
    3400: [-0.246, -0.103, 0.090, 0.170],
    3300: [-0.224, -0.114, 0.093, 0.192],
    3200: [-0.328, -0.139, 0.103, 0.190]
}

table_al_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.110, -0.058, 0.057, 0.106],
    3900: [-0.127, -0.062, 0.054, 0.112],
    3800: [-0.117, -0.071, 0.059, 0.121],
    3700: [-0.143, -0.089, 0.061, 0.129],
    3600: [-0.157, -0.076, 0.071, 0.141],
    3500: [-0.126, -0.042, 0.048, 0.087],
    3400: [-0.223, -0.056, 0.048, 0.090],
    3300: [-0.156, -0.092, 0.021, 0.068],
    3200: [-0.177, -0.083, 0.042, 0.100]
}

table_si_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.140, -0.071, 0.072, 0.131],
    3900: [-0.103, -0.080, 0.084, 0.118],
    3800: [-0.071, -0.032, 0.092, 0.162],
    3700: [-0.177, -0.074, 0.124, 0.211],
    3600: [-0.226, -0.115, 0.106, 0.196],
    3500: [-0.284, -0.146, 0.133, 0.240],
    3400: [-0.447, -0.211, 0.192, 0.325],
    3300: [-0.224, -0.099, 0.093, 0.192],
    3200: [-0.224, -0.099, 0.093, 0.192]
}

table_k_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.101, -0.050, 0.047, 0.091],
    3900: [-0.105, -0.051, 0.049, 0.096],
    3800: [-0.111, -0.055, 0.052, 0.102],
    3700: [-0.118, -0.057, 0.055, 0.107],
    3600: [-0.103, -0.050, 0.048, 0.095],
    3500: [-0.103, -0.050, 0.048, 0.095],
    3400: [-0.099, -0.048, 0.047, 0.092],
    3300: [-0.098, -0.048, 0.046, 0.091],
    3200: [-0.093, -0.046, 0.045, 0.088]
}

table_ca_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.070, -0.040, 0.029, 0.068],
    3900: [-0.083, -0.040, 0.040, 0.082],
    3800: [-0.082, -0.039, 0.040, 0.082],
    3700: [-0.096, -0.047, 0.046, 0.094],
    3600: [-0.080, -0.043, 0.039, 0.082],
    3500: [-0.099, -0.053, 0.050, 0.103],
    3400: [-0.123, -0.066, 0.052, 0.111],
    3300: [-0.139, -0.081, 0.061, 0.136],
    3200: [-0.106, -0.100, 0.093, 0.201]
}

table_ti_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.147, -0.073, 0.060, 0.115],
    3900: [-0.150, -0.074, 0.063, 0.119],
    3800: [-0.152, -0.075, 0.063, 0.121],
    3700: [-0.166, -0.082, 0.070, 0.132],
    3600: [-0.137, -0.070, 0.067, 0.128],
    3500: [-0.126, -0.063, 0.062, 0.119],
    3400: [-0.129, -0.065, 0.066, 0.127],
    3300: [-0.134, -0.069, 0.068, 0.132],
    3200: [-0.138, -0.070, 0.070, 0.136]
}

table_v_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.265, -0.124, 0.084, 0.139],
    3900: [-0.265, -0.125, 0.089, 0.147],
    3800: [-0.281, -0.135, 0.099, 0.162],
    3700: [-0.338, -0.192, 0.164, 0.253],
    3600: [-0.365, -0.209, 0.157, 0.237],
    3500: [-0.336, -0.185, 0.232, 0.394],
    3400: [0, 0, 0, 0],
    3300: [0, 0, 0, 0],
    3200: [0, 0, 0, 0]
}

table_cr_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.193, -0.091, 0.074, 0.130],
    3900: [-0.219, -0.103, 0.083, 0.144],
    3800: [-0.267, -0.126, 0.099, 0.168],
    3700: [-0.310, -0.208, 0.169, 0.261],
    3600: [0, 0, 0, 0],
    3500: [0, 0, 0, 0],
    3400: [0, 0, 0, 0],
    3300: [0, 0, 0, 0],
    3200: [0, 0, 0, 0]
}

table_mn_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.146, -0.071, 0.064, 0.121],
    3900: [-0.172, -0.083, 0.072, 0.137],
    3800: [-0.212, -0.101, 0.085, 0.156],
    3700: [-0.306, -0.143, 0.104, 0.180],
    3600: [-0.427, -0.190, 0.122, 0.208],
    3500: [-0.541, -0.265, 0.140, 0.245],
    3400: [0, 0, 0, 0],
    3300: [0, 0, 0, 0],
    3200: [0, 0, 0, 0]
}

table_ni_data = {
    'Pseudocontinuum Displacement': ['−2%', '−1%', '+1%', '+2%'],
    4000: [-0.500, -0.345, 0.223, 0.321],
    3900: [-0.456, -0.272, 0.277, 0.398],
    3800: [-0.490, -0.304, 0.264, 0.411],
    3700: [-0.574, -0.342, 0.248, 0.327],
    3600: [0, 0, 0, 0],
    3500: [0, 0, 0, 0],
    3400: [0, 0, 0, 0],
    3300: [0, 0, 0, 0],
    3200: [0, 0, 0, 0]
}

# Criando DataFrames
df_table_feI = pd.DataFrame(table_feI_data)
df_table_feH = pd.DataFrame(table_feH_data)
df_table_oh = pd.DataFrame(table_oh_data)
df_table_h2o = pd.DataFrame(table_h2o_data)
df_table_co = pd.DataFrame(table_co_data)
df_table_na = pd.DataFrame(table_na_data)
df_table_mg = pd.DataFrame(table_mg_data)
df_table_al = pd.DataFrame(table_al_data)
df_table_si = pd.DataFrame(table_si_data)
df_table_k = pd.DataFrame(table_k_data)
df_table_ca = pd.DataFrame(table_ca_data)
df_table_ti = pd.DataFrame(table_ti_data)
df_table_v = pd.DataFrame(table_v_data)
df_table_cr = pd.DataFrame(table_cr_data)
df_table_mn = pd.DataFrame(table_mn_data)
df_table_ni = pd.DataFrame(table_ni_data)

# Dicionário de DataFrames
dataframes = {
    'Fe': df_table_feI,
    'FeH': df_table_feH,
    'OH': df_table_oh,
    'H2O': df_table_h2o,
    'CO': df_table_co,
    'Na': df_table_na,
    'Mg': df_table_mg,
    'Al': df_table_al,
    'Si': df_table_si,
    'K': df_table_k,
    'Ca': df_table_ca,
    'Ti': df_table_ti,
    'V': df_table_v,
    'Cr': df_table_cr,
    'Mn': df_table_mn,
    'Ni': df_table_ni
    # Adicione os outros DataFrames aqui...
}

# Função para buscar incertezas
'''
def get_uncertainty_pseudocontinuum(temperatura, deslocamento_num, elemento):

    temperaturas_disponiveis = [col for col in dataframes['Fe I'].columns if isinstance(col, int)]
    temperatura_aproximada = min(temperaturas_disponiveis, key=lambda x: abs(x - temperatura))

    deslocamento_num = round(deslocamento_num)
    # Converte a temperatura e o deslocamento para a formatação correta
    deslocamento_str = f"{deslocamento_num:+d}%".replace("-", "−")

    if elemento == "all":
        resultados = {}
        for elem, df in dataframes.items():
            resultado = df[df['Pseudocontinuum Displacement'] == deslocamento_str][temperatura_aproximada]
            resultados[elem] = float(resultado.values[0]) if not resultado.empty else None
        return resultados
    else:
        # Caso específico para um elemento
        df = dataframes.get(elemento)
        if df is not None:
            resultado = df[df['Pseudocontinuum Displacement'] == deslocamento_str][temperatura_aproximada]
            return float(resultado.values[0]) if not resultado.empty else None
        else:
            return None

# Exemplo de uso

temperatura = int(input("Digite a temperatura desejada (exemplo: 4000): "))
deslocamento_num = float(input("Digite o deslocamento de pseudocontínuo como número inteiro (ex: -2, -1, 1, 2): "))
elemento = input("Digite o elemento ou all: ")
resultados = get_uncertainty_pseudocontinuum(temperatura, deslocamento_num, elemento)
print(resultados)
'''

def get_uncertainty_pseudocontinuum(temperatura, deslocamento_num, elemento):
    temperaturas_disponiveis = [col for col in dataframes['Fe'].columns if isinstance(col, int)]
    temperatura_aproximada = min(temperaturas_disponiveis, key=lambda x: abs(x - temperatura))

    # Find the nearest available reference magnitude (1% or 2%) and scale
    sigma = abs(float(deslocamento_num))
    ref_magnitudes = np.array([1, 2])
    ref_mag = ref_magnitudes[np.abs(ref_magnitudes - sigma).argmin()]
    scale = sigma / ref_mag if ref_mag > 0 else 0.0

    # Always use the positive reference column; the sign of the displacement
    # does not matter because we are computing an uncertainty magnitude.
    deslocamento_str = f"+{int(ref_mag)}%"

    def lookup(df):
        resultado = df[df['Pseudocontinuum Displacement'] == deslocamento_str][temperatura_aproximada]
        if resultado.empty:
            return None
        return float(resultado.values[0]) * scale

    if elemento == "all":
        resultados = {}
        for elem, df in dataframes.items():
            val = lookup(df)
            resultados[elem] = round(val, 4) if val is not None else None
        return resultados

    df = dataframes.get(elemento)
    if df is None:
        return None, None

    val = lookup(df)
    if val is None:
        return None, None
    return {elemento: round(val, 4)}, f'sigma(pseudo) = {round(val, 4)}'

