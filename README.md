# COVID-19-UNRC
<h2> Paquete para modelizar la epidemia COVID-19 </h2>

El archivo FitSEIR_UNRC.py contiene varias funciones con la finalidad de descargar datos actualizados sobre la pandemia de COVID-19 y ajustar los parámetros de   un modelo SEIR a estos datos.

**Ejemplo de uso**
Desde una consola de python (ipython o jupyter-qtconsole)

    >> from FitSEIR_UNRC import downloadData, FitSEIR

Importa las funciones downloadData para desacragar datos y FItSEIR para ajustar el modelo SEIR a los datos de la pandemia.

    >> downloadData()

Descarga los datos de infectados, recuperados y muertos de todos los paises del mundo.

    >> FitSEIR(Pais,Metodo)

Ajusta un modelo SEIR a los datos de "Pais". "Pais" es  el nombre en ingles del país que se quiere analizar.  "Metodo" es el método de optimización que se quiere utilizar,las opciones posibles son

* ["dual_annealing"](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html#scipy.optimize.dual_annealing): es la opción por defecto, es un minimizador global estocástico.  Produce un buen resultado en un tiempo algo prolongado pero aceptable
* ["shgo"](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.shgo.html): Produce un resultado rápido pero suele ser no muy bueno.
* ["brute"](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brute.html#scipy.optimize.brute): Halla prácticamente el mejor ajuste en un tiempo extremedamente largo.

<h2> Modelo SEIR </h2>

<b> Bibliografía </b>

[BCF2019] "Mathematical Models in Population Biology and Epidemiology", Fred Brauer and Carlos Castillo-Chavez and Zhilan Feng, ISBN: 978-14-9399-828-9, Springer Nature,2019.

**Modelo**


SEIR Susceptibles-Expuestos-Infectados-Removidos por la enfermedad.  El modelo es básicamente el de sección 2.5 de [BCF2019].

![SEIR](Imagenes/SEIR.png)
![](Imagenes/Formulas.png)

Sólo es necesario modelar las tres primeras  ecuaciones

**Requerimientos**

Los programas ajustando el modelo a los datos de Argentina requieren descargar desde ["Ministerio de Salud"](http://datos.salud.gob.ar/dataset/covid-19-casos-registrados-en-la-republica-argentina/archivo/fd657d02-a33a-498b-a91b-2ef1a68b8d16) la base de datos de casos COVID-19.


**Resultado**

![](Imagenes/18-junio-2020-Buenos-Aires.png)
![](Imagenes/18-junio-2020-CABA.png)
![](Imagenes/18-junio-2020-Córdoba.png)
