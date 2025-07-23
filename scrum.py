import streamlit as st
import random
import time
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_sortables import sort_items

# --- Configuración Inicial y Base de Datos del Juego ---

def get_initial_product_backlog():
    """Devuelve el estado inicial del product backlog como una lista de diccionarios."""
    return [
        {"name": "Registro de Usuarios con Email y DPI", "points": 13, "value": 10, "mandatory": True, "type": 'Seguridad'},
        {"name": "Checkout con Tarjeta de Crédito (integración con banco local)", "points": 13, "value": 10, "mandatory": True, "type": 'Seguridad'},
        {"name": "Catálogo de Restaurantes por Zona", "points": 21, "value": 9, "mandatory": True, "type": 'Core'},
        {"name": "Añadir Plato al Carrito de Compras", "points": 5, "value": 8, "mandatory": True, "type": 'Core'},
        {"name": "Login de Usuario", "points": 8, "value": 8, "type": 'Core'},
        {"name": "Ver Carrito de Compras", "points": 8, "value": 7, "type": 'Core'},
        {"name": "Función de Búsqueda de Platos", "points": 13, "value": 7, "type": 'Funcionalidad'},
        {"name": "Página de Perfil de Usuario", "points": 8, "value": 6, "type": 'Funcionalidad'},
        {"name": "Sistema de Calificaciones con 'estrellitas'", "points": 13, "value": 6, "type": 'Marketing'},
        {"name": "Integración con WhatsApp para notificaciones", "points": 8, "value": 5, "type": 'Marketing'},
        {"name": "Reseteo de Contraseña", "points": 5, "value": 5, "type": 'Seguridad'},
        {"name": "Panel de Administración de Restaurantes", "points": 21, "value": 4, "type": 'Admin'},
    ]

OBSTACLES = [
    {"title": "¡Deuda Técnica Inesperada!", "description": "Un módulo antiguo está causando fallos intermitentes.", "icon": "🔥", "role": "Development Team", "choices": [
        {"text": "Refactorizar ahora", "consequence": -8, "desc": "Consume tiempo, pero soluciona el problema de raíz."}, 
        {"text": "Aplicar un parche rápido", "consequence": -3, "desc": "Una solución temporal que nos permite seguir avanzando."},
        {"text": "Organizar un workshop de 'clean code'", "consequence": +2, "desc": "El equipo se siente proactivo y aprende nuevas técnicas, mejorando la moral y la velocidad."},
        {"text": "Ignorar el problema y seguir", "consequence": -10, "desc": "Máximo riesgo. El problema podría escalar y detener el sprint por completo."}
    ]},
    {"title": "¡Apagón de luz en la zona!", "description": "La oficina se ha quedado sin electricidad. La planta de emergencia no es suficiente para todos.", "icon": "💡", "role": "Scrum Master", "choices": [
        {"text": "Enviar a todos a casa (Home Office)", "consequence": -2, "desc": "Algunos no tienen buen internet en casa, la coordinación se dificulta un poco."}, 
        {"text": "Trabajar por turnos en la oficina", "consequence": -4, "desc": "Se pierde mucho tiempo y el ritmo de trabajo se rompe."},
        {"text": "Ir a un café con internet cercano", "consequence": 0, "desc": "La empresa paga el café. El cambio de ambiente distrae un poco pero se mantiene el ritmo."},
        {"text": "Usar 'hotspots' de celulares", "consequence": -3, "desc": "La conexión es inestable y los datos se consumen rápido."}
    ]},
     {"title": "¡Bloqueo en la Aguilar Batres!", "description": "Una manifestación ha bloqueado una de las vías principales. Varios miembros del equipo llegarán tarde.", "icon": "🚗", "role": "Scrum Master", "choices": [
        {"text": "Iniciar el día con tareas que no requieren a todo el equipo", "consequence": -1, "desc": "Buena gestión, el impacto es mínimo."},
        {"text": "Declarar 'Home Office' para los afectados", "consequence": -2, "desc": "Se pierde algo de coordinación pero avanzan."},
        {"text": "Esperar a que todos lleguen", "consequence": -5, "desc": "Se pierde media mañana de trabajo del equipo completo."},
        {"text": "Hacer una 'Daily' virtual de emergencia", "consequence": +1, "desc": "Excelente coordinación. El equipo se alinea y reorganiza el trabajo del día eficientemente."}
    ]},
    {"title": "¡Un Dev Junior Necesita Ayuda!", "description": "Un miembro nuevo del equipo está atascado con una tarea compleja.", "icon": "🧑‍🏫", "role": "Development Team", "choices": [
        {"text": "Que un Senior le dedique la tarde", "consequence": -6, "desc": "Invierte en el equipo a largo plazo, pero pierdes la capacidad del Senior hoy."}, 
        {"text": "Sugerirle que investigue por su cuenta", "consequence": -2, "desc": "Fomenta la autonomía, pero la tarea podría no completarse correctamente."},
        {"text": "Organizar una sesión de 'pair programming'", "consequence": +4, "desc": "Ambos aprenden y resuelven el problema más rápido de lo que lo harían por separado."},
        {"text": "Reasignar la tarea a un Senior", "consequence": -1, "desc": "La tarea se hará rápido, pero el junior no aprende y puede desmotivarse."}
    ]},
    {"title": "¡Feriado inesperado!", "description": "El gobierno decreta feriado el día de mañana por un evento nacional. Se pierde un día completo de trabajo.", "icon": "🎉", "role": "Scrum Master", "choices": [
        {"text": "Aceptar la pérdida del día", "consequence": -7, "desc": "La capacidad del sprint se reduce significativamente."},
        {"text": "Proponer reponer las horas el fin de semana", "consequence": -4, "desc": "El equipo acepta a regañadientes, la moral baja un poco."},
        {"text": "Re-planificar el resto del sprint", "consequence": -2, "desc": "Una reunión de emergencia consume tiempo, pero se logra ajustar el alcance."},
        {"text": "Cancelar el sprint y empezar uno nuevo", "consequence": 0, "desc": "Decisión drástica. No se pierde capacidad, pero tampoco se entrega valor en este ciclo."}
    ]},
    {"title": "¡Problemas con la SAT!", "description": "La integración con la facturación electrónica (FEL) está fallando por un cambio no documentado en la API de la SAT.", "icon": "🧾", "role": "Development Team", "choices": [
        {"text": "Contactar al soporte de la SAT y esperar", "consequence": -5, "desc": "La historia se bloquea hasta tener respuesta."},
        {"text": "Intentar ingeniería inversa para entender el cambio", "consequence": -8, "desc": "Es un esfuerzo enorme y arriesgado."},
        {"text": "Buscar una librería de un tercero que ya lo resolvió", "consequence": -1, "desc": "Cuesta un poco de dinero, pero ahorra mucho tiempo."},
        {"text": "Trabajar en otra historia mientras se espera", "consequence": -2, "desc": "El cambio de contexto reduce la eficiencia del equipo."}
    ]},
]

MULTI_ROLE_OBSTACLES = [
    {"title": "¡Requerimiento Urgente de Marketing!", "description": "Marketing necesita un 'landing page' para una campaña que inicia en 2 días. No estaba en el backlog y es una distracción del objetivo del Sprint.", "icon": "📢", 
     "decisions": {
        "Product Owner": {
            "prompt": "Marketing presiona. ¿Cómo respondes a esta petición que amenaza el Sprint?",
            "choices": [
                {"text": "Rechazar la petición y proteger el sprint", "consequence": 0, "desc": "El equipo está feliz, pero hay conflicto con Marketing."},
                {"text": "Negociar con Marketing una versión más simple", "consequence": -4, "desc": "Se logra un acuerdo, pero la negociación y el nuevo desarrollo consumen capacidad."}
            ]
        },
        "Development Team": {
            "prompt": "El PO ha negociado una versión simple. ¿Cómo la aborda el equipo?",
            "choices": [
                {"text": "Trabajar horas extra para cumplir", "consequence": -3, "desc": "Se logra la tarea, pero el equipo se agota y su rendimiento futuro se ve afectado."},
                {"text": "Intentar automatizar parte del proceso", "consequence": +1, "desc": "El equipo encuentra una forma inteligente de hacerlo rápido, ganando eficiencia."}
            ]
        }
     }},
    {"title": "¡Descubrimiento Tecnológico!", "description": "Un desarrollador descubre una nueva librería de código abierto que puede implementar una función compleja en una fracción del tiempo.", "icon": "✨",
     "decisions": {
         "Development Team": {
             "prompt": "Es una gran oportunidad, pero no es la tecnología estándar de la empresa. ¿Qué hacen?",
             "choices": [
                 {"text": "¡Implementarla ahora mismo!", "consequence": +8, "desc": "La ganancia de eficiencia es enorme y se libera capacidad para más tareas."},
                 {"text": "Investigarla un poco más antes de usarla", "consequence": +3, "desc": "Se pierde un poco de tiempo en la investigación, pero la ganancia sigue siendo muy buena."}
             ]
         },
         "Scrum Master": {
             "prompt": "El equipo quiere usar una nueva tecnología. ¿Cómo gestionas el riesgo?",
             "choices": [
                 {"text": "Confiar en el equipo y dar luz verde", "consequence": 0, "desc": "Fomenta la auto-organización y la moral."},
                 {"text": "Pedir una demo antes de integrarla", "consequence": -2, "desc": "Asegura la calidad, pero la burocracia ralentiza el proceso."}
             ]
         }
     }},
    {"title": "¡Conflicto de Diseño UX/UI!", "description": "El diseñador propone una interfaz muy moderna pero compleja de implementar. El equipo técnico prefiere una solución más simple y rápida.", "icon": "🎨",
     "decisions": {
         "Product Owner": {
             "prompt": "Una mejor UX podría atraer más usuarios, pero retrasa el lanzamiento. ¿Qué priorizas?",
             "choices": [
                 {"text": "Priorizar la experiencia de usuario (UX)", "consequence": -5, "desc": "El equipo deberá invertir más tiempo, retrasando otras historias."},
                 {"text": "Priorizar la velocidad de entrega (Time to Market)", "consequence": 0, "desc": "Se lanza una versión funcional pero menos atractiva."}
             ]
         },
         "Development Team": {
             "prompt": "Independientemente de la decisión del PO, ¿cómo aborda el equipo el desafío técnico?",
             "choices": [
                 {"text": "Buscar un componente pre-hecho que se aproxime", "consequence": +2, "desc": "Se ahorra tiempo de desarrollo encontrando una solución intermedia."},
                 {"text": "Desarrollar la interfaz desde cero como se pidió", "consequence": -3, "desc": "Asegura que el diseño se cumpla, pero es un esfuerzo técnico considerable."}
             ]
         }
     }}
]


# --- Gestión del Estado del Juego ---

def init_game():
    """Initializes the game state using Streamlit's session_state."""
    st.session_state.clear()
    st.session_state.screen = "intro"
    st.session_state.sprint_actual = 1
    st.session_state.puntos_totales = 0
    st.session_state.velocidad_equipo = 0
    st.session_state.product_backlog = get_initial_product_backlog()
    st.session_state.sprint_log = []
    st.session_state.sprint_backlog = []
    st.session_state.retrospective_bonus = None
    st.session_state.burndown_charts_data = {}
    st.session_state.available_obstacles = OBSTACLES.copy()
    st.session_state.available_multi_obstacles = MULTI_ROLE_OBSTACLES.copy()
    st.session_state.simulation_log = []

# --- Funciones de Ayuda y Renderizado ---

def log_event(sprint, day, event_type, details, consequence=0, capacity=0, points_done=0):
    """Adds a structured entry to the simulation log."""
    st.session_state.simulation_log.append({
        "Sprint": sprint, "Day": day, "Event Type": event_type,
        "Details": details, "Consequence (pts)": consequence,
        "Sprint Capacity": capacity, "Points Completed": points_done
    })

def get_name_from_display_string(display_str):
    """Extracts the original story name from the formatted display string."""
    clean_s = display_str.replace('**OBLIGATORIO** ', '')
    name_part = clean_s.split(' | ')[0]
    last_paren_index = name_part.rfind(' (')
    return name_part[:last_paren_index]

def update_sidebar():
    st.sidebar.header("📊 Estado del Proyecto")
    st.sidebar.metric("Sprint Actual", f"{st.session_state.sprint_actual} de 5")
    st.sidebar.metric("Puntos Totales Entregados", st.session_state.puntos_totales)
    velocidad_display = f"{st.session_state.velocidad_equipo} puntos" if st.session_state.velocidad_equipo > 0 else "Desconocida"
    st.sidebar.metric("Velocidad Base del Equipo", velocidad_display)
    if st.session_state.retrospective_bonus:
        st.sidebar.success(f"Bonus de Retrospectiva: {st.session_state.retrospective_bonus['desc']}")
    st.sidebar.subheader("📄 Resumen de Sprints")
    for log in st.session_state.sprint_log:
        st.sidebar.info(log)

def show_intro_screen():
    st.title("🚀 Simulador de Scrum: Proyecto Quetzal")
    st.header("Contexto del Caso")
    st.markdown("""
    Eres parte del equipo que lanzará **"Guate-Come"**, una nueva app de delivery de comida en Guatemala. El mercado es competitivo, con gigantes como Uber Eats y PedidosYa. Nuestra ventaja competitiva será la **hiper-localización**: enfocarnos en restaurantes pequeños y de barrio que los grandes ignoran, y ofrecer un servicio al cliente excepcional vía WhatsApp.

    El CEO ha invertido Q500,000 para el desarrollo inicial y quiere ver un producto funcional (MVP) en **5 Sprints** (de 5 días cada uno) para presentarlo a una nueva ronda de inversionistas.
    """)
    
    with st.expander("📘 Conceptos Clave: Puntos de Historia vs. Valor"):
        st.write("""
        - **Puntos de Historia (Esfuerzo):** Miden qué tan *grande* o *difícil* es una tarea para el **Equipo de Desarrollo**. No es tiempo, es una mezcla de complejidad, trabajo y riesgo.
        - **Valor (Importancia):** Mide qué tan *importante* es una tarea para el negocio. Es la perspectiva del **Product Owner**.
        
        *Una tarea puede ser muy fácil de hacer (pocos puntos) pero muy importante para el negocio (mucho valor), y viceversa.*
        """)

    st.subheader("Guía de Roles")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Product Owner**")
        st.write("- **Tu Objetivo:** Maximizar el Retorno de Inversión (ROI).\n- **Tu Decisión Clave:** ¿Qué construir? ¿Qué dejar para después?")
    with col2:
        st.warning("**Scrum Master**")
        st.write("- **Tu Objetivo:** Proteger al equipo y asegurar que el proceso Scrum se siga correctamente.\n- **Tu Decisión Clave:** ¿Cómo resolver los problemas sin afectar la capacidad del equipo?")
    with col3:
        st.error("**Development Team**")
        st.write("- **Tu Objetivo:** Entregar un incremento de software funcional y de alta calidad.\n- **Tu Decisión Clave:** ¿Cuánto trabajo podemos hacer? ¿Cómo resolvemos los problemas técnicos?")

    if st.button("Entendido, ¡a planificar!"):
        st.session_state.screen = "planning"
        st.rerun()

def show_planning_screen():
    st.header(f"Sprint #{st.session_state.sprint_actual}: 📝 Sprint Planning")

    st.subheader("Decisión del Product Owner: Priorizar el Backlog")
    st.markdown("Arrastra las historias para definir el orden de trabajo. Recuerda tu objetivo: maximizar el valor de negocio.")
    
    display_items = [f"{'**OBLIGATORIO** ' if item.get('mandatory') else ''}{item['name']} ({item['points']} pts) | Valor: {item['value']}" for item in st.session_state.product_backlog]
    sorted_display_items = sort_items(display_items, direction='vertical')
    
    backlog_map = {item['name']: item for item in st.session_state.product_backlog}
    new_sorted_backlog = [backlog_map[get_name_from_display_string(s)] for s in sorted_display_items]
    st.session_state.product_backlog = new_sorted_backlog

    st.write("---")
    st.subheader("Decisión del Equipo de Desarrollo: Seleccionar el Sprint Backlog")
    st.markdown("Selecciona las historias que el equipo se compromete a completar. Sé realista con tu capacidad.")

    options = [f"{'**OBLIGATORIO** ' if item.get('mandatory') else ''}{item['name']} ({item['points']} pts) | Valor: {item['value']}" for item in st.session_state.product_backlog]
    
    selected_stories_str = st.multiselect("Selecciona historias del Product Backlog (en orden de prioridad)", options)
    
    selected_names = [get_name_from_display_string(s) for s in selected_stories_str]
    puntos_planeados = sum(next(item['points'] for item in st.session_state.product_backlog if item['name'] == name) for name in selected_names)
            
    st.info(f"**Total de puntos planeados para este Sprint:** {puntos_planeados}")

    if st.button("▶️ Iniciar Sprint", disabled=(puntos_planeados == 0)):
        st.session_state.sprint_backlog = [item for item in st.session_state.product_backlog if item['name'] in selected_names]
        st.session_state.product_backlog = [item for item in st.session_state.product_backlog if item['name'] not in selected_names]
        
        st.session_state.sprint_day = 1
        st.session_state.sprint_capacity = st.session_state.velocidad_equipo if st.session_state.velocidad_equipo > 0 else random.randint(25, 35)
        st.session_state.sprint_obstacles_resolved = 0
        st.session_state.sprint_points_remaining = puntos_planeados
        st.session_state.burndown_data = [puntos_planeados]
        
        # NEW: Predetermine the schedule for the sprint
        sprint_days = [1, 2, 3, 4, 5]
        random.shuffle(sprint_days)
        st.session_state.problem_free_day = sprint_days.pop()
        st.session_state.multi_role_obstacle_day = sprint_days.pop()
        st.session_state.single_obstacle_days = sprint_days

        log_event(st.session_state.sprint_actual, 0, "Planning", f"Planeados {puntos_planeados} puntos.", 0, st.session_state.sprint_capacity, 0)

        st.session_state.screen = "daily_scrum"
        st.rerun()

def show_daily_scrum_screen():
    st.header(f"Sprint #{st.session_state.sprint_actual}: Día {st.session_state.sprint_day} de 5")
    
    # BUG FIX: This logic now correctly ensures exactly one problem-free day and handles transitions.
    if st.session_state.sprint_day > 5:
        calculate_sprint_outcome()
        st.session_state.screen = "review"
        st.rerun()

    current_day = st.session_state.sprint_day
    event_handled = False
    
    if current_day == st.session_state.multi_role_obstacle_day:
        if not st.session_state.available_multi_obstacles:
            st.session_state.available_multi_obstacles = MULTI_ROLE_OBSTACLES.copy() # Reshuffle if empty
        st.session_state.current_obstacle = st.session_state.available_multi_obstacles.pop(0)
        st.session_state.screen = "multi_obstacle_start"
        event_handled = True
    elif current_day in st.session_state.single_obstacle_days:
        if not st.session_state.available_obstacles:
            st.session_state.available_obstacles = OBSTACLES.copy() # Reshuffle if empty
        st.session_state.current_obstacle = st.session_state.available_obstacles.pop(random.randrange(len(st.session_state.available_obstacles)))
        st.session_state.screen = "obstacle"
        event_handled = True

    if event_handled:
        st.rerun()
    else: # This is the problem-free day
        st.success("El Daily Scrum transcurre sin problemas. El equipo sigue avanzando.")
        st.session_state.sprint_day += 1
        work_done = st.session_state.sprint_capacity / 5 
        st.session_state.sprint_points_remaining = max(0, st.session_state.sprint_points_remaining - work_done)
        st.session_state.burndown_data.append(st.session_state.sprint_points_remaining)
        if st.button("Siguiente Día"):
            st.rerun()


def show_obstacle_screen(multi_role_context=None):
    event = st.session_state.current_obstacle
    st.header(f"Sprint #{st.session_state.sprint_actual}: Día {st.session_state.sprint_day}")
    
    if multi_role_context:
        role, decision_data = multi_role_context
        st.subheader(f"⚡ ¡Decisión Colaborativa! (Parte {st.session_state.multi_decision_step}/2)")
        prompt = decision_data['prompt']
    else:
        role = event['role']
        st.subheader(f"⚡ ¡Obstáculo Detectado en el Daily Scrum!")
        prompt = f"*{event['icon']} **{event['title']}**: {event['description']}*"

    # Color-coded role indicator
    if role == "Product Owner": st.info(f"**Decisión para: {role}**")
    elif role == "Scrum Master": st.warning(f"**Decisión para: {role}**")
    else: st.error(f"**Decisión para: {role}**")
    st.markdown(prompt)

    choices = decision_data['choices'] if multi_role_context else event['choices']
    cols = st.columns(2)
    for i, choice in enumerate(choices):
        with cols[i % 2]:
            if st.button(f"{choice['text']}", help=choice['desc'], key=f"choice_{i}"):
                if multi_role_context:
                    st.session_state.multi_decision_step += 1
                    st.session_state.multi_choices.append({"role": role, "text": choice['text'], "consequence": choice['consequence']})
                    st.rerun()
                else:
                    log_event(st.session_state.sprint_actual, st.session_state.sprint_day, "Obstacle", f"{event['title']} - {choice['text']}", choice['consequence'], st.session_state.sprint_capacity + choice['consequence'])
                    st.session_state.last_consequence = choice['consequence']
                    st.session_state.last_consequence_text = f"La decisión de '{choice['text']}' resultó en un ajuste de **{choice['consequence']} puntos** a la capacidad del Sprint."
                    st.session_state.sprint_capacity += choice['consequence']
                    st.session_state.sprint_obstacles_resolved += 1
                    st.session_state.screen = "consequence"
                    st.rerun()

def show_multi_obstacle_flow():
    """Manages the multi-step decision process for a multi-role obstacle."""
    if 'multi_decision_step' not in st.session_state:
        st.session_state.multi_decision_step = 1
        st.session_state.multi_choices = []

    event = st.session_state.current_obstacle
    roles = list(event['decisions'].keys())

    if st.session_state.multi_decision_step == 1:
        role = roles[0]
        decision_data = event['decisions'][role]
        show_obstacle_screen(multi_role_context=(role, decision_data))
    elif st.session_state.multi_decision_step == 2:
        role = roles[1]
        decision_data = event['decisions'][role]
        show_obstacle_screen(multi_role_context=(role, decision_data))
    else: # Both decisions made
        st.session_state.screen = "multi_consequence"
        del st.session_state.multi_decision_step
        st.rerun()

def show_consequence_screen(is_multi=False):
    st.header(f"Sprint #{st.session_state.sprint_actual}: Día {st.session_state.sprint_day}")
    st.subheader("Resultado de la Decisión")
    
    total_consequence = 0
    if is_multi:
        event_title = st.session_state.current_obstacle['title']
        st.markdown(f"*{st.session_state.current_obstacle['icon']} **{event_title}***")
        log_details = f"{event_title} - "
        for choice in st.session_state.multi_choices:
            role = choice['role']
            text = f"La decisión del **{role}** ('{choice['text']}') tuvo una consecuencia de **{choice['consequence']}** puntos."
            log_details += f"{role}: {choice['text']}. "
            if choice['consequence'] < 0: st.error(text)
            else: st.success(text)
            total_consequence += choice['consequence']
        
        st.info(f"**Impacto Total en el Sprint:** {total_consequence} puntos.")
        st.session_state.sprint_capacity += total_consequence
        st.session_state.sprint_obstacles_resolved += 1
        log_event(st.session_state.sprint_actual, st.session_state.sprint_day, "Multi-Obstacle", log_details, total_consequence, st.session_state.sprint_capacity)

    else:
        consequence = st.session_state.last_consequence
        consequence_text = st.session_state.last_consequence_text
        if consequence < 0: st.error(f"**Consecuencia Negativa:** {consequence_text}")
        else: st.success(f"**Consecuencia Positiva:** {consequence_text}")

    work_done_today = st.session_state.sprint_capacity / 5
    st.session_state.sprint_points_remaining = max(0, st.session_state.sprint_points_remaining - work_done_today)
    st.session_state.burndown_data.append(st.session_state.sprint_points_remaining)
    st.session_state.sprint_day += 1

    if st.session_state.sprint_day > 5:
        calculate_sprint_outcome()
        st.session_state.screen = "review"
    else:
        st.session_state.screen = "daily_scrum"
    
    if st.button("Continuar con el Sprint"):
        if 'multi_choices' in st.session_state: del st.session_state.multi_choices
        st.rerun()

def show_review_screen():
    outcome = st.session_state.sprint_outcome
    st.header(f"Sprint #{st.session_state.sprint_actual}: 🔄 Sprint Review")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Capacidad Final del Sprint", outcome['capacidad_final'])
    col2.metric("Puntos Planeados", outcome['puntos_planeados'])
    col3.metric("Puntos Completados", outcome['puntos_completados'])
    
    if st.button("Ir a la Retrospectiva"):
        st.session_state.screen = "retrospective"
        st.rerun()

def show_retrospective_screen():
    st.header(f"Sprint #{st.session_state.sprint_actual}: 🙏 Sprint Retrospective")
    st.write("El equipo reflexiona. Como Scrum Master, guías la conversación.")
    st.subheader("¿Qué debería mejorar el equipo para el próximo Sprint?")

    choices = {
        "Mejorar la comunicación interna": {"bonus": "comunicacion", "desc": "Reduce el impacto negativo de los cambios del PO."},
        "Invertir en automatización de pruebas": {"bonus": "herramientas", "desc": "Reduce la probabilidad de encontrar deuda técnica."},
        "Fomentar el 'pair programming'": {"bonus": "mentoring", "desc": "Mejora el rendimiento al resolver problemas de dependencias o de juniors."},
        "Realizar un 'Team Building'": {"bonus": "moral", "desc": "Aumenta la moral del equipo, lo que puede llevar a descubrimientos tecnológicos positivos."},
        "Definir un 'Definition of Done' más estricto": {"bonus": "calidad", "desc": "Aumenta la calidad, pero podría reducir ligeramente la velocidad inicial del próximo sprint."}
    }

    for choice, data in choices.items():
        if st.button(choice, help=data["desc"]):
            st.session_state.retrospective_bonus = data
            st.session_state.sprint_actual += 1
            if 'intervention_shown' in st.session_state: del st.session_state.intervention_shown
            if st.session_state.sprint_actual > 5: st.session_state.screen = "end"
            else: st.session_state.screen = "planning"
            st.rerun()

def show_end_screen():
    st.balloons()
    st.title("🎉 ¡Simulación Completada!")
    
    final_score = st.session_state.puntos_totales
    penalty = 0
    mandatos_incumplidos = [story['name'] for story in st.session_state.product_backlog if story.get('mandatory')]
    
    if mandatos_incumplidos:
        penalty = 50
        final_score -= penalty
        st.error(f"**¡Mandatos Incumplidos!**")
        st.write("No completaste todas las historias obligatorias. El CEO está furioso. Sufres una penalización de **50** puntos.")
        for story in mandatos_incumplidos:
            st.write(f"- {story}")
    else:
        st.success("**¡Objetivos Cumplidos!**")
        st.write("¡Felicidades! Completaste todos los mandatos del CEO y lanzaste un MVP sólido.")

    st.metric("Puntuación Base", st.session_state.puntos_totales)
    st.metric("Penalización", f"-{penalty}")
    st.metric("Puntuación Final del Proyecto Quetzal", max(0, final_score))
    
    st.header("Gráficos Burndown de los Sprints")
    for i in range(1, 6):
        sprint_data = st.session_state.burndown_charts_data.get(i)
        if sprint_data:
            fig = generate_burndown_chart(sprint_data, i)
            st.pyplot(fig)

    # NEW: CSV Download Button
    st.header("Descargar Resultados")
    df = pd.DataFrame(st.session_state.simulation_log)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar reporte en CSV",
        data=csv,
        file_name='resultados_simulacion_scrum.csv',
        mime='text/csv',
    )
            
    if st.button("🔄 Reiniciar Simulación"):
        init_game()
        st.rerun()

# --- Lógica Principal y Gráficos ---

def calculate_sprint_outcome():
    puntos_planeados = sum(data['points'] for data in st.session_state.sprint_backlog)
    puntos_completados_calculados = round(puntos_planeados - st.session_state.sprint_points_remaining)
    
    historias_completadas = []
    historias_no_completadas = []
    
    temp_points = 0
    for story in st.session_state.sprint_backlog:
        if temp_points + story['points'] <= puntos_completados_calculados:
            temp_points += story['points']
            historias_completadas.append(story)
        else:
            historias_no_completadas.append(story)
    
    puntos_completados_reales = sum(h['points'] for h in historias_completadas)
    st.session_state.puntos_totales += puntos_completados_reales
    st.session_state.velocidad_equipo = st.session_state.sprint_capacity
    st.session_state.sprint_log.append(f"Sprint {st.session_state.sprint_actual}: {puntos_completados_reales} pts completados.")
    st.session_state.product_backlog.extend(historias_no_completadas)
    
    st.session_state.sprint_outcome = {
        "capacidad_final": st.session_state.sprint_capacity,
        "puntos_planeados": puntos_planeados,
        "puntos_completados": puntos_completados_reales,
        "historias_completadas": historias_completadas,
        "historias_no_completadas": historias_no_completadas
    }
    st.session_state.burndown_charts_data[st.session_state.sprint_actual] = st.session_state.burndown_data
    log_event(st.session_state.sprint_actual, 5, "Review", f"Completados {puntos_completados_reales} de {puntos_planeados} puntos.", 0, st.session_state.sprint_capacity, puntos_completados_reales)


def generate_burndown_chart(burndown_data, sprint_number):
    days = list(range(len(burndown_data)))
    if not days or len(days) < 2: return None
    
    total_points = burndown_data[0]
    ideal_line = [total_points - (total_points / (len(days) - 1)) * i for i in days]

    fig, ax = plt.subplots()
    ax.plot(days, burndown_data, marker='o', linestyle='-', label='Trabajo Restante (Real)')
    ax.plot(days, ideal_line, linestyle='--', label='Línea Ideal')
    ax.set_title(f'Burndown Chart - Sprint {sprint_number}')
    ax.set_xlabel("Día del Sprint")
    ax.set_ylabel("Puntos de Historia Restantes")
    ax.grid(True)
    ax.legend()
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    return fig

# --- Punto de Entrada del Script ---

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    if 'screen' not in st.session_state:
        init_game()

    update_sidebar()

    screen_to_show = st.session_state.get("screen", "intro")
    screens = {
        "intro": show_intro_screen,
        "planning": show_planning_screen,
        "daily_scrum": show_daily_scrum_screen,
        "obstacle": show_obstacle_screen,
        "multi_obstacle_start": show_multi_obstacle_flow,
        "consequence": show_consequence_screen,
        "multi_consequence": lambda: show_consequence_screen(is_multi=True),
        "review": show_review_screen,
        "retrospective": show_retrospective_screen,
        "end": show_end_screen
    }
    screens[screen_to_show]()
