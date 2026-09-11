# complexipy-playground

Proyecto Python de ejemplo con la complejidad cognitiva repartida a propósito.

Es material de prueba para herramientas de análisis estático: mezcla funciones
triviales con funciones deliberadamente enrevesadas, en carpetas con perfiles
distintos, para que cualquier informe tenga algo real que medir en lugar de
salir vacío.

| Carpeta | Perfil |
| --- | --- |
| `src/billing` | Una función muy enrevesada y otra moderada, junto a aritmética trivial. |
| `src/orders` | Un árbol de decisión anidado y un validador de complejidad media. |
| `src/utils` | Funciones pequeñas, todas triviales. |

Tomando 15 como umbral de referencia, tres funciones quedan por encima y trece
por debajo. Las escritas a propósito por encima llevan un comentario `# hotspot`.

## Este proyecto no se ejecuta

No tiene dependencias, ni configuración, ni lee variables de entorno. Es solo
código fuente para analizar. Si algún día aparece aquí un `.env`, una clave o
cualquier credencial, es un error: el `.gitignore` los bloquea de antemano.
