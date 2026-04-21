# Justificación breve del equipo

## Problema operativo
La aseguradora necesita un asistente interno para el área de siniestros que ayude a localizar información en documentos, preparar borradores de respuesta y apoyar a gestores humanos sin comprometer tiempos de respuesta ni tratamiento de datos sensibles.

## Prioridad dominante del diseño
La prioridad dominante del diseño es equilibrar **seguridad del dato y rendimiento operativo**, porque el caso combina presencia de PII, tolerancia baja al error, latencia objetivo inferior a 4 segundos y una carga relevante de usuarios internos simultáneos.

## Decisión principal del equipo
El equipo decide priorizar una arquitectura con enfoque **gestionado**, usando Amazon Bedrock como recomendación inicial en la capa de inferencia/modelo.

## Por qué tomamos esta decisión
Tomamos esta decisión porque una opción gestionada reduce complejidad operativa, acelera el despliegue del MVP y facilita una salida más controlada para un caso que exige trazabilidad, revisión humana y tiempos de respuesta razonables. En este contexto, la rapidez de implantación y la simplicidad operativa pesan más que el control fino del stack.

## Trade-off aceptado
Aceptamos el siguiente trade-off: **menos control fino y personalización a cambio de más rapidez de despliegue, menor fricción operativa y una gobernanza inicial más manejable**.

## Riesgo crítico
El riesgo crítico es la **exposición o tratamiento inadecuado de datos personales sensibles (PII)**. Por eso proponemos minimización de datos, control de acceso, revisión humana en casos sensibles y validación previa del tratamiento de información antes del despliegue.

## Mejora para una segunda iteración
En una segunda iteración mejoraríamos la lógica de reglas para introducir criterios más finos de coste, disponibilidad y escalado, y haríamos que la salida del memo cambie de forma más evidente cuando cambien variables como la latencia, la demanda o el presupuesto.

## Diferencia entre ayuda de IA y decisión del equipo
La IA se ha utilizado como apoyo para estructurar, revisar y redactar mejor el contenido, pero la selección de variables relevantes, la elección del trade-off dominante y la decisión arquitectónica final han sido tomadas por el equipo.
