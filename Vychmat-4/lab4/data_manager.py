import numpy as np


def load_data_from_txt(file_path):
    if not file_path.lower().endswith('.txt'):
        raise Exception("Файл должен иметь расширение TXT.")
    try:
        def conv(s):
            if isinstance(s, bytes):
                s = s.decode('utf-8')
            return float(s.replace(',', '.'))
        converters = {0: conv, 1: conv}
        data = np.loadtxt(file_path, converters=converters)
        if data.ndim == 1:
            data = data.reshape(-1, 2)
        x = data[:, 0]
        y = data[:, 1]
        return x, y
    except Exception as e:
        raise Exception("Ошибка загрузки данных из TXT: " + str(e))
