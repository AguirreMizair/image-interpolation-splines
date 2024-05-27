import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline

def improve_image_quality_blurry(image, factor=1):
    # Obtener las dimensiones de la imagen
    height, width = image.shape    
    
    # Crear una malla
    x = np.arange(0, width)
    y = np.arange(0, height)
    
    # Crear una función interpolante 2D
    interpolator = RectBivariateSpline(y, x, image)
    
    # Crear una nueva malla mas fina
    y_new = np.arange(0, width, 1 / factor)
    x_new = np.arange(0, height, 1 / factor)

    # Interpolar los valores de los nuevos puntos
    image_interpolated = interpolator(x_new, y_new)
    
    return image_interpolated
