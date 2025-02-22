from django.db import models
from math import pi, cos, sin
width_board, height_board=720, 720
centerx, centery=width_board/2, height_board/2
diameterField=30
diameterPiece=24
distcc=40 # center-center distance
Middle_Layer=4 # layer of circles outside of the center circle, it builds up a hexagon. Beyond this layer will be 6 corners

class Spieler():
    def __init__(self):
        pass

class Board():
    def __init__(self, centerx, centery, distcc, init_dir=1, nr_spieler=1):
        self.distcc=distcc # center-center distance
        self.nr_spieler=nr_spieler
        self.spieler=[]
        self.dct_board=self.init_dct(centerx, centery, distcc)
        self.lst_board=[self.dct_board[a1] for a1 in self.dct_board]
        self.lst_board_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_board]

        self.lst_piece=self.init_pieces(centerx, centery, distcc, init_dir)
        self.lst_piece_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_piece]
        self.lst_ziel=self.init_pieces(centerx, centery, distcc, init_dir+3)
        self.lst_ziel_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_ziel]
        self.selected=None
        self.valid_pos=[]
        self.gewonnen=False
    def reset(self, centerx, centery, distcc, init_dir=1):
        self.lst_piece=self.init_pieces(centerx, centery, distcc, init_dir)
        self.lst_piece_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_piece]
        self.lst_ziel=self.init_pieces(centerx, centery, distcc, init_dir+3)
        self.lst_ziel_round=[(round(coord[0]), round(coord[1])) for coord in self.lst_ziel]
        self.selected=None
        self.valid_pos=[]
        self.gewonnen=False
    def init_spieler(self, nr_spieler):
        for n1 in range(nr_spieler):
            pass
        pass
    def init_dct(self, centerx, centery, distcc):
        """(nr_layer, nr_beam(0-5), nr_side perpendicular to beam):(x,y)"""
        dct_board={}
        dct_board[(0,0,0)]=(centerx, centery)
        for nr_layer in range(1, Middle_Layer*2+1):
            r1=distcc*nr_layer # Distance from center to the current layer
            nr_circles_layer=nr_layer # Number of circles on this layer
            nr_skip=nr_layer-Middle_Layer
            for direction in range(6):
                angle1=(direction*2*pi)/6
                x1, y1=centerx+r1*cos(angle1), centery+r1*sin(angle1)
                # fantacy next point to calculate the coordinate of points in between
                angle2=((direction+1)*2*pi)/6
                x2, y2=centerx+r1*cos(angle2), centery+r1*sin(angle2)
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
        return dct_board # the key may not be used
    
    def init_pieces(self, centerx, centery, distcc, init_dir=1):
        lst_piece=[]
        for k in range(Middle_Layer+1, Middle_Layer*2+1):
            radius = distcc * k  # Distance for the current layer
            num_circles_layer = k  # Number of circles in this layer
            num_to_skip = k - Middle_Layer

            angle = (init_dir * 2 * pi) / 6  # init_dir entscheidet, so die Stücke am Anfang legen
            x = centerx + radius * cos(angle)
            y = centery + radius * sin(angle)
            # Fantacy 'next point' to calculate the coordinate of points in between
            angle1 = ((init_dir + 1) * 2 * pi) / 6
            x1 = centerx + radius * cos(angle1)
            y1 = centery + radius * sin(angle1)

            for j in range(num_to_skip, num_circles_layer - num_to_skip + 1):
                x2 = x + (x1 - x) * j / num_circles_layer
                y2 = y + (y1 - y) * j / num_circles_layer
                lst_piece.append((round(x2), round(y2)))
        return lst_piece

    def get_precise_coord(self, coord_round):
        """find the index in lst_board_round, then return the value from lst_board"""
        return self.lst_board[self.lst_board_round.index(coord_round)]

    def find_neighbors(self, coord_round):
        # returns (coord_neighbor1, coord_neighbor2)
        x,y=self.get_precise_coord(coord_round)
        lst_neighbor=[]
        for i in range(6):
            angle=i*2*pi/6
            x1=round(x+self.distcc*cos(angle))
            y1=round(y+self.distcc*sin(angle))
            x2=round(x+2*self.distcc*cos(angle))
            y2=round(y+2*self.distcc*sin(angle))
            lst_neighbor.append(((x1, y1), (x2, y2)))
        return lst_neighbor

    def find_valid_pos(self, coord_round):
        visited=set()
        connected_nodes=[]
        lst_neighbor=self.find_neighbors(coord_round)
        for coord1, _ in lst_neighbor:
            # if it is in board but not in pieces
            if coord1 in self.lst_board_round and coord1 not in self.lst_piece_round:
                connected_nodes.append(coord1)

        def dfs(coord_round):
            if coord_round in visited:
                return  # Skip if already visited
            visited.add(coord_round)  # Mark node as visited
            connected_nodes.append(coord_round)  # Add node to connected list

            lst_neighbor1 = self.find_neighbors(coord_round)
            for coord1, coord2 in lst_neighbor1:
                if (coord2 not in visited and
                    coord1 in self.lst_piece_round and
                    coord2 not in self.lst_piece_round and 
                    coord2 in self.lst_board_round):
                    dfs(coord2)
        dfs(coord_round)
        return connected_nodes

    def klicken(self, coord_round):
        coord_from=coord_to=None
        if coord_round in self.lst_piece_round:
            if self.selected is not None:
                self.valid_pos=[]
            self.valid_pos=self.find_valid_pos(coord_round)
            if len(self.valid_pos)>0:
                self.selected=coord_round
        elif self.selected and coord_round in self.valid_pos:
            # move piece, pop the old piece and insert the new piece
            index_from=self.lst_piece_round.index(self.selected)
            coord_from=self.selected
            self.lst_piece_round.pop(index_from)
            self.lst_piece.pop(index_from)
            self.lst_piece_round.append(coord_round)
            self.lst_piece.append(self.get_precise_coord(coord_round))
            coord_to=coord_round
            self.selected=None
            self.valid_pos=[]
            self.win_check()
        return self.selected, self.valid_pos, coord_from, coord_to, self.gewonnen
    
    def win_check(self):
        sorted_lst_piece=sorted(self.lst_piece_round)
        sorted_lst_ziel=sorted(self.lst_ziel_round)
        print(sorted_lst_piece)
        print(sorted_lst_ziel)
        if sorted_lst_piece==sorted_lst_ziel:
            self.gewonnen=True
# todos: reset, win check, add player, turn board, swap turns