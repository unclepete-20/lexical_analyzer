# Analizador Léxico ✍🏻

### Descripcion ✏️

Este repositorio contiene la implementacion de Autómatas en todas sus versiones; desde AFN hasta AFD y sus minimizaciones. Se ha construido utilizando Python como motor principal para desarrollar toda la lógica e implementación de los algoritmos que rigen a los autómatas. Este proyecto permite construir AFN's y AFD's a partir de de expresiones regulares que posteriormente son convertidos al formato postfix y los cuales son procesados para producir visualmente la representacion de dicha expresion como un autómata. Es importante mencionar que por medio de estas implementaciones, es posible determinar si una cadena generada por una expresion regular pertenece a L(r), este siendo la representacion del lenguaje que se haya definido.

### Funcionalidades ⚙️

- [x] AFN a partir del algoritmo de Thompson
- [ ] AFN ➡️ AFD por medio de la construccion de Subconjuntos
- [ ] AFD Directo
- [ ] Minimización de AFN y AFD
- [ ] Simulación de las cadenas por medio de Autómatas