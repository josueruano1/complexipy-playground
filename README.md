# complexipy-playground

Proyecto Python de ejemplo con la complejidad cognitiva repartida a propósito.

Es material de prueba para herramientas de análisis estático: mezcla funciones
triviales con funciones deliberadamente enrevesadas, en carpetas con perfiles
distintos, para que cualquier informe tenga algo real que medir en lugar de
salir vacío.

| Carpeta | Perfil |
| --- | --- |
| `src/billing` | Facturación: conciliación, recargos, notas de crédito y aritmética trivial. |
| `src/orders` | Pedidos: un árbol de decisión, precios regionales, devoluciones y validación. |
| `src/utils` | Funciones pequeñas, todas triviales. |
| `reports` | Informes: una función larga de agregación. |
| `notifications` | Plantillas de avisos de cobro. |

Algunas funciones quedan a propósito por encima de 15, el umbral de referencia;
el resto se mantiene por debajo.

## Este proyecto no se ejecuta

No tiene dependencias, ni configuración, ni lee variables de entorno. Es solo
código fuente para analizar. Si algún día aparece aquí un `.env`, una clave o
cualquier credencial, es un error: el `.gitignore` los bloquea de antemano.
