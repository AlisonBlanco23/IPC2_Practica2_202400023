from graphviz import Digraph
import os

class VisualizadorGraphviz:
    def __init__(self, filename="cola_turnos"): 
        self.filename = filename
        self.ruta_base = r"C:\Users\aliso\OneDrive\Documentos\USAC\Cuarto semestre\Programación\IPC2\Practica 2"

    def generar_grafo(self, nodo_frente):
        dot = Digraph(comment='Cola de Turnos Médicos')
        dot.attr(dpi='200')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='rectangle', style='filled', fontname='Arial', fontsize='11')
        dot.attr('edge', fontname='Arial', fontsize='10')

        if nodo_frente is None:
            dot.node('empty', '¡No hay pacientes en espera!', shape='note', fillcolor='lightgreen', fontname='Arial', fontsize='14', fontcolor='darkgreen')
        else:
            actual = nodo_frente
            i = 0
            prev_node_id = None
            tiempo_acumulado_espera = 0

            while actual is not None:
                paciente = actual.paciente
                tiempo_atencion_paciente = paciente.obtener_tiempo_atencion()
                tiempo_total_paciente = tiempo_acumulado_espera + tiempo_atencion_paciente

                label = f"""<<B>Paciente {i+1}</B><BR/>{paciente.nombre}<BR/><FONT POINT-SIZE="10">{paciente.edad} años</FONT><BR/>{paciente.especialidad}<BR/><FONT POINT-SIZE="10">Total: {tiempo_total_paciente} min</FONT>>"""

                current_node_id = f"p{i}"

                colores = {
                    "Medicina General": "#AED6F1",
                    "Pediatría": "#FADBD8",
                    "Ginecología": "#D5F5E3",
                    "Dermatología": "#EBDEF0"
                }
                fillcolor = colores.get(paciente.especialidad, "#FDEDEC")

                dot.node(current_node_id, label, fillcolor=fillcolor, color="black", penwidth="2")

                if prev_node_id is not None:
                    dot.edge(prev_node_id, current_node_id, label=" → ", fontcolor="blue", color="blue", penwidth="2")

                prev_node_id = current_node_id
                tiempo_acumulado_espera += tiempo_atencion_paciente
                actual = actual.siguiente
                i += 1

        ruta_completa = os.path.join(self.ruta_base, self.filename)
        dot.render(ruta_completa, format='png', cleanup=True)
        print(f"Gráfico generado en: {ruta_completa}.png")

    def obtener_ruta_imagen(self) -> str:
        return os.path.join(self.ruta_base, f"{self.filename}.png") 