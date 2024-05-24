1. Hacer la logica del juego
    [X] - El juego reparte 2 cartas a cada jugador incluida la casa
        [ ] - Validar si te toca Blackjack en la primera jugada
            [ ] - Pagar apuesta 3:2 (1.5x)
    [ ] - El juego es capaz de notar cuando la casa gana y automaticamente termina la ronda
    [X] - El juego puede dejar pedir otra carta 
    [X] - EL juego debe decidir si perdiste con la suma de tus cartas
    [X] - Si la casa tiene 16 en su suma, tiene que pedir otra carta
        [X] -  Si la casa tiene 17 o mas se puede quedar con eso
    [X] - Validar que el sistema identifiquen el AS como 1 u 11
        [X] - Validar que el usuario identifique el AS como 1 u 11
        [X] - Si al momento de repartir toca 2 AS (11) uno se cambia por 1 automaticamente
    [ ] - Agregar botones
        [ ] - Agregar funcionalidades como el "DOUBLE", "SPLIT" 
            [ ] - Anadir boton de double con su condicion de uso
            [ ] - Anadir boton de split con su condicion
                [ ] - Anadir boton de "RE-SPLIT" (No tan comun)
        [X] - Agregar boton para "STAND"
            [X] - Agregar la funcion y que pase de turno 
            [ ] - Hacer que pase al siguiente jugador
        [ ] - Agregar boton de "FOLD" 
    [ ] - Al finalizar la ronda, limpiar la mesa y volver a jugar
        [ ] - Agregar condicion de derrota si algun jugador se queda sin dinero
        [ ] - Agregar posibilidad de retirarse

2. Hacer que se muestren las cartas que le toco a cada jugador
    [X] - Con las variables NAMECARDS se tiene que tomar la carta de images
        [X] - Seleccionar un palo de forma aleatoria
    [ ] - La casa debe mostrar solo 1 carta, la otra tiene que ser oculta
        [ ] - La casa muestra sus cartas cuando terminan las apuestas
        [ ] - Agregar funcionalidad de "INSURANCE"

3. Hacer las fichas de las apuestas
    [ ] - Se debe poner de alguna manera controlar las apuestas
        [ ] - Al ganar la apuesta un jugador, su ganancia es su apuesta duplicada