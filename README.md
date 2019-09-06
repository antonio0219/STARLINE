# DOCUMENTACIÓN (COMO CREAR NIVELES)
+ Lo primero que tendríamos que hacer es acceder al fichero config.csv, ubicado en *STARLINE/assets/config/config.csv*
En la primera línea del fichero config.csv encontramos el número de la nave que está seleccionada por cada jugador. Hay un total de 11 naves y se pueden seleccionar desde el selector dentro del juego.
En las líneas siguientes encontramos los niveles que están predefinidos en el juego (Ordenados según aparezcan en el juego), y están estructuradas de la siguiente manera:
    1. __El nombre del archivo con su extensión.__ Todos los ficheros de niveles estarán ubicados en *STARLINE/assets/levels*, donde tendremos que crear un archivo nuevo con extensión csv.
    2. __El nombre que aparecerá dentro del juego.__
    3. __La canción que sonará en dicho nivel.__ Se pueden añadir canciones en *STARLINE/assets/music* (preferiblemente en formato ogg), o bien utilizar una de las canciones que están ya importadas.
    4. Si escribimos *True* en este espacio, el nivel ya estará desbloqueado y aparecerá en verde dentro del juego, pero si escribimos *False*, tendremos que superar la fase anterior para que se desbloquee la fase actual.
    
        Ejemplo:
        ~~~
        prueba.csv;PRUEBA;music.ogg;True
        ~~~
+ Una vez hemos terminado con el fichero config.csv, debemos entrar a el archivo del nivel que vamos a crear desde cualquier editor de texto.
Las líneas 1 y 2 son para determinar las coordenadas iniciales de las dos naves, quedando de la siguiente manera (La coordenada 0,0 será el centro del objeto):
    ~~~~
    player1;coordenada x;coordenada y
    player2;coordenada x;coordenada y
    ~~~~
+ A continuación podremos añadir tanto enemigos como mensajes:
Todos los objetos deberán tener como primer parámetro el instante (en milisegundos) cuando queramos que aparezca, empezando a contar el tiempo desde el inicio del nivel. Por ejemplo, si ponemos 3000, el enemigo o mensaje se generará 3 segundos después de comenzar el nivel.
Los objetos deberán estar ordenados por orden de aparición en el tiempo, es decir, un objeto que aparezca a los 3000 milisegundos debe de ir antes dentro del fichero que otro que aparezca a los 4000.
Los mansajes requieren los siguientes parámetros:
    1. __El instante en milisegundos cuando se muestre el mensaje__.
    2. Escribimos __message__ para indicar el tipo de objeto que vamos a crear.
    3. __El contenido del mensaje__.
    4. __Los milisegundos que el mensaje aparecerá en la pantalla__. Por ejemplo, si queremos que el mensaje se vea por 5 segundos, pondremos 5000.
    5. __Coordenada en X__. Es recomendable posicionar el mensaje en las coordenadas X: 500, Y: 600.
    6. __Coordenada en Y__.
    7. __Los milisegundos que habrá entre cada caracter del mensaje__. Es recomendable usar 50 milisegundos.
    
        Ejemplo:
        ~~~
        4000;message;¡Hola mundo!;5000;500;600;50
        ~~~
    
    Los ovnis y los alien se crean de una forma muy similar, y requieren los siguientes parámetros:
    1. __El instante en milisegundos cuando se genere el enemigo__.
    2. __El tipo de enemigo que queremos crear__. Si queremos un ovni, escribimos *ovni*, y si queremos un alien, escribimos *alien*.
    3. __Coordenada en X__.
    4. __Coordenada en Y__.
    5. __Los píxeles que se moverá en x en cada frame__. Si queremos que se mueva a la derecha pondremos un número positivo, y uno negativo para que se mueva a la izquierda. Mientras más positivo (O más negativo) sea el número más rápido se moverá.
    6. __Los píxeles que se moverá en x en cada frame__.
+ El nivel acabará cuando se terminen los objetos de la lista.