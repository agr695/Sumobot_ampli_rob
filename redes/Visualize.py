import pygame
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import tflearn
import tensorflow as tf
from tflearn.layers.merge_ops import merge
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_1d, global_max_pool

class window():
    """ Clase de visualizacion de mapas """
    def __init__(self, screen_size = (800,600), map_cell=20, map_offset=(100,100)):
        """ Se inicializan todos los puntos necesarios para poder usar pygame """
        # Colores que se pueden usar para el mapa
        self.colors = {'black': (0,0,0),
                        'white': (255,255,255),
                        'red': (255,0,0),
                        'green': (0,255,0),
                        'blue': (0,0,255),
                        'yel': (255,0,128)}

        # Tamano de la pantalla para mostrar el contenido
        self.display_width, self.display_height = screen_size

        # Tamano de la celda pintada
        self.cell = map_cell

        # Offset del mapa
        self.x_offset, self.y_offset = map_offset

        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Animation')

        self.clock = pygame.time.Clock()

    def quitting(self):
        """ En pygame mira para ver si se ha cerrado la pantalla,
        esto sirve para informarnos y poder cerrar la aplicacion
        sin tener que 'matar' la applicacion

        Tambien se podrian anadir otros botones como
            if event.type == event.KEYDOWN:
                if event.key == pygame.K_W:
        Esto por ejemplo captaria una pulsacion de la letra W"""

        finish = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

        return(finish)

    def cycle(self, mapa, init, lines):
        """ Muestra un ciclo de refresco en la pantalla """
        # Rellena la pantalla de un color
        self.gameDisplay.fill(self.colors['white'])

        ########### Lo que queremos que haga ###########
        self.show_map(mapa)
        self.show_lines(init, lines)
        # # # # # # # # # # # # # # # # # # # # # # # # #

        # Actualiza la pantalla
        pygame.display.update()

        # Pantalla con refresco 60 fps
        self.clock.tick(60)

    def show_map(self, nmap):
        """ Dibuja el mapa como cuadrados """
        for i, val in enumerate(nmap):
            for j, v in enumerate(val):
                if v == 1:
                    pygame.draw.rect(self.gameDisplay, self.colors['black'], (i*self.cell + self.x_offset, j*self.cell + self.y_offset, self.cell, self.cell))
                if v == 2:
                    pygame.draw.rect(self.gameDisplay, self.colors['green'], (i*self.cell + self.x_offset, j*self.cell + self.y_offset, self.cell, self.cell))
                if v == 3:
                    pass
                    #pygame.draw.rect(self.gameDisplay, self.colors['red'], (i*self.cell + self.x_offset, j*self.cell + self.y_offset, self.cell, self.cell))
                if v == 4:
                    pass
                    #pygame.draw.rect(self.gameDisplay, self.colors['blue'], (i*self.cell + self.x_offset, j*self.cell + self.y_offset, self.cell, self.cell))
                if v == 5:
                    pygame.draw.rect(self.gameDisplay, self.colors['yel'], (i*self.cell + self.x_offset, j*self.cell + self.y_offset, self.cell, self.cell))

    def application_2(self, cmap):
        """ Contiene todos los elementos para que la aplicacion funcione correctamente """
        finish = False
        mapa = cmap.get_map()

        while not finish:
            self.gameDisplay.fill(self.colors['white'])

            self.show_map(mapa)
            pygame.display.update()

            self.clock.tick(60)

            finish = self.quitting()

    def application(self, cmap, init, lines):
        """ Contiene todos los elementos para que la aplicacion funcione correctamente """
        finish = False
        mapa = cmap.get_map()

        while not finish:
            self.cycle(mapa, init, lines)

            finish = self.quitting()

        #pygame.quit()
        #quit()

    def mouse2map(self, mpos):
        """ Pasamos de posiciones de la pantalla a posiciones del mapa """
        x_map = int((mpos[0]-self.x_offset)/self.cell)
        y_map = int((mpos[1]-self.y_offset)/self.cell)

        return((x_map, y_map))

    def map2mouse(self, mpos, full=False):
        """ Pasa de valores de mapa a valores del mouse
        el full indica que queremos en coordendas absolutas
        o pixel a pixel"""

        if full == False:
            # Coordenadas absolutas(posicion inicial del punto)
            xmouse = int(self.cell*mpos[0] + self.x_offset)
            ymouse = int(self.cell*mpos[1] + self.y_offset)

        else:
            # Coordenadas no absolutas (Tiene en cuenta tambien posibles valores intermedios)
            xmouse = int(self.cell*mpos[0][0] + self.x_offset + mpos[0][1])
            ymouse = int(self.cell*mpos[1][0] + self.y_offset + mpos[1][1])

        return((xmouse, ymouse))

    def show_lines(self, init, lines):
        #print(lines)
        for l in lines:
            aux = [l[0] + self.x_offset, l[1] + self.y_offset]
            init2 = [init[0] + self.x_offset, init[1] + self.y_offset]

            pygame.draw.line(self.gameDisplay, self.colors['blue'], init2, aux, 1)

    def info(self):
        return(self.cell)

class terreno():
    """ Clase para crear los mapas a pintar, guardar, etc.. """
    def __init__(self):
        pass

    def create_map(self, map_size):
        self.map = np.zeros([map_size[0],map_size[1]], dtype=int)
        # Define los bordes del mapa
        for i in range(map_size[0]):
            for j in range(map_size[1]):
                if i == 0 or i == map_size[0]-1 or j==0 or j == map_size[1]-1:
                    self.map[i][j] = 1

    def get_map(self):
        return(self.map)

    def add_point(self, p, v):
        """ Anade un punto al mapa """
        self.map[p[0]][p[1]] = v

    def generate_random_map(self, nobs=3):
        """ Genera un mapa de dimensiones aleatorias y coloca los
        obstaculos """
        [w, h] = [random.randint(15,25), random.randint(15,25)]
        self.create_map([w, h])

        ntoo1 = random.randint(1,nobs)
        ntoo2 = nobs - ntoo1
        """
        for _ in range(ntoo1):
            self.create_obstacles(1, w, h)
        for _ in range(ntoo2):
            self.create_obstacles(0, w, h)
        """


    def create_obstacles(self, tipo, w, h):
        """ Crea los obstaculos de 2 tipos distintos """
        map_size = min(w, h)
        size = random.randint(2,math.ceil(map_size/4))
        if tipo == 0:
            # Crea elemento con forma de cuadrado
            size = math.ceil(size/2)
            centro = [random.randint(size, w-size-1), random.randint(size, h-size-1)]
            for i in range(centro[0]-size, centro[0]+size+1):
                for j in range(centro[1]-size, centro[1]+size+1):
                    self.map[i][j] = 1

        elif tipo == 1:
            # Crea linea
            d = random.randint(0,1)
            size = math.ceil(size/2)
            if d == 0:
                centro = [random.randint(size, w-size-1), random.randint(1, h-1)]
                for i in range(centro[0]-size, centro[0]+size+1):
                    self.map[i][centro[1]] = 1

            if d == 1:
                centro = [random.randint(1, w-1), random.randint(size, h-size-1)]
                for i in range(centro[1]-size, centro[1]+size+1):
                    self.map[centro[0]][i] = 1

    def create_position(self):
        """ Crea una posicion para el robot """
        finish = False
        while not finish:
            [x, y] = [random.randint(1, len(self.map)-1), random.randint(1, len(self.map[0])-1)]
            if self.map[x][y] != 1:
                finish = True
                self.map[x][y] = 2

        return([x, y])

    def create_targets(self, me):
        self.empty_burst(me)
        return(self.preprocess())

    def empty_burst(self, me):
        """ Rafaga de las lineas disparada desde el rayo
        encuentra las casillas donde se pueden encontrar
        los objetos a ser detectados """

        self.posible_targets = []
        self.posi = [me[0] + 0.5, me[1] + 0.5]

        for i in range(200):
            # Angulo en radianes que se va a ver
            """ Tener en cuenta que al dibujarlo como el 0,0 se encuentra en
            la esquina izq/sup el angulo correra en sentido de las agujas del
            reloj. Necesario que sea en radianes"""
            ang = 2*i*np.pi/200
            #print(ang*180/np.pi) # Ver angulo actua en grados

            cosa = np.cos(ang)
            sena = np.sin(ang)

            iter_end = False
            coff = 0
            soff = 0
            while not iter_end:
                coff, soff = self.rescale_empty(coff, soff, cosa, sena)

                col_pos = self.reconstruction_empty(coff, soff)

                if self.map[col_pos[0]][col_pos[1]] == 1:
                    #print(coff, soff)
                    iter_end = True
                if self.map[col_pos[0]][col_pos[1]] == 0:
                    self.map[col_pos[0]][col_pos[1]] = 3
                    if col_pos not in self.posible_targets:
                        self.posible_targets.append(col_pos)
            #print(detalle)
            #print('###################')

        return(self.posible_targets)

    def rescale_empty(self, coff, soff, cos_org, sen_org):
        """ Se approxima con una linea recta con un angulo determinado por
        el coseno y el seno. Va comprobando si ha llegado a un valor entero
        y guarda el valor double de la otra componente.

        Usandose de forma iterativa se puede ir avanzando de pixel en pixel
        y comporbar si se ha colisionado cn algun objeto y tener presicion
        en la medida de choque """

        #print(cos_org, sen_org)

        # Para alcanzar el siguente valor entero
        if coff%1 == 0.0:
            cint = coff + 1*np.sign(cos_org)
        else:
            cint = math.ceil(abs(coff))*np.sign(cos_org)

        if soff%1 == 0.0:
            sint = soff + 1*np.sign(sen_org)
        else:
            sint = math.ceil(abs(soff))*np.sign(sen_org)

        #print(cint, coff)
        #print(sint, soff)

        """ Para poder alcanzar el siguente punto tenermos los siguientes expresiones
        y = sen/cos * x + y_0  // x = cos/sen * y + x_0
        En la primera expresion queremos x/y=entero y en la otra y/x=entero
        El que nos de un valor menor sera el que determine la colision """

        if sen_org == 0.0:
            aux1 = np.inf
        else:
            aux1 = (sint - soff)/(sen_org/cos_org) # x/y=int
        if cos_org == 0.0:
            aux2 = np.inf
        else:
            aux2 = (cint - coff)/(cos_org/sen_org) # y/x=int

        #print(aux1, aux2)

        if abs(aux1) > abs(aux2): # Llega antes a x
            rcos = cint
            rsen = aux2 + soff
        if abs(aux2) > abs(aux1): # Llega antes a y
            rcos = aux1 + coff
            rsen = sint
        if abs(aux2) == abs(aux1):
            rcos = cint
            rsen = sint
        #print('asdffdsa')
        return(rcos, rsen)

    def reconstruction_empty(self, pos_x, pos_y):
        """ Con los valores de coff y soff los pasa a valores discretos
        dentro del mapa detallado.

        Lo aproximamos al valor mas bajo"""
        mov = [0, 0]
        mov[0] = math.floor((abs(pos_x))*np.sign(pos_x) + self.posi[0])
        mov[1] = math.floor((abs(pos_y))*np.sign(pos_y) + self.posi[1])

        return(mov)

    def preprocess(self):
        """ Procesa la posicion de lso posibles objetivos para que puedan ser 'muestreados'
        en su totalidad. Es decir, que el rayo pueda pasar por todo el objeto """
        self.non_map = self.map
        self.pretarget = []
        cont = 0
        for [x,y] in self.posible_targets:
            flag = True
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.non_map[x+i][y+j] == 1 or self.non_map[x+i][y+j] == 0 or self.non_map[x+i][y+j] == 2:
                        flag = False
            if flag == True:
                self.map[x][y] = 4
                self.pretarget.append([x,y])
                cont += 1

        return(cont)

            #print(len(self.pretarget))

    def set_target(self):
        """ De entre todas las posiciones definidas se elige una y se saca de la lista
        para no repetir ninguna posicion """
        maxi = len(self.pretarget)
        np = random.randint(0, maxi-1)
        target = self.pretarget[np]
        self.pretarget.pop(np)
        self.map[target[0]][target[1]] = 1
        ############# Ojo con que no se elimina del mapa el bicho
        self.tar = [target[0],target[1]]
        return(target)

    def erase_target(self):
        self.map[self.tar[0]][self.tar[1]] = 4

    def solution(self, me, target, nps=8):
        cos = target[0] - me[0]
        sen = target[1] - me[1]
        #print(cos, sen)

        ang = math.atan2(sen,cos)
        if ang < 0:
            ang = 2*np.pi + ang


        #print(ang*180/np.pi, ang)
        sol = np.zeros([nps, 1])
        sc = 2*np.pi/nps

        nsol = math.floor(abs(ang/sc))
        sol[nsol] = 1.0
        return(sol, [sc*nsol, sc*(nsol+1)], ang)

    def solution_lt(self, me, target, nps=200):
        cos = target[0] - me[0]
        sen = target[1] - me[1]

        ang = -math.atan2(sen,cos)

        #for i in range(-int((2*np.pi/(np.pi/4))/2), int((2*np.pi/(np.pi/4))/2)):
        #    print('################')
        #    print(i*np.pi/4)
        #    a = i * np.pi/4

        if ang < 0:
            ang = ang + 2*np.pi
        #    else:
        #        a2 = a

        #    print(a2)





        #ang = 2*np.pi - (ang + np.pi/2)

        sc = 2*np.pi/nps
        nsol = math.floor(abs(ang/sc))

        sol = nps - nsol

        return(sol)

class measurements():
    """ Clase para obtener las medidas """
    def __init__(self):
        pass

    def env_info(self, mapa, scale=20, resize=True):
        """ Obtiene informacion sobre el medio
        Para que sea mas preciso se puede usar el resize
        para que se pueda trabajar de forma mas precisa
        en caso de querer mostrarlo despues"""

        self.scale = scale

        if resize == True:
            x_len = len(mapa)*scale
            y_len = len(mapa[0])*scale
            self.map = np.zeros([x_len,y_len], dtype=int)

            # Reescala el mapa para tener mas detalles
            for i, val in enumerate(mapa):
                for j, v in enumerate(val):
                    if v != 0:
                        for m in range(i*self.scale, (i+1)*self.scale):
                            for n in range(j*self.scale, (j+1)*self.scale):
                                self.map[m][n] = v
        else:
            self.map = mapa

    def rescale(self, coff, soff, cos_org, sen_org):
        """ Se approxima con una linea recta con un angulo determinado por
        el coseno y el seno. Va comprobando si ha llegado a un valor entero
        y guarda el valor double de la otra componente.

        Usandose de forma iterativa se puede ir avanzando de pixel en pixel
        y comporbar si se ha colisionado cn algun objeto y tener presicion
        en la medida de choque """

        #print(cos_org, sen_org)

        # Para alcanzar el siguente valor entero
        if coff%1 == 0.0:
            cint = coff + 1*np.sign(cos_org)
        else:
            cint = math.ceil(abs(coff))*np.sign(cos_org)

        if soff%1 == 0.0:
            sint = soff + 1*np.sign(sen_org)
        else:
            sint = math.ceil(abs(soff))*np.sign(sen_org)

        #print(cint, coff)
        #print(sint, soff)

        """ Para poder alcanzar el siguente punto tenermos los siguientes expresiones
        y = sen/cos * x + y_0  // x = cos/sen * y + x_0
        En la primera expresion queremos x/y=entero y en la otra y/x=entero
        El que nos de un valor menor sera el que determine la colision """

        if sen_org == 0.0:
            aux1 = np.inf
        else:
            aux1 = (sint - soff)/(sen_org/cos_org) # x/y=int
        if cos_org == 0.0:
            aux2 = np.inf
        else:
            aux2 = (cint - coff)/(cos_org/sen_org) # y/x=int

        #print(aux1, aux2)

        if abs(aux1) > abs(aux2): # Llega antes a x
            rcos = cint
            rsen = aux2 + soff
        if abs(aux2) > abs(aux1): # Llega antes a y
            rcos = aux1 + coff
            rsen = sint
        if abs(aux2) == abs(aux1):
            rcos = cint
            rsen = sint
        #print('asdffdsa')
        return(rcos, rsen)

    def reconstruction(self, pos_x, pos_y):
        """ Con los valores de coff y soff los pasa a valores discretos
        dentro del mapa detallado.

        Lo aproximamos al valor mas bajo"""
        mov = [0, 0]
        mov[0] = int(math.floor(abs(pos_x))*np.sign(pos_x) + self.posi[0])
        mov[1] = int(math.floor(abs(pos_y))*np.sign(pos_y) + self.posi[1])

        return(mov)

    def line_record(self, line):
        """ Con el vector de colisiones determina el punto en coordenadas del
        mapa del punto inicial y final """

        l = []
        for v in line:
            vec = [0, 0]

            vec[0] = v[0] + self.posi[0]
            vec[1] = v[1] + self.posi[1]

            l.append(vec)

        return(self.posi, l)

    def burst(self, nb, myself):
        """ Rafaga de las lineas disparada desde el rayo """
        colisions = []

        self.posi = [myself[0][0]*self.scale + myself[1][0], myself[0][1]*self.scale + myself[1][1]]
        #print(self.posi)
        self.angles = []
        for i in range(nb):
            # Angulo en radianes que se va a ver
            """ Tener en cuenta que al dibujarlo como el 0,0 se encuentra en
            la esquina izq/sup el angulo correra en sentido de las agujas del
            reloj. Necesario que sea en radianes"""
            ang = 2*i*np.pi/nb
            #print(ang*180/np.pi) # Ver angulo actua en grados
            self.angles.append(ang)
            cosa = np.cos(ang)
            sena = np.sin(ang)

            iter_end = False
            coff = 0
            soff = 0
            while not iter_end:
                coff, soff = self.rescale(coff, soff, cosa, sena)

                col_pos = self.reconstruction(coff, soff)

                if self.map[col_pos[0]][col_pos[1]] == 1:
                    #print(coff, soff)
                    iter_end = True
            colisions.append([coff, soff])
            #print(detalle)
            #print('###################')
            self.perfect_meas(colisions)



        return(self.line_record(colisions))

    def perfect_meas(self, colisions):
        self.meas = colisions
        self.mod_meas = [math.sqrt(v[0]**2+v[1]**2) for v in colisions]

    def ret(self, wtr=0):
        if wtr == 0:
            return(self.mod_meas)
        elif wtr == 1:
            self.error()
            return(self.mod_meas_2)
        elif wtr == 2:
            return(self.angles)

    def batch_burst(self, size, start=0):
        self.sort_meas = []
        for i in range(size):
            #print(start, i, len(self.mod_meas))
            #print(self.mod_meas[start+i])
            if start + i >= len(self.mod_meas):
                self.sort_meas.append(self.mod_meas[start+i-len(self.mod_meas)])
            else:
                self.sort_meas.append(self.mod_meas[start+i])
        self.error_2()
        return(self.sort_meas)

    def swept(self, size):
        s = []
        for i in range(len(self.mod_meas)):
            s.append(self.batch_burst(size, i))

        return(s)

    def error(self):
        er = 0.02*(550 - 10)
        self.mod_meas_2 = [i+random.uniform(-er, er) for i in self.mod_meas]

    def error_2(self):
        er = 0.01*(550 - 10)
        self.sort_meas = [i+random.uniform(-er, er) for i in self.sort_meas]

class ploting():
    def __init__(self):
        pass

    def plot_graph(self, y, x,sol,ang):
        # Muestra un plot con la informacion y con separacion x
        plt.plot(x, y)
        plt.plot([sol[0],sol[1]],[0,0])
        plt.plot([ang,ang],[0, 300])
        plt.savefig('imagen1.png')
        plt.show()

    def b_plot(self, y, x, y1, x1):
        plt.subplot(211)
        plt.plot(x,y)
        plt.subplot(212)
        plt.plot(x1,y1)
        plt.show()

class ANN():
    def __init__(self, n1=6, n2=2, n=(80,80,80), learning_rate=1e-3, batch_size=100, hm_epochs=10, validation=0.2):
        self.lr = learning_rate
        self.n_in = n1
        self.n_out = n2
        self.neurons = n

        self.batch_size = batch_size
        self.lr = learning_rate
        self.n_epochs = hm_epochs
        self.validation = validation
        self.n_nodes_hl1 = 200
        self.n_nodes_hl2 = 200
        self.n_nodes_hl3 = 200

        self.filename = 'otro.out'

    def zero2one(self, t):
        """ Trasnforma las entradas entre 0-1"""
        maxi = 550
        mini = 10
        fin = []
        for i in t:
            if i < mini:
                fin.append(0.0)
            elif i > maxi:
                fin.append(1.0)
            else:
                fin.append(i/(maxi-mini))
        #print(fin)
        return(fin)

    def generate_data(self, env, meas, pts=20, nex=250, expmap=2):
        """ Genera un numero de mapas nex y en cada mapa un numero de
        ejemplos expmap

        Se usa un barrido de 360 grados"""
        training_data = []
        labels = []
        for _ in range(nex):
            env.create_random_map()
            me = env.create_position()
            env.create_targets(me)
            meas.env_info(env.get_map())
            for _ in range(expmap):
                target = env.set_target()
                meas.burst(pts, (me,(10,10)))
                training_data.append(meas.ret())
                labels.append(env.solution(me, target)[0])

        return(training_data, labels)

    def generate_data_lt(self, env, meas, pts=72, nex=250, expmap=5):
        """ Igual que el anterior pero cogiendo una pequena ventana"""
        training_data = []
        labels = []
        for j in range(nex):
            correct = False
            while not correct:
                env.generate_random_map()
                me = env.create_position()
                num = env.create_targets(me)
                if num > 15:
                    correct = True
                else:
                    correct = False

            for _ in range(expmap):
                target = env.set_target()
                meas.env_info(env.get_map())
                meas.burst(pts, (me,(10,10)))
                s = meas.swept(10)
                flag = 0
                for i in range(pts):
                    r = meas.batch_burst(self.n_in, i)

                    pos = env.solution_lt(me, target, pts)
                    mini = i
                    maxi = i+self.n_in if i+self.n_in < pts else i+self.n_in-pts
                    #print(mini, maxi, pos)
                    if pos < maxi and pos > mini:
                        labels.append([0.0, 1.0])
                        X = self.zero2one(r)
                        training_data.append(X)
                    else:
                        if flag == 0:
                            labels.append([1.0, 0.0])
                            X = self.zero2one(r)
                            training_data.append(X)
                            flag = 1
                        elif flag == 1:
                            flag = 2
                        elif flag == 2:
                            flag = 3
                        elif flag == 3:
                            flag = 4
                        elif flag == 4:
                            flag = 5
                        elif flag == 5:
                            flag = 6
                        else:
                            flag = 0

                    """if pos > i:
                        if i + bat > pts:
                            if i + bat - pts < pos:
                                labels.append(1.0)
                            else:
                                labels.append(0.0)
                        else:
                            if i + bat < pos:
                                labels.append(1.0)
                            else:
                                labels.append(0.0)
                    elif i + bat > pts:
                        labels.append(0.0)
                    else:
                        labels.append(0.0)
                    """

                env.erase_target()
            print(j)#, cont, sum(labels))
        #print(len(training_data),len(labels))
        a = sum([i[0] for i in labels])
        b = sum([i[1] for i in labels])
        print(a, b)
        return(training_data,labels)

    def build_ann(self, l):
        net = tflearn.input_data(shape=[None, l[0]])
        for i in range(1,len(l)-1):
            net = tflearn.fully_connected(net, l[i], bias=True, weights_init='truncated_normal', bias_init='zeros')#, activation='relu')

        net = tflearn.fully_connected(net, l[-1], bias=True, weights_init='truncated_normal', bias_init='zeros')#, activation='linear')
        net = tflearn.regression(net,  optimizer='adam', learning_rate=1e-2, loss='mean_square', name='target')

        return(net)

    def build_ann_2(self):

        tflearn.init_graph(num_cores=8, gpu_memory_fraction=0.5)
        net = tflearn.input_data(shape=[None, self.n_in])
        for i in range(len(self.neurons)):
            #print('#############2')
            net = tflearn.fully_connected(net, self.neurons[i], activation='relu',weights_init=tflearn.initializations.variance_scaling(seed=1234))#, activation='relu')

        net = tflearn.fully_connected(net, self.n_out, activation='linear', weights_init=tflearn.initializations.variance_scaling(seed=1234))#, activation='linear')
        net = tflearn.regression(net,  optimizer='adam', learning_rate=self.lr, loss='mean_square', name='target')
        model = tflearn.DNN(net, tensorboard_verbose=3, tensorboard_dir='log')

        return(model)

    def build_ann_3(self):
        tflearn.init_graph(num_cores=8, gpu_memory_fraction=0.5)
        net = tflearn.input_data(shape=[None, self.n_in])
        net = tflearn.embedding(net,input_dim=20,output_dim=32,name="embedding")

        b1 = tflearn.conv_1d(net, 32, 4, padding='same', activation='linear')
        b2 = tflearn.conv_1d(net, 32, 5, padding='same', activation='linear')

        net = merge([b1, b2], mode='concat', axis=1)
        net = tf.expand_dims(net, 2)
        net = global_max_pool(net)
        net = dropout(net, 0.5)

        net = tflearn.fully_connected(net, self.n_out, activation='linear', weights_init=tflearn.initializations.variance_scaling(seed=1234))#, activation='linear')
        net = tflearn.regression(net,  optimizer='adam', learning_rate=1e-3, loss='mean_square', name='target')#mean_square
        model = tflearn.DNN(net, tensorboard_verbose=3, tensorboard_dir='log')

        return(model)

    def train_ann(self, env, meas, sel=False):
        if sel == False:
            data, labels = self.generate_data_lt(env, meas)
            self.save_samples(data, labels)
        else:
            data, labels = self.load_samples()
        #print('De las ' + str(len(labels)) + ' son = 1: ' + str(sum(labels)))
        X = np.array([i for i in data]).reshape(-1, self.n_in)
        #rint(X[0])
        y = np.array([i for i in labels]).reshape(-1, self.n_out)
        self.model = self.build_ann_2()

        self.model.fit(X, y,  n_epoch=self.n_epochs, validation_set=0.1, shuffle=True, show_metric=True, run_id='AR_Proyect.tflearn')
        self.model.save('AR_Proyect.tflearn')

    def test_model(self, env, meas, pts=5, nex=20, expmap=4):
        training_data = []
        labels = []
        solnet = []
        for j in range(nex):
            correct = False
            while not correct:
                env.generate_random_map()
                me = env.create_position()
                num = env.create_targets(me)
                if num > 15:
                    correct = True
                else:
                    correct = False

            for _ in range(expmap):
                target = env.set_target()
                meas.env_info(env.get_map())
                meas.burst(pts, (me,(10,10)))
                s = meas.swept(10)
                flag = 0
                for i in range(pts):#range(int(pts/20)):
                    #i = i*20
                    r = meas.batch_burst(self.n_in, i)
                    #print(r, len(r))
                    pos = env.solution_lt(me, target, pts)
                    mini = i
                    maxi = i+self.n_in if i+self.n_in < pts else i+self.n_in-pts
                    #print(mini, maxi, pos)
                    #solnet.append(self.model.predict(r))
                    if pos < maxi and pos > mini:
                        #print(r))
                        x = self.zero2one(r)
                        #print(x)
                        X = np.array(x).reshape(-1, self.n_in)
                        #print(X)
                        labels.append([0.0, 1.0])
                        training_data.append(r)
                        solnet.append(self.model.predict(X))
                    else:
                        if flag == 0:
                            #print(r))
                            x = self.zero2one(r)
                            #print(x)
                            X = np.array(x).reshape(-1, self.n_in)
                            #print(X)
                            labels.append([1.0, 0.0])
                            training_data.append(r)
                            solnet.append(self.model.predict(X))
                            flag = 1
                        elif flag == 1:
                            flag = 2
                        elif flag == 2:
                            flag = 3
                        elif flag == 3:
                            flag = 4
                        elif flag == 4:
                            flag = 5
                        elif flag == 5:
                            flag = 6
                        else:
                            flag = 0
                env.erase_target()

        return(labels, solnet)

    def neural(self, data):
        hl_1 = {'weights':tf.Variable(tf.random_normal([self.n_in, self.n_nodes_hl1])),
                'biases':tf.Variable(tf.random_normal([self.n_nodes_hl1]))}

        hl_2 = {'weights':tf.Variable(tf.random_normal([self.n_nodes_hl1, self.n_nodes_hl2])),
                'biases':tf.Variable(tf.random_normal([self.n_nodes_hl2]))}

        hl_3 = {'weights':tf.Variable(tf.random_normal([self.n_nodes_hl2, self.n_nodes_hl3])),
                'biases':tf.Variable(tf.random_normal([self.n_nodes_hl3]))}

        outl = {'weights':tf.Variable(tf.random_normal([self.n_nodes_hl3, self.n_out])),
                'biases':tf.Variable(tf.random_normal([self.n_out]))}

        l1 = tf.add(tf.matmul(data, hl_1['weights']), hl_1['biases'])
        l1 = tf.nn.relu(l1)

        l2 = tf.add(tf.matmul(l1, hl_2['weights']), hl_2['biases'])
        l2 = tf.nn.relu(l2)

        l3 = tf.add(tf.matmul(l2, hl_3['weights']), hl_3['biases'])
        l3 = tf.nn.relu(l3)
        l3 = tf.nn.dropout(l3, 0.8)

        out = tf.add(tf.matmul(l3, outl['weights']), outl['biases'])

        #tf.nn.dropout(out, 0.6)

        return(out)

    def neural_conv(self, data):
        weights = {'W_conv1': tf.Variable(tf.random_normal([4,1,32])),
                    'W_conv2': tf.Variable(tf.random_normal([5, 16, 32])),
                    'W_fc': tf.Variable(tf.random_normal([5*32, 512])),
                    'out': tf.Variable(tf.random_normal([1024, 2]))}

        biases = {'b_conv1': tf.Variable(tf.random_normal([32])),
                    'b_conv2': tf.Variable(tf.random_normal([32])),
                    'b_fc': tf.Variable(tf.random_normal([512])),
                    'out': tf.Variable(tf.random_normal([2]))}

        data = tf.reshape(data, shape=[-1, 20, 1])

        conv1 = tf.nn.relu(conv1d(data, weights['W_conv1']) + biases['b_conv1'])
        conv1 = maxpool1d(conv1)

        conv2 = tf.nn.relu(conv1d(conv1, weights['W_conv2']) + biases['b_conv2'])
        conv2 = maxpool1d(conv2)

        fc = tf.reshape(conv2, [-1, 5*32])
        fc = tf.nn.relu(tf.matmul(fc, weights['W_fc']) + biases['b_fc'])
        fc = tf.nn.dropout(fc, 0.8)

        output = tf.matmul(fc, weights['out']) + biases['out']

        return(output)

    def train(self, env, meas):
        x = tf.placeholder('float', [None, self.n_in])
        y = tf.placeholder('float')

        prediction = self.neural(x)
        print('########')
        print(y)

        cost= tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
        optimizer=tf.train.AdamOptimizer().minimize(cost)
        X, Y = self.generate_data_lt(env, meas)
        x_train = X[0:int(len(X)*(1-self.validation))]
        x_test = X[int(len(X)*(1-self.validation)):len(X)]
        y_train = Y[0:int(len(Y)*(1-self.validation))]
        y_test = Y[int(len(Y)*(1-self.validation)):len(X)]

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for epoch in range(self.n_epochs):
                epoch_loss = 0
                for i in range(int(len(x_train)/self.batch_size)):
                    epoch_x = x_train[self.batch_size*i:self.batch_size*(i+1)]
                    pepoch_y = y_train[self.batch_size*i:self.batch_size*(i+1)]
                    epoch_y = np.array([i for i in pepoch_y]).reshape([100,2])
                    _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                    epoch_loss += c
                print('Epoch', epoch, 'completed out of', self.n_epochs, 'loss:',epoch_loss)

            correct= tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
            accuracy= tf.reduce_mean(tf.cast(correct,'float'))
            y_test = np.array([i for i in y_test]).reshape([len(y_test),2])
            print('Accuracy:',accuracy.eval({x:x_test, y:y_test}))

    def train_conv(self, env, meas):
        x = tf.placeholder('float', [None, self.n_in])
        y = tf.placeholder('float')

        keep_prob = tf.placeholder(tf.float32)

        prediction = self.neural_conv(x)
        print('########')
        print(y)

        cost= tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
        optimizer=tf.train.AdamOptimizer().minimize(cost)
        X, Y = self.generate_data_lt(env, meas)
        x_train = X[0:int(len(X)*(1-self.validation))]
        x_test = X[int(len(X)*(1-self.validation)):len(X)]
        y_train = Y[0:int(len(Y)*(1-self.validation))]
        y_test = Y[int(len(Y)*(1-self.validation)):len(X)]

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for epoch in range(self.n_epochs):
                epoch_loss = 0
                for i in range(int(len(x_train)/self.batch_size)):
                    epoch_x = x_train[self.batch_size*i:self.batch_size*(i+1)]
                    pepoch_y = y_train[self.batch_size*i:self.batch_size*(i+1)]
                    epoch_y = np.array([i for i in pepoch_y]).reshape([100,2])
                    _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                    epoch_loss += c
                print('Epoch', epoch, 'completed out of', self.n_epochs, 'loss:',epoch_loss)

            correct= tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
            accuracy= tf.reduce_mean(tf.cast(correct,'float'))
            y_test = np.array([i for i in y_test]).reshape([len(y_test),2])
            print('Accuracy:',accuracy.eval({x:x_test, y:y_test}))

    def save_samples(self, X, y):
        f = open(self.filename, 'a')
        #print(X)
        #print(y)
        for i, j in zip(X, y):
            for i2 in i:
                f.write(str(i2) + ',')
            f.write('\n')
            for j2 in j:
                f.write(str(j2) + ',')
            f.write('\n')
        f.close()

    def load_samples(self):
        f = open(self.filename, 'r')

        lines = f.readlines()

        X = []
        y = []

        for c,i in enumerate(lines):
            s = i.split(',')
            s.pop(-1)
            s = [float(i) for i in s]

            if c%2 == 0:
                X.append(s)
            else:
                y.append(s)

        #print(X)
        #print(y)
        f.close()

        return(X,y)

    def load_model(self):
        self.model = self.build_ann_2()

        self.model = self.model.load('AR_Proyect.tflearn')

        return(self.model)

    def prediction(self, X):
        return(self.model.predict(X))

def conv1d(x, W):
  return tf.nn.conv1d(x, W, stride=1, padding='SAME')

def maxpool1d(x):
  return tf.layers.max_pooling1d(x, pool_size=4, strides=1, padding='SAME')

def try_map():
    win = window()
    env = terreno()
    meas = measurements()

    env.generate_random_map()
    me = env.create_position()
    env.create_targets(me)
    target = env.set_target()
    win.application_2(env)
    env.erase_target()
    target = env.set_target()
    win.application_2(env)
    env.erase_target()


    pygame.quit()
    quit()

def try_meas():
    win = window()
    env = terreno()
    meas = measurements()
    p = ploting()
    ar = ANN()
    pts = 200

    env.generate_random_map()

    meas.env_info(env.get_map())
    me = env.create_position()
    env.create_targets(me)
    target = env.set_target()
    meas.env_info(env.get_map())
    ini, lin = meas.burst(pts, (me,(10,10)))
    win.application(env, ini, lin)
    pos = env.solution_lt(me, target, pts)
    print(pos)

    r = meas.batch_burst(20, 3*20)

    t = [j for j in range(0,len(r))]
    p.b_plot(r, t,meas.ret(1), meas.ret(2))
    """
    for i in range(0,10):
        r = meas.batch_burst(20, i*20)
        t = [j+i*20 for j in range(0,len(r))]
        r2 = ar.zero2one(r)
        p.b_plot(r2, t,meas.ret(), meas.ret(2))
    """
    env.erase_target()
    print('eh')
    """
    target = env.set_target()
    meas.env_info(env.get_map())
    ini, lin = meas.burst(pts, (me,(10,10)))
    win.application(env, ini, lin)
    env.erase_target()
    """

    #p.b_plot(meas.ret(), meas.ret(2))
    print('oh')

    pygame.quit()
    quit()

def train_to_see_what_the_hell_happen():
    #win = window()
    env = terreno()
    meas = measurements()

    ar = ANN()

    ar.train_ann(env, meas)

#try_meas()
#train_to_see_what_the_hell_happen()

#env = terreno()

#print(env.solution_lt([0,0], [1,-1], nps=200))


#train_to_see_what_the_hell_happen()
"""
win = window()
env = terreno()
meas = measurements()
pt = ploting()
env.create_map((20,20))
env.add_point((10,7), 1)
meas.env_info(env.get_map(), win.info())
init, lines = meas.burst(200, ((5,5),(10,10)))
#pt.plot_graph(meas.ret(), meas.ret(2))
win.application(env, init, lines)
pygame.quit()
quit()
"""

"""
env = terreno()
win = window()
meas = measurements()
pt = ploting()
env.generate_random_map()
me = env.create_position()
env.create_targets(me)
tar = env.set_target()
meas.env_info(env.get_map(), win.info())
init, lines = meas.burst(200, (me,(10,10)))
print(env.solution(me, tar))
pt.plot_graph(meas.ret(), meas.ret(2), env.solution(me, tar)[1], env.solution(me,tar)[2])
print(meas.ret())
print(meas.swept(10))
win.application(env, init, lines)
"""

win = window()
env = terreno()
meas = measurements()


ar = ANN()

#ar.train_ann(env, meas)
ar.train_ann(env,meas,False)

a, b = ar.test_model(env, meas, 72, 50, expmap=1)
#ar.generate_data_lt(env, meas, 200, 20, nex=1, expmap=1)
#print(a)
#print(b)
cont = 0
cont1p = 0
cont2p = 0
cont1 = 0
cont2 = 0
cont1n = 0
cont2n = 0
for i, j in zip(a,b):
    #print(i, j)
    #print('================')
    #print(i,j[0][0])
    cont += 1
    if i[1] ==1.0:
        cont1 += 1
        if int(i[1]) == int(round(j[0][1])):
            cont1p += 1
            #print('si')
        elif int(i[0]) == int(round(j[0][0])):
            #print('no')
            cont1n += 1
        else:
            pass

    elif i[1] == 0.0:
        cont2 += 1
        if int(i[0]) == int(round(j[0][0])):
            cont2p += 1
            #print('si')
        elif int(i[1]) == int(round(j[0][1])):
            #print('no')
            cont2n += 1

print(cont)
print('Con obstaculo se ha detectado correctamente ' + str(cont1p) + ' de ' +str(cont1) + ' ==> ' + str(cont1p/cont1))
print('Sin obstaculo se ha detectado correctamente ' + str(cont2p) + ' de ' +str(cont2) + ' ==> ' + str(cont2p/cont2))
print('Obstaculo falso ' + str(cont1n) + ' de ' +str(cont1) + ' ==> ' + str(cont1n/cont1))
print('Vacio falso ' + str(cont2n) + ' de ' +str(cont2) + ' ==> ' + str(cont2n/cont2))

"""
#ar = ANN()
#ar.train_conv(env, meas)
#ar.train_ann(env, meas)
"""
