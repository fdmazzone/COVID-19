# COVID-19-UNRC
<h2> Paquete para modelizar la epidemia COVID-19 </h2>

El archivo FitSEIR_UNRC.py contiene varias funciones con la finalidad de descargar datos actualizados y ajustar los parámetros de   un modelo SEIR a estos datos.

**Ejemplo de uso**
Desde una consola de python (Ipython o Jupyter)

in[1]: from FitSEIR_UNRC import downloadData, FitSEIR

Importa las funciones downloadData para desacragar datos y FItSEIR para ajustar el modelo SEIR a los datos de la pandemia.

in[2]: downloadData()

Descarga los datos de infectados, recuperados y muertos de todos los paises del mundo.

in[3]: FitSEIR(Pais,Metodo)

Ajusta un modelo SEIR a los datos de "Pais". "Pais" es  el nombre en ingles del país que se quiere analizar.  "Metodo" es el método de optimización que se quiere utilizar,las opciones posibles son

* "dual_annealing": es la opción por defecto, es un minimizador global estocástico.  Produce un buen resultado en un tiempo algo prolongado pero aceptable
* "shgo": Produce un resultado rápido pero suele ser no muy bueno.
* "brute": Halla prácticamente el mejor ajuste en un tiempo extremedamente largo.

<h2> Modelo SEIR </h2>

<b> Bibliografía </b>

[BCF2019] "Mathematical Models in Population Biology and Epidemiology", Fred Brauer and Carlos Castillo-Chavez and Zhilan Feng, ISBN: 978-14-9399-828-9, Springer Nature,2019.

**Modelo**


SEIRD Susceptibles-Expuestos-Infectados-Recuperados y Defuntos por la enfermedad.  El modelo que construímos es básicamente el de sección 2.5 de [BCF2019] con la variación de incluir defunciones..


![SEIRD](Imagenes/SEIR.png)



$$
\begin{aligned}
&S^{\prime}=-\beta S I-\epsilon\beta E S\\
&E^{\prime}=\beta S I+\epsilon\beta E S-k E\\
&I'=k E-(\alpha+d) I\\
&R^{\prime}=\alpha I
\end{aligned}
$$

$$\begin{aligned}
\frac{1}{\alpha}&=\text{periodo infecciosidad medio}\\
\beta&=\text{cantidad de contactos por individuo por unidad de tiempo}\\
d&=\text{tasa de mortalidad}\\
\frac{1}{k}&=\text{vida media de un expuesto}\\
\epsilon &=\text{factor de corrección de contagiosidad}\\
\mathcal{R}_0&=\beta N\left(\frac{1}{\alpha+d}+\frac{\epsilon}{k}\right)=\text{número reproducción básico}\\
            &=\text{Cantidad infecciones a lo largo de la vida de un infeccioso dentro de una población de sólo susceptibles}\\
\end{aligned}
$$


Sólo es necesario modelar las primeras dos ecuaciones
