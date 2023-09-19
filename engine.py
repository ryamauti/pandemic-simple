import yaml
import random


def display(text):
    print(text)


def get_config():
    with open('config.yaml', 'r', encoding='UTF-8') as f:    
        data = yaml.load(f, Loader=yaml.FullLoader)    
    rules = data['Rules']
    cities = data['Cities']    
    return cities, rules


class Game:
    def __init__(self, num_players=2, level='Hard'):
        cities, rules = get_config()
        self.cities = cities
        self.rules = rules        
        self.turn = 0   
        self.num_players = num_players
        self.level = level     
        self.pawns = list()
        self.board = dict()        
        self.centers = self.rules['Research_centers']
        self.diseases = self.rules['Diseases']
        self.round = self.rules['Round']
        self.citycards = self.rules['CityCards']
        self.infection = self.rules['Infection']
        self.outbreak = self.rules['Outbreak']
        self.epidemic = self.rules['Epidemic_card']
        self.setup_functions()        
        


    def setup_functions(self):
        self.define_pawns()
        self.define_board()
        self.create_infection_deck()
        self.create_game_deck()
        self.who_plays = random.randint(0, self.num_players-1)
        display(f'== Game starts now with {self.num_players} players ==')
        self.currentplayer = self.pawns[self.who_plays]  
        self.currentplayer.newturn()
        


    def gameover(self):
        display(f'== GAME OVER in round {self.turn} ==')
                 
        
    def define_pawns(self):
        playercount = self.num_players
        pawnrules = self.rules['Pawns']
        if playercount == 1:
            pawnrules = filter(lambda x: x['single_player_out'] == False, pawnrules)
            playercount = 3
        self.playercount = playercount        
        pawnlist = [x['class'] for x in pawnrules]        
        for i in range(playercount):
            pawn_type = random.choice(pawnlist)
            pawn_object = PawnClass(pawn_type, pawnrules, self)
            self.pawns.append(pawn_object)
            pawnlist.remove(pawn_type)

    
    def define_board(self):
        for c in self.cities:
            code = c['code']
            self.board[code] = CityData(c)


    def shuffle(self, deck):
        random.shuffle(deck)
        display(f'== Deck com {len(deck)} cartas embaralhado ==')
        return deck
    

    def create_infection_deck(self):        
        infecdeck = list(self.board)
        self.infecdeck = self.shuffle(infecdeck)
        self.infecpile = list()
        for stage in [1, 2, 3]:
            for i in range(3):
                card = self.infecdeck.pop()
                self.infecpile.append(card)
                for j in range(stage):                    
                    color = self.board[card].color
                    self.add_disease(card, color)


    def create_game_deck(self):
        gamedeck = list(self.board)
        gamedeck = self.shuffle(gamedeck)
        cards_to_each = self.citycards['Initial_draw'][self.num_players]
        for p in self.pawns:
            for i in range(cards_to_each):
                p.cards.append(gamedeck.pop())
        for sc in self.citycards['Special_Cards']:
            gamedeck.append(sc['Code'])
        gamedeck = self.shuffle(gamedeck)
        epidemic_cards_num = self.epidemic['Type'][self.level]
        epidemic_card = self.epidemic['Code']
        deck_chunk_size = len(gamedeck) // epidemic_cards_num
        d_start = 0
        d_limit = deck_chunk_size
        gamedeck_final = list()
        for k in range(epidemic_cards_num):
            if k == epidemic_cards_num - 1:
                d_limit = len(gamedeck)
            smalldeck = gamedeck[d_start : d_limit]
            smalldeck.append(epidemic_card)
            smalldeck = self.shuffle(smalldeck)
            gamedeck_final += smalldeck
            d_start = d_limit
            d_limit += deck_chunk_size
        self.gamedeck = gamedeck_final
        
        
    def add_disease(self, code, color):
        has_outbreak = self.board[code].add_disease(color)
        if has_outbreak:
            self.handle_outbreak(code, color)


    def handle_outbreak(self, code, color):
        self.outbreak['Status'] += 1
        if self.outbreak['Status'] >= self.outbreak['Limit']:
            self.gameover()
        for c in self.board[code].connections:
            if self.board[c].had_outbreak == False:
                self.add_disease(c, color)


    def next_turn(self):
        for c in self.board:
            self.board[c].had_outbreak = False
        self.who_plays = self.who_plays + 1
        self.who_plays = self.who_plays % self.num_players
        self.currentplayer = self.pawns[self.who_plays]
        

    
    def do_round(self):
        for j in self.round['Actions']['Moves']:
            self.perform_action()        
        for j in self.citycards['Rate']:
            self.handle_city_cards()        
        for j in self.infection['Rate']:
            self.handle_infection()
        self.next_turn()


    def perform_action(self):
        pass

    def handle_city_cards(self):
        pass

    def handle_infection(self):
        pass
       

class CityData:
    def __init__(self, cityinfo):
        self.code = cityinfo['code']
        self.name = cityinfo['name']
        self.color = cityinfo['color'] 
        self.connections = cityinfo['connections']
        self.disease = dict()
        self.disease['YELLOW'] = 0
        self.disease['BLACK'] = 0
        self.disease['BLUE'] = 0
        self.disease['RED'] = 0
        self.had_outbreak = False
        if self.code == 'AT':
            self.research_center = True
        else:
            self.research_center = False


    def is_connected(self, destination):
        if destination in self.connections:
            return True
        else:
            return False
        
    
    def add_disease(self, color):        
        if self.disease[color] < 3:
            self.disease[color] += 1  
            return False          
        else:
            display(f'== Outbreak in {self.name} ==')
            self.had_outbreak = True
            return True
        
    

class PawnClass:
    def __init__(self, pawntype, pawnrules, this_game):
        for p in pawnrules:
            if p['class'] == pawntype:
                self.color = p['color'] 
                self.name = p['name']        
        self.gamedata = this_game        
        self.type = pawntype
        self.cards = list()
        self.position = 'AT'
        self.moves = 0
        self.active = False


    def newturn(self):
        display(f'==  {self.name} {self.color} turn starts now ==')
        self.moves = 4
        self.active = True

    def endturn(self):        
        self.active = False


    def citydata(self):
        return self.gamedata.board[self.position]


    def treat_disease(self):
        cd = self.citydata()
        colors = [k for k in cd.disease if cd.disease[k] > 0]
        if len(colors) == 0:
            display(f'== não há doenças na cidade ==')
            return False
        elif len(colors) >= 2:
            # TODO: tratar caso de mais que uma doença na cidade
            display(f'== Há mais que uma doença na cidade. Escolha a doença a curar ==')
            return False
        else:
            color = colors[0]
            cd.disease[color] -= 1
            display(f'== Doente curado ==')
            return True
            # TODO: tratar casos de doença curada
            # TODO: tratar casos da profissão Médico


    def build_center(self):
        cd = self.citydata()
        if cd.research_center == True:
            display(f'== Já há um centro de pesquisa na cidade ==')
            return False
        else:
            # TODO: checar se há centros de cidade disponíveis
            # TODO: se não houver, escolher qual cidade terá seu centro destruído
            cd.research_center = True
            display(f'== Centro de pesquisa construído ==')
            # TODO: reduzir quantidade de centros disponíveis
            return True


    def share_cards(self):
        pass

    def discover_cure(self):
        pass

    def go_to_neighbor(self, destination):
        cd = self.citydata()
        if cd.is_connected(destination):
            self.position = destination
            display(f'== Player {self.type} está agora em {self.position} ==')
            return True
        else:
            display(f'== Não há ligação entre as cidades {self.position} e {destination} ==')
            return False
        

    def go_to_center(self, destination):
        cd = self.citydata()
        cd_dest = self.gamedata.board[destination]   
        if cd.research_center == True and cd_dest.research_center == True:
            self.position = destination
            display(f'== Player {self.type} está agora em {self.position} ==')   
            return True     
        else:
            display(f'== Não há ligação entre as cidades {self.position} e {destination} ==')
            return False        


    def go_to_card(self, selected_card, destination):   
        if selected_card == destination:
            self.position = destination
            self.cards.remove(selected_card)
            display(f'== Player {self.type} está agora em {self.position} ==')   
            return True     
        else:
            display(f'== Não há ligação entre as cidades {self.position} e {destination} ==')
            return False
        

    def go_from_card(self, selected_card, destination):
        if selected_card == self.position:
            self.position = destination
            self.cards.remove(selected_card)
            display(f'== Player {self.type} está agora em {self.position} ==')   
            return True     
        else:
            display(f'== Não há ligação entre as cidades {self.position} e {destination} ==')
            return False



if __name__ == '__main__':
    game = Game(2)
    
    for p in game.pawns:
        print(p.type, p.cards)