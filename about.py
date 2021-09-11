###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    HANDY INTERACTION                                ###
###                        PURPOSE:    WINDOWS/LINUX/MACOS FLAT MODERN UI               ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################


# THIS FILE IS DEDICATED FOR THE ABOUT PAGE IN THE APPLICATION WHICH ACTS AS A OR AS A HELP TAB OF THE SOFTWARE APPLICATION
#BELOW IS A DUMMY RANDOM GENERATED TEXT TO DISPLAY IN THE ABOUT HOME PAGE.
#KEEP ALL YOUR ABOUT IN ONE PLACE, ASSIGN IT TO A VARIABLE AND THEN IMPORT THIS FILE TO MAIN.PY FILE, AN DUSE THIS VARIABLE FOR THE DOCUMENT.
aboutHome = """
La principal funcionalidad del software Handy Interaction es correr diferentes modelos de vision por computador para el reconocimiento de la mano y extracción de información relacionada con esta extremidad. La ventana principal en este caso está dividida en dos partes, que permiten controlar el uso de la cámara web conectada al computador (en el centro de la ventana) y escoger un modelo de extracción con alguna visualización de los datos (a la derecha de la ventana). 

El modelo principal de la aplicación es una solución de seguimiento de dedos y manos de alta fidelidad, que hace parte de MediaPipe® (solución multiplataforma desarrollada por Google® para medios en vivo y de transmisión). Emplea el aprendizaje de maquina para inferir 21 puntos de referencia 2D de una mano a partir de un solo fotograma. Mientras que los enfoques actuales de vanguardia se basan principalmente en entornos de escritorio potentes para la inferencia, el método de Handy Interaction logra un rendimiento en tiempo real en un computador convencional e incluso se escala a varias manos. Se espera que proporcionar esta funcionalidad de percepción de la mano a la comunidad de investigación y desarrollo más amplia, resulte en la aparición de casos de uso creativos, estimulando nuevas aplicaciones y vías de investigación. 

Los 21 puntos de referencia de la mano (hand landmarks) que extrae el modelo se muestran en el manual de usuario. Handy Interaction además de la identificación de puntos de referencia, permite su envío por medio del protocolo OSC a otro software en el mismo computador o a otro computador conectado a una misma red usando un protocolo UDP (User Datagram Protocol).

El menú de la derecha en la funcionalidad principal (Run Model), permite extraer otras características asociadas al movimiento de la mano, partiendo de los puntos de referencia mencionados anteriormente. La lista completa puede accederse por medio de un menú desplegable.

Entre las opciones se encuentran 2 modelos de aprendizaje de máquina para la detección de poses y algunos ejemplos de reconocimientos de gestos que pueden usarse para el control de sistemas interactivos, tales como ‘scroll’, ‘zoom’ y ‘slide’. Este último tipo de gestos se calculan directamente usando alguna métrica de relacionamiento entre puntos de referencia de la mano y no por medio de modelos de aprendizaje de máquina.

Cualquiera de las opciones en el menú desplegable permite visualizar en tiempo real la característica extraída o la salida del modelo, y además enviar el resultado por medio de mensajes OSC para ser usado en otro tipo de aplicación computacional. En este caso, la misma información que se muestra como resultado de la inferencia del modelo, es la que se envía por OSC. Para indicaciones sobre como configurar las opciones del envío de datos, el lector debe referirse a la sección OSC Settings del manual de usuario. 
"""

aboutGestureRec = """
La funcionalidad de captura de datos para entrenamiento de modelos de reconocimiento de gestos es similar a la funcionalidad de captura de poses (ver sección anterior). Vale aclarar que una pose es la configuración estática (en un solo fotograma) de los puntos de referencia de la mano, mientras que un gesto es el movimiento de la mano durante una ventana corta de tiempo (usualmente entre 40-100 fotogramas) y en algunos casos durante un tiempo indefinido. Partiendo de esta aclaración, este módulo de Handy Interaction permite recoger datos clasificados para el entrenamiento de modelos de reconocimiento de gestos. 

A diferencia del modulo para captura de poses que genera un archivo diferente para cada clase, el modulo para captura de gestos produce un único archivo con extensión .npz que por defecto es llamado ‘hand_gestures’, en el cual deben incluirse todos los datos de entrenamiento para las diferentes clases consideradas en la tarea de clasificación. El formato de los archivos .npz es de tipo ‘zip’ y cada archivo contiene una variable en formato .npy. Asi mismo, un archivo npy es un archivo de matriz NumPy creado por el paquete de software Python con la biblioteca NumPy instalada. Contiene una matriz guardada en el formato de archivo NumPy (npy). Los archivos npy almacenan toda la información necesaria para reconstruir una matriz en cualquier computadora, que incluye información de tipo y forma.

El uso de la interfaz gráfica es el siguiente. Primero, se debe ingresar el nombre de la clase y hacer click en el boton ‘Add Class’ para validar el texto ingresado. Segundo, se proceden a grabar los datos de entrenamiento para esa clase. Como se tratan de gestos con una duración en el tiempo, el software por defecto captura las posiciones de los puntos de referencia de la mano durante 45 fotogramas. El boton ‘Record’ habilita una barra de progreso para permitir la preparación del usuario en la ejecución del gesto y luego procede con la captura durante 45 fotogramas. Por cada ejemplo que se quiera incluir en el conjunto de datos de entrenamiento para una misma clase, se debe repetir el mismo procedimeinto dando click en el boron ‘Record’. 

Tercero, para agregar ejemplos de entrenamiento que pertenezcan a otra clase, se debe presionar el boton ‘Save’ para guardar los datos previamente ingresados. Al hacerlo, la interfaz limpia el campo de texto para permitir el ingreso de una nueva clase en el conjunto de datos de entrenamiento. Cada que se quiera agregar una nueva clase, se debe proceder con los mismos tres pasos de forma iterativa. Vale la pena aclarar que cada que se presiona el boton ‘Save’ todos los datos acumulados de entrenamiento para todas las clases ingresadas se guardan sobre el mismo archivo ‘hand_gestures.npz’.
"""

aboutPoseRec = """
Para el entrenamiento de modelos supervisados es necesario tener a disposición un conjunto de datos que permitan identificar los diferentes casos de clasificación con su respectiva anotación sobre la categoría a la que pertenecen, de modo que el modelo pueda aprender de estos ejemplos. Para suplir esta necesidad, el software Handy Interaction cuenta con un módulo que permite recoger estos datos para el entrenamiento de un sistema de clasificación de poses realizadas con la mano.

La interfaz gráfica en este caso permite como primer paso, escribir el nombre de una clase (categoría) que representará los datos que están por ser capturados. Escribir un nombre y luego la tecla enter, garantiza que hay un nombre válido para la clase antes de proceder con la captura de los datos de entrenamiento, antes de habilitar el boton ‘start’ de inicio de captura. Un click en este boton, muestra la imagen que se obtiene desde la cámara conectada al computador y permite visualizar una barra de progreso que indica el porcentaje de tiempo alcanzado antes de iniciar la grabación de datos de entrenamiento. Esto con el fin, de permitir un tiempo de preparación de la pose con la mano y no capturar datos que no correspondan a la clase declarada. 

La captura de datos de entrenamiento esta basada en almacenar las posiciones de los 21 puntos de referencia, de forma continua, para cada fotograma proveniente de la cámara. Por lo que la pose de la mano debe mantenerse hasta que se presione el boton ‘stop’. Este tipo de procedimiento es típico en el entrenamiento de modelos de aprendizaje de máquina y pretende grabar la misma pose con típicas variaciones en su ejecución, como orientación de la mano, rotación, oclusión o incluso condiciones de iluminación en la imagen. Cuando se termina la captura de datos, se crea un archivo comprimido en formato zip, con un archivo CSV (comma separated values) con los datos de entrenamiento que corresponden a la clase que da nombre al archivo. Para capturar datos de entrenamiento pertenecientes a otra clase, se debe repetir el procedimeinto, comenzando por escribir el nombre de la nueva clase.
"""

aboutOsc = """
La última funcionalidad del software es la configuración del envío de datos OSC. Handy Interaction esta diseñado para enviar por medio de este protocolo de comunicación, los resultados de la inferencia del modelo seleccionado. Como el objetivo principal del software es el uso con fines interactivos de los resultados de los modelos de aprendizaje de máquina, la opción del envio de datos OSC está siempre activada y lo que el usuario puede hacer es configurar la forma como se usa. Por ejemplo, seleccionando la dirección IP, la ruta y el puerto que se usan en el envío de los datos.
"""