
# 🤖 Bot Discord CS50

Este bot de Discord fue creado para asistir en la gestión de estudiantes y oficinas dentro del contexto del curso **CS50**. Utiliza interfaces interactivas como `Modals` y `Selects` para permitir una experiencia fluida y validada para los usuarios y administradores.

---

## 🎯 ¿Qué hace el bot?

### 🏢 Gestión de Offices
- Los offices (espacios de ayuda) se almacenan en dos estructuras:
  - `Estado.OfficesLista`: offices activos
  - `Estado.OfficesRevision`: offices en revisión
- Al editar un office, se cargan sus datos automáticamente y se permiten modificaciones con validaciones integradas.

### ✍️ Modal de edición
- El `formularioAgregarOffices` permite editar datos de un office, como:
  - ID o nombre de la office
  - Horario del bloque (`10-12`, `1-3`, `3-5`)
- Se valida:
  - Que no se repita un nombre ya existente
  - Que el formato de horario sea correcto

### 👤 Selección de estudiantes por rol
- Se presenta un menú desplegable (`Select`) con hasta 25 estudiantes que tengan el rol `Y25C1-Student`.
- Una vez seleccionado el estudiante, se lanza el `Modal` correspondiente para completar o editar información vinculada.

---

## 📘 Manual de uso

Puedes consultar el manual de uso completo del bot en el siguiente enlace:

👉 [Manual del Bot Discord CS50 (Jessua Solís)](https://corc-my.sharepoint.com/:w:/g/personal/jessua_solis96u_std_uni_edu_ni/ER4crIBo7qBFlfJoXNcjQAAB3tdSh_thbUDUkZpzPUwHpw?rtime=p9AKb0u13Ug)
