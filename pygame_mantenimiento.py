import pygame
import sys
import os
import matplotlib.pyplot as plt
from properties import *
from pygame.locals import *
import pygame_gui

WHITE = (255, 255, 255)
GRAY = (112, 128, 144)
SEMIWHITE = (245, 245, 245)
SEMIWHITE2 = (240, 240, 240)
SEMIWHITE3 = (220, 220, 220)
LIGHTGRAY = (192, 192, 192)

class PGManten:
    """
    Clase para trabajar con pygame
    """
    def __init__(self, window_size=(1000, 650)):
        self.initialize_pygame()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 40)
        self.font_2 = pygame.font.SysFont('Arial', 20)
        self.font_3 = pygame.font.SysFont('Arial', 16)
        self.WINDOW_SIZE = window_size  # Tamaño ventana principal
        self.screen_form = pygame.display.set_mode(self.WINDOW_SIZE)
        self.logo = pygame.image.load(os.path.join('pics', 'logo.png')) # Carga logo utp
        #self.logo = pygame.transform.scale(self.logo, (118, 76))
        self.property_class = Property(workspace_size=(800, 460))  # Instancia de propiedades
        self.error = False  # Define si se produce una excepción

    @staticmethod
    def initialize_pygame():
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centra la interfaz
        pygame.display.set_caption('REL-Imp')

    def execute_pygame(self):
        manager = pygame_gui.UIManager((800, 600))

        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=manager)
        position_mouse = (0, 0)  # Inicializar posicion presionad
        grid = True  # Rejilla habilitada
        close = False
        timer = 0  # Necesario para el doble click
        dt = 0  # Incrementos del timer
        while not close:
            time_delta = self.clock.tick(60)/1000.0
            keys = pygame.key.get_pressed()  # Obtencion de tecla presionada
            for event in pygame.event.get():
                if self.property_class.draw:  # Eventos para texto de name
                    self.property_class.check_text(event)
                if event.type == pygame.QUIT:
                    close = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position_mouse = pygame.mouse.get_pos()
                    #print('pos', position_mouse)
                    if pygame.mouse.get_pressed()[0]:  # Boton izquierdo
                        if timer == 0 and self.property_class.modulos:
                            timer = 0.001
                        elif timer < 0.3 and not self.property_class.elem_type and self.property_class.modulos:  # Doble click apertura modulo/Debo bloquear esto mientras aun se este ejecutando el panel de propiedades
                            timer = 0
                            self.property_class.name_element.active = True  # Activar casilla de nombre propiedades
                            self.property_class.element_property(position_mouse, 1)  # Activar propiedad elemento
                            if self.property_class.elem_selected:
                                self.property_class.name_element.buffer = \
                                    [char for char in self.property_class.elem_selected]
                            # Aca se le pone al buffer el texto del elemento seleccionado
                            for container in self.property_class.elementos['containers']:  #Acciones de ingreso de texto
                                if container.selected:
                                    for caja in container.cajas:
                                        if caja.tag == self.property_class.elem_selected:
                                            self.property_class.box_field1.buffer = [char for char in str(caja.alpha)]  # se le pone a los buffers los valores de los elementos seleccionados
                                            self.property_class.box_field2.buffer = [char for char in str(caja.betha)]
                                    for knn_ind in container.knn:
                                        for col in knn_ind.cols:
                                            for caja in col:
                                                if caja.tag == self.property_class.elem_selected:
                                                    self.property_class.box_field1.buffer = \
                                                        [char for char in str(caja.alpha)]
                                                    self.property_class.box_field2.buffer = \
                                                        [char for char in str(caja.betha)]
                                    for stand_ind in container.stand:
                                        if stand_ind.tag == self.property_class.elem_selected:
                                            self.property_class.box_field1.buffer = [char for char in str(stand_ind.alpha)]
                                            self.property_class.box_field2.buffer = [char for char in str(stand_ind.betha)]
                                    for kdn in container.kdn:
                                        if kdn.tag == self.property_class.elem_selected:
                                            self.property_class.box_field1.buffer = [char for char in str(kdn.alpha)]
                                            self.property_class.box_field2.buffer = [char for char in str(kdn.betha)]
                        self.property_class.list_box_systems.consult_position(position_mouse)
                        if self.property_class.add_rect.collidepoint(position_mouse) \
                                and self.property_class.cont < 14:  # Agregar pestañas si son menos de 14
                            self.property_class.add_container()
                        if self.property_class.min_rect.collidepoint(position_mouse):
                            self.property_class.delete_container(position_mouse)  # Verificar si alguna pestaña se cierra
                        self.property_class.select_container(position_mouse, self.screen_form)  # Seleccionar pestaña
                        if not self.property_class.show_msg:
                            self.property_class.check_actions(position_mouse)  # verifica acciones
                        if not self.property_class.show_msg2:
                            self.property_class.check_actions(position_mouse)  # verifica acciones

                        self.property_class.close_elements(position_mouse)  # Cerrar elementos
                        self.property_class.add_red_elements(position_mouse)
                        for container in self.property_class.elementos['containers']:
                            container.list_box.scroll.action_bar(position_mouse)
                        self.property_class.list_box_systems.scroll.action_bar(position_mouse)
                        if self.property_class.show_msg:  # Si La ventana de mensajes esta disponible
                            if self.property_class.mensaje.accept.recta.collidepoint(position_mouse):
                                self.property_class.show_msg = False
                        if self.property_class.show_msg2:  # Si La ventana de mensajes esta disponible
                            if self.property_class.mensaje2.accept.recta.collidepoint(position_mouse):
                                self.property_class.actions = [0]*9
                                self.property_class.show_msg2 = False
                        if self.property_class.line_delete:
                            for container in self.property_class.elementos['containers']:
                                if container.selected:
                                    for conexion in container.conections:
                                        if conexion.elem1 == self.property_class.line_element.elem1 and conexion.elem2\
                                                == self.property_class.line_element.elem2:
                                            container.conections.remove(conexion)
                                            for nodo in container.nodos:
                                                nodo.connected = False
                                            for key in container.keys:  # Recorre nodos conectados
                                                # Busca los terminales de la conexion eliminada y los retira de algun nodo
                                                if conexion.elem1 in container.nodos_sistema[key] and \
                                                        conexion.elem2 in container.nodos_sistema[key]:
                                                    container.nodos_sistema[key].remove(conexion.elem1)
                                                    container.nodos_sistema[key].remove(conexion.elem2)

                                            self.property_class.line_element = None
                                            self.property_class.line_delete = False
                                            break

                        if self.property_class.connecting:  # Si se encuentra la linea de dibujo activa se pueden adicionar elementos a la conexion
                            self.property_class.duple_conection.append([self.property_class.init_pos, self.property_class.end_line])  # Todos los puntos de una conexion
                            self.property_class.points_conection.extend(self.property_class.build_rect_points(self.property_class.duple_conection[-1]))
                            if self.property_class.end_line != self.property_class.duple_conection[0][0]:
                                self.property_class.init_pos = self.property_class.end_line
                                for container in self.property_class.elementos['containers']:
                                    if container.selected:
                                        for nodo in container.nodos:
                                            if nodo.rect.collidepoint(self.property_class.end_line):
                                                self.property_class.hold_line = False  # Deja de dibujar la linea
                                                self.property_class.line_able = False  # Deja de habilitar linea
                                                self.property_class.connecting = False  # Deja de conectar
                                                self.property_class.elem2 = nodo  # Elemento final de la conexion
                                                conexion = Conexion(self.property_class.duple_conection,
                                                                                            self.property_class.elem1,
                                                                                            self.property_class.elem2,
                                                                    self.property_class.points_conection)
                                                container.conections.add(conexion)
                                                self.property_class.duple_conection = []
                                                self.property_class.points_conection = []
                                                # Verificar a que nodo del sistema van los nodos fisicos del objeto
                                                container.check_node(self.property_class.elem1, self.property_class.elem2)

                            else:
                                self.property_class.duple_conection.pop()
                        if self.property_class.actions[3]:  # Eliminar elemento
                            self.property_class.delete_element(position_mouse)
                        if self.property_class.actions[5]:  # importa modulo
                            if self.property_class.list_box_modules.accept2.recta.collidepoint(position_mouse):
                                self.property_class.draw_module = True
                                self.property_class.elem_modulo = self.property_class.list_box_modules.list_items[self.property_class.list_box_modules.conten_actual-1]
                        """if self.property_class.rect_up.collidepoint(position_mouse):
                            self.property_class.scroll()"""
                        if self.property_class.line_able:  # Permitir dibujar linea
                            self.property_class.hold_line = True
                        if self.property_class.drawing:  # Poner elemento
                            self.property_class.put_element()
                        if self.property_class.moving and self.property_class.move_inside:  # Redesplazar elemento
                            self.property_class.repos_element()
                        if self.property_class.check.recta.collidepoint(position_mouse):  # Para rotar cajitas
                            for container in self.property_class.elementos['containers']:
                                if container.selected:
                                    for caja in container.cajas:
                                        if caja.tag == self.property_class.elem_selected:
                                            conectado = True
                                            for nodo in caja.nodos:
                                                if nodo.connected:
                                                    conectado = False
                                            if conectado:
                                                caja.orientation = not caja.orientation
                                                self.property_class.check.push = caja.orientation
                                                for nodo in caja.nodos:
                                                    container.nodos.remove(nodo)
                                                caja.calc_nodes()
                                                for nodo in caja.nodos:
                                                    container.nodos.add(nodo)
                                            else:
                                                self.property_class.show_msg = True
                                                self.property_class.mensaje.text = 'El elemento debe estar desconectado'
                    elif pygame.mouse.get_pressed()[2] and self.property_class.modulos:  # Boton derecho
                        self.property_class.element_property(position_mouse)
                elif keys[K_ESCAPE]:  # Acciones al presionar tecla escape
                    position_mouse = self.property_class.cancel()
                    self.property_class.close_elements((0, 0), force=True)
                    self.property_class.box_field1.active = False
                    self.property_class.box_field2.active = False
                manager.process_events(event)
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == hello_button:
                            print('Hello World!')

            manager.update(time_delta)
            
            if timer != 0:  # Incremento del timer
                timer += dt
                if timer >= 0.5:  # Reinicio del timer
                    timer = 0
            abs_position = pygame.mouse.get_pos()
            self.screen_form.fill(SEMIWHITE2)
            self.property_class.draw_containers(self.screen_form)
            self.property_class.draw_on_screen(self.screen_form, abs_position, position_mouse)
            self.property_class.exec_actions(self.screen_form, abs_position, position_mouse)  # Ejecutar acciones: Mover, borrar...
            if self.property_class.actions[6] or self.property_class.elem_proper or self.property_class.config_bit \
                    or self.property_class.time_play or self.property_class.time_plot:  # Escribir nombre de pestañas
                self.property_class.draw_text(self.screen_form)
                self.property_class.draw = True
            if self.property_class.hold_line:  # Dibujando linea en caliente
                self.property_class.draw_line(self.screen_form)
            if self.property_class.element_moved != None:  # Mover elementos
                self.property_class.move_element(self.screen_form, abs_position)
                self.property_class.moving = True
            if self.property_class.show_msg:
                self.property_class.mensaje.draw(self.screen_form)
                if self.property_class.mensaje.accept.recta.collidepoint(abs_position):
                    self.property_class.mensaje.accept.over = True
                else:
                    self.property_class.mensaje.accept.over = False
            if self.property_class.show_msg2:
                self.property_class.mensaje2.draw(self.screen_form)
                if self.property_class.mensaje2.accept.recta.collidepoint(abs_position):
                    self.property_class.mensaje2.accept.over = True
                else:
                    self.property_class.mensaje2.accept.over = False
            self.screen_form.blit(self.logo, (20, 10))
            self.screen_form.blit(self.font.render('REL-Imp', True, (0, 0, 0)), (550, 20))
            self.screen_form.blit(self.font_2.render('Plataforma para la identificación de componentes críticos', True, (0, 0, 0)), (550, 65))
            #self.screen_form.blit(self.font_2.render('medida de la importancia', True, (0, 0, 0)), (30, 95))
            self.screen_form.blit(self.font_3.render('Editando sistema:', True, (0, 0, 0)), (760, 570))
            self.screen_form.blit(self.font_3.render(self.property_class.cont_selected.name, True, (0, 0, 0)), (870, 570))
            self.screen_form.blit(self.font_2.render('Sistemas', True, (0, 0, 0)), (50, 345))
            self.clock.tick(60)
            dt = self.clock.tick(30) / 1000  # Delta del timer
            #manager.draw_ui(self.screen_form)
            pygame.display.update()
