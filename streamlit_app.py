import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
from imagenes import improve_image_quality_blurry
import concurrent.futures



def main():
    """Interfaz principal del programa"""
    
    st.title("Interpolación de Imagen")
    st.write("Carga una imagen y modifica sus píxeles.")

    # Cargar la imagen desde el explorador de archivos
    uploaded_image = st.file_uploader("Selecciona una imagen borrosa", type=["jpg", "jpeg", "png"])
    
    factor = st.number_input("Inserta el factor de conversión", 
                             value=10.0, placeholder="Escribe un número", 
                             min_value=0.0, max_value=500.0,
                             step=0.1)
    st.write("Por cada pixel en la imagen original, se crearán", factor, "nuevos píxeles")
    
    if uploaded_image is not None:
        
        image = np.array(Image.open(uploaded_image).convert('L'))
            
        imagen = plt.figure(figsize=(10, 5))
        plt.imshow(image, cmap='gray')
        plt.axis('off')

        st.subheader("Imagen Original")
        st.pyplot(imagen)

        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            #En este bloque controlo el timepo maximo de ejecucion
            
            futuro = executor.submit(improve_image_quality_blurry, image, factor)
            
            try:
                improved_image = futuro.result(timeout= 0.6)
                
                imagen_nueva = plt.figure(figsize=(10, 5))
                plt.imshow(improved_image, cmap='gray')
                plt.axis('off')

                # Mostrar  la nueva imagen

                st.subheader("Imagen Nueva")
                st.pyplot(imagen_nueva)
                
                #para guardar la imagen
                
                nombre = uploaded_image.name + "_interpolada"
                
                buf = BytesIO()
                plt.imsave(buf, improved_image, format='jpg', cmap='gray')
                buf.seek(0)

                st.download_button(
                    label="Descargar imagen mejorada",
                    data=buf,
                    file_name=nombre + '.jpg',
                    mime='image/jpg'
                )
                
            except concurrent.futures.TimeoutError as e:
                st.error("Poder de computo exedido. Se necesita bajar el factor o subir una imagen mas ligera.", icon = "🔥")
                st.stop()
                

if __name__ == "__main__":
    main()
