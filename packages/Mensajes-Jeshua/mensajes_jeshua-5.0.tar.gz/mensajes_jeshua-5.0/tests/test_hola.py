import unittest
import numpy as np
from mensajes.hola.saludos import generar_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6))



# La carpeta mensajes es un paquete, dentro de ella esta la carpeta hola y la carpeta adios que ambas son subpaquetes.
# Para indicar de forma estricta que el directorio mensajes es un paquete que incluye módulos. Lo que se hace generalmente es crear dentro del paquete un nuevo archivo, un nuevo script con el nombre: __init__.py.
# La carpeta hola es un subpaquete, dentro de ella esta el módulo saludos.
# La carpeta adios es un subpaquete, dentro de ella esta el módulo despedidas.

# Distribución local...
# Para crear un paquete distribuible, tenemos que crear un fichero especial fuera de la raíz del directorio del paquete.
# El fichero especial, tiene que tener de nombre: setup.py
# Una vez hemos definido el distrito y su configuración, tenemos que generar el paquete. Así que vamos a llamar a este script setup desde la terminal. Llamamos al script setup.py y le pasamos el parametro sdist para generar el distribuible. 
# De esta manera, automáticamente se generarán diferentes ficheros y carpetas; y la que nos interesa es la carpeta dist.

# Para instalar un paquete distribuible...
# Estanddo en la raíz del proyecto, en módulos y paquetes vamos a acceder a el directorio dist.
# >> cd dist
# >> pip install (El nombre del paquete)
# Con pip list podemos ver la lista de paquetes que tenemos instalados en nuestra maquina.

# Para hacer una actualización de un paquete...
# Una vez hecho el cambio, iríamos a nuestro setup.py y le cambiariamos la verison, después, volveríamos a la raíz donde tenemos el setup.py. y ...
# >>python setup.py sdist
# Una vez, ya creada la nueva versión, vamos a actualizarla...
# >>cd dist
# >>pip install (Nombre del paquete actualizado) --upgrade      
# Esto automáticamente desinstala la versión anterior e instala la nueva.

# Para borrar un paquete...
# Se abre la terminal y...
# pip uninstall (Nombre del paquete que se quiere borrar)

# Comando especial -> cd .. -> Para volver de dist a la raíz.

#------------------------------------------------------------------------------------------------------------------
# Para que la maquina se encargue ella misma de encontrar todos los paquetes:
# from setuptools import setup, find_packages
# packages=find_packages()
# para probrar lo anterior, en la terminal escribimos: python setup.py sdist


# Otra cosa que podemos programar es que si necesitamos utilizar una librería externa en una de nuestras funciones que esta en uno de los modulos...
# por ejemplo la librería externa numpy...
# >>pip install numpy
# Una vez instalada la importas...
# import numpy as np

# Nuestro paquete mensajes tendra un módulo externo, es por eso que necesitamos indicarle en el setup.py que instale este paquete como una dependencia (numpy)...
# Para indicar que nuestro paquete de mensajes tiene esta dependencia de numpy, Abajo del todo indicar un nuevo parámetro a setup llamado...
# install_requires=['diferentes paquetes qu se van a instalar'], se puede indicar que version de la libreria se quiere installar, de esta manera siempre se instalaria esa versión como dependencia.
# También se le puede pedir una version mas grande o igual a la que requeramos, de esta manera nos cuidamos la espalda por si sale una versión nueva.
# También se puede crear un requirements.txt y ahí indicar cadda paqute que se requiere instalar y en la versión que se requiere instalar.
# Si se hace lo del txt, entonces en install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()]

# Para probar todo lo anterior creemos una nueva versión de mensajes...
# Pero antes, necesitamos indicarle a la maquina que el fichero requirements.txt forma parte también del paquete para que lo pueda procesar al instalarlo...
# Para ello vamos a crear un nuevo archivo en la raíz y le vamos a llamar de la siguiente manera, escrito todo en mayúscula MANIFEST.in....
# Con esto ya le estariamos indicando que incluya dentro del setup el fichero requirements. 

# Vamos a hacer una pequeña prueba unitaria, porque en principio, cuando tenemos un fichero llamado test al lado del setup, nosotros podemos desde la raíz Llamar al fichero setup.py y ejecutar test...
# >>python setup.py test
# Sin embargo al hacer esto no estamos haciendo ninguna prueba...
# La manera correcta de manejar diferentes kits de pruebas es la siguiente...
# En la raíz, justo donde tenemos la carpeta de nuestro paquete, vamos a crear otra carpeta llamada 'tests' , si, en plural.
# Nuestro fichero test lo movemos a la carpeta tests y le vamos a cambiar el nombre, deberiamos de tener por regla general, Por regla general, un fichero test para cada paquete que estamos comprobando, por ejemplo...
# En este caso en especifico nuestro test, deberia de llamarse test_hola
# Observar este script para chequear los cambios. 
# Dejamos vacio el test en setup.py y creamos abajo de test: test_suite='tests'
# Y es muy importante antes de continuar que indiquemos que test: test_suite='tests' también es un paquete.
# Por lo tanto le creamos el __init__.py a la carpeta tests que tambiés es un paquete.
# De tal manera, esto debería de permitir que la mquina auto descubra los diferentes ficheros de testing que hay.

#Después se actuliza una vez mas el paquete a la version 4.0 y se instala, dejando todo listo para distribuir el paquete públicamente.


#-------------------------Hasta aquí la distribucion local-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Distribuciñon Pública

# Ahora, vamos a ver cómo transformar este paquete local en un paquete que podamos publicar en internet el repositorio de pypi.

# pypi.org, básicamente es el lugar donde se almacenan todos los paquetes que nosotros instalamos cuando ponemos el comando pip install y el nombre de un paquete.

# Si quieres publicar en test.pypi.org cambia el nombre del paquete y cambia la versión del paquete, para el nombre agrega tu nombre de usuario de la página para que no haya conflicto por si hay otor paquete con el mismo nombre.

# Crea un README.md y en el describe la información de tu paquete.

# Agrega el README.md al MANIFEST.in y al setup.py

# Debajo del description un long_description=open('README.md').read(). En el MANIFEST -> include README.md

# Si se tiene una cuenta en GIT se puede colocar el link en la URL del paquete.

# También se agrega una licencia...

# También se debe agregar los clasificadores.

# En este punto se debe instalar dos paquetes para hacer lo que es el build, la construcción del paquete público y también la publicación.
# >>pip install build twine

# >>python -m twine

# Hay que borrar los paquuetes obsoletos.

# Despues van unos comandos.

# At this point watch video.