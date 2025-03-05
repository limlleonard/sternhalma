from math import pi, cos, sin
width_board, height_board=720, 720
CENTERX, CENTERY=width_board/2, height_board/2
diameterField=30
diameterPiece=24
DISTCC=40 # center-center distance
Middle_Layer=4 # layer of circles outside of the center circle, it builds up a hexagon. Beyond this layer will be 6 corners

def rotate_point(pc, p1, nr_angle):
    cx, cy = pc
    x1, y1 = p1
    angle_rad = 2*pi*nr_angle/6
    # Translate point to origin
    translated_x = x1 - cx
    translated_y = y1 - cy
    # Rotate point
    x2 = translated_x * cos(angle_rad) - translated_y * sin(angle_rad)
    y2 = translated_x * sin(angle_rad) + translated_y * cos(angle_rad)
    # Translate point back
    x2 += cx
    y2 += cy
    return (x2, y2)

class Board():
    def __init__(self):
        """(nr_layer, nr_beam(0-5), nr_side perpendicular to beam):(x,y)
        lst_board, lst_board_round saves the coord of all positions in the same order"""
        self.dct_board=self.init_dict()
        self.lst_board=[self.dct_board[a1] for a1 in self.dct_board]
        self.lst_board_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_board]

    def init_dict(self):
        dct_board={}
        dct_board[(0,0,0)]=(CENTERX, CENTERY)
        for nr_layer in range(1, Middle_Layer*2+1):
            r1=DISTCC*nr_layer # Distance from center to the current layer
            nr_circles_layer=nr_layer # Number of circles on this layer
            nr_skip=nr_layer-Middle_Layer
            for direction in range(6):
                angle1=(direction*2*pi)/6
                x1, y1=CENTERX+r1*cos(angle1), CENTERY+r1*sin(angle1)
                # fantacy next point to calculate the coordinate of points in between
                angle2=((direction+1)*2*pi)/6
                x2, y2=CENTERX+r1*cos(angle2), CENTERY+r1*sin(angle2)
                if nr_skip<1: # inside the middle layer
                    for nr_circle_layer in range(nr_circles_layer):
                        x3=x1+(x2-x1)*nr_circle_layer/nr_circles_layer
                        y3=y1+(y2-y1)*nr_circle_layer/nr_circles_layer
                        dct_board[(nr_layer, direction, nr_circle_layer)]=(x3, y3)
                else: # outer layers / corners
                    for nr_circle_layer in range(nr_skip, nr_circles_layer-nr_skip+1):
                        x3=x1+(x2-x1)*nr_circle_layer/nr_circles_layer
                        y3=y1+(y2-y1)*nr_circle_layer/nr_circles_layer
                        dct_board[(nr_layer, direction, nr_circle_layer)]=(x3, y3)
        return dct_board
    
class Spieler():
    def __init__(self, init_dir=1):
        self.lst_piece=self.init_group(init_dir)
        self.lst_piece_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_piece]
        self.lst_target=self.init_group(init_dir+3)
        self.lst_target_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_target]
        self.selected=None # coord of the selected figur
        self.valid_pos=[]
        self.gewonnen=False

    def init_group(self, init_dir):
        """Initialize die Stelle der """
        lst_piece=[]
        for k in range(Middle_Layer+1, Middle_Layer*2+1):
            radius = DISTCC * k  # Distance for the current layer
            num_circles_layer = k  # Number of circles in this layer
            num_to_skip = k - Middle_Layer

            angle = (init_dir * 2 * pi) / 6  # init_dir entscheidet, so die Stücke am Anfang legen
            x = CENTERX + radius * cos(angle)
            y = CENTERY + radius * sin(angle)
            # Fantacy 'next point' to calculate the coordinate of points in between
            angle1 = ((init_dir + 1) * 2 * pi) / 6
            x1 = CENTERX + radius * cos(angle1)
            y1 = CENTERY + radius * sin(angle1)

            for j in range(num_to_skip, num_circles_layer - num_to_skip + 1):
                x2 = x + (x1 - x) * j / num_circles_layer
                y2 = y + (y1 - y) * j / num_circles_layer
                lst_piece.append((round(x2), round(y2)))
        return lst_piece

    def win_check(self):
        sorted_lst_piece=sorted(self.lst_piece_round)
        sorted_lst_ziel=sorted(self.lst_target_round)
        if sorted_lst_piece==sorted_lst_ziel:
            self.gewonnen=True

    def rotate(self, lst_piece):
        return [(2*CENTERX-x, 2*CENTERY-y) for (x,y) in lst_piece]

class Spiel():
    def save():
        # save to django instance. 
        # stones
        pass
    def __init__(self, nr_spieler=2):
        self.board=Board()
        self.spieler=[]
        self.order=0
        self.dct_dir={1: [1], 2: [1,4], 3: [1,3,5], 4:[1,4,2,5], 5:[1,3,5,2,4], 6:[1,3,5,2,4,6]}
        # self.reset(nr_spieler)
        # self.spieler_rotate=[]
    
    def reset(self, nr_spieler=2):
        self.spieler=[]
        for nr1 in range(nr_spieler):
            init_dir=self.dct_dir[nr_spieler][nr1]
            self.spieler.append(Spieler(init_dir))
        self.order=0 # self.spieler[self.order] ist der Spieler, der dran ist

    def get_precise_coord(self, coord_round):
        """find the index in lst_board_round, then return the value from lst_board"""
        return self.board.lst_board[self.board.lst_board_round.index(coord_round)]
    
    def find_neighbors(self, coord_round):
        """6 positionen rund um der Figur + 6 positionen darüber"""
        x,y=self.get_precise_coord(coord_round)
        lst_neighbor=[]
        for i in range(6):
            angle=i*2*pi/6
            x1=round(x+DISTCC*cos(angle))
            y1=round(y+DISTCC*sin(angle))
            x2=round(x+2*DISTCC*cos(angle)) # position über dem direkten Nachbar
            y2=round(y+2*DISTCC*sin(angle))
            lst_neighbor.append(((x1, y1), (x2, y2)))
        return lst_neighbor
    
    def get_ll_piece(self):
        ll_piece=[] # Figuren aller Farben berückwichtigen
        for spieler1 in self.spieler:
            ll_piece.append(spieler1.lst_piece_round)
        return ll_piece

    def find_valid_pos(self, coord_round):
        visited=set()
        valid_pos=[]
        ll_piece=self.get_ll_piece()
        lst_piece=[coord for figuren in ll_piece for coord in figuren] # Figuren aller Farben berückwichtigen
        lst_neighbor=self.find_neighbors(coord_round)
        for coord1, _ in lst_neighbor: # no jump
            # if it is in board but not in pieces
            if coord1 in self.board.lst_board_round and coord1 not in lst_piece:
                valid_pos.append(coord1)

        def dfs(coord_round):
            if coord_round in visited:
                return  # Skip if already visited
            visited.add(coord_round)  # Mark node as visited
            valid_pos.append(coord_round)  # Add node to connected list

            lst_neighbor1 = self.find_neighbors(coord_round)
            for coord1, coord2 in lst_neighbor1:
                if (coord2 not in visited and
                    coord1 in lst_piece and
                    coord2 not in lst_piece and 
                    coord2 in self.board.lst_board_round):
                    dfs(coord2)
        dfs(coord_round)
        return valid_pos

    def klicken(self, coord_round):
        # coord_from=coord_to=None
        neue_figuren=None
        spieler=self.spieler[self.order]
        if coord_round in spieler.lst_piece_round: # auf einer der Figuren klickt
            # if spieler.selected is not None:
            #     spieler.valid_pos=[]
            spieler.valid_pos=self.find_valid_pos(coord_round)
            if len(spieler.valid_pos)>0: # Nur ein Figur, das bewegen kann, darf gewählt werden
                spieler.selected=coord_round
        elif spieler.selected and coord_round in spieler.valid_pos:
            # move piece, pop the old piece and insert the new piece
            index_from=spieler.lst_piece_round.index(spieler.selected)
            # coord_from=spieler.selected
            spieler.lst_piece_round.pop(index_from)
            spieler.lst_piece.pop(index_from)
            spieler.lst_piece_round.append(coord_round)
            spieler.lst_piece.append(self.get_precise_coord(coord_round))
            # coord_to=coord_round
            spieler.selected=None
            spieler.valid_pos=[]
            spieler.win_check()
            self.order=(self.order+1)%len(self.spieler) # next
            neue_figuren=self.get_ll_piece() # wenn neue_figuren nicht None, bedeutet ein Bewegung wird gemacht
        return spieler.selected, spieler.valid_pos, neue_figuren, self.order, spieler.gewonnen

    def get_rotate_spieler(self, nr_angle):
        """Rotate all the player and return them"""
        spieler_rotate=[]
        for spieler_alt in self.spieler:
            spieler_neu=spieler_alt.copy()
            spieler_neu.lst_piece=[rotate_point((CENTERX, CENTERY), p1, nr_angle) for p1 in spieler_neu.lst_piece]
            spieler_neu.lst_piece_round=[(round(coord[0]), round(coord[1])) for coord in spieler_neu.lst_piece]
            spieler_neu.lst_target=[rotate_point((CENTERX, CENTERY), p1, nr_angle) for p1 in spieler_neu.lst_target]
            spieler_neu.lst_target_round=[(round(coord[0]), round(coord[1])) for coord in spieler_neu.lst_target]
        return spieler_rotate
# todos: reset, win check, add player, turn board, swap turns
