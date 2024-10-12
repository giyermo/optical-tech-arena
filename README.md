# optical-tech-arena

A repository with the code to solve the agorize tech arena problem about optic services.

# **Sprints**

1.  **Read inputs**

    Be able to read the inputs from the standard input file (stdin) using fileinput library.

2. **Generate the graph**

    Use inputs to generate the graph according to the problem.

3. **Show cuts**

    Represent the cuts that the problem will generate.

4. **Search for algorithm**

    Look for possible algorithms that can solve the problem or that we can build from in order to do it.

    # **Planteaminto para el algoritmo:**
       1. Como la puntuación depende del valor, planificar las rutas de los nuevos servicios priorizando el orden de su valor
       2. Teniendo en cuenta que evalua solo V, se podría realizar a fuerza bruta el algoritmo, al no depender de la complejidad
       3. Los nodos deben controlar cuántas veces se ha hecho una conversión de canal para evitar exceder su límite.
    

# **Caja de Dudas**

-> si empleamos el network.py como el archivo que crea los grafos, no sería más comodo que los servicios fuesen un `dict` en vez de un `tuple` por legibilidad y sostenibilidad??? Supongo que en el uso de memoría habrá una gran diferencia, pero ns hasta que punto es notable

# **Silly things to take into account**

1. **Parallel edges**
   Edges can be parallel, but not loops. So I am not sure if the approach of main.py with the edges can allow them
