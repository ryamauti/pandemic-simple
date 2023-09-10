import yaml
import pygame


def get_config():
    with open('config.yaml', 'r', encoding='UTF-8') as f:    
        data = yaml.load(f, Loader=yaml.FullLoader)

    # Colors
    colors = data['Colors']

    # Cities
    cities = data['Cities']    
    citypos = dict()
    for c in cities:
        # criar citypos
        citypos[c['code']] = c['board']    
        # ajustar dimensoes do board
        c['board'][0] = 60 + c['board'][0] * 1.5 
        c['board'][1] = 20 + c['board'][1] * 1.6

    # Left Buttons
    buttons = data['Buttons']

    # Middle Cards
    cards = data['Cards']

    return cities, citypos, colors, buttons, cards


def city_clicks(cities):
    clickables = list()
    for c in cities:        
        x = c['board'][0]
        y = c['board'][1]        
        saida = dict()
        saida['code'] = c['code']
        saida['rect'] = pygame.rect.Rect(x-20, y-20, 40, 40)
        clickables.append(saida)
    return clickables


def draw_lines(screen, colors, cities, citypos):
    for c in cities:
        pos = c['board']
        linecolor = colors['LINECOLOR']
        if 'connections' in c:
            conn = c['connections']
            for cn in conn:
                pos2 = citypos[cn]
                if abs(pos[0] - pos2[0]) < 600:
                    pygame.draw.line(screen, linecolor, pos, pos2, 2)
                elif pos[0] < 300:
                    pygame.draw.line(screen, linecolor, pos, (pos2[0] - 1700, pos2[1]), 2)
                elif pos[0] > 1000:
                    pygame.draw.line(screen, linecolor, pos, (pos2[0] + 1700, pos2[1]), 2)


def draw_cities(screen, colors, cities, fonte, selected_city=''):
    # draw cities       
    for c in cities:
        pos = c['board']
        color = colors[c['color']]            
        pygame.draw.circle(screen, color, pos, 20)

        if c['code'] == selected_city:
            pygame.draw.circle(screen, colors['SUCCESS'] ,pos, 20, width=3)

        if 'name' in c:
            cityname = c['name']
            text = fonte.render(cityname, True, colors['FONTCOLOR'], colors['BACKGROUND']) 
            textRect = text.get_rect()
            textRect.center = (pos[0], pos[1]+25)
            screen.blit(text, textRect)

def define_pawns(game, colors, citypos):
    pawns = dict()
    size = 16
    n = 0
    for p in game.pawns:
        pawns[p] = dict()        
        code = p.position
        pawns[p]['x'] = citypos[code][0] - 18 + 20 * (n // 2) 
        pawns[p]['y'] = citypos[code][1] - 18 + 20 * (n % 2) 
        pawns[p]['color'] = colors[p.color]
        pawns[p]['color_border'] = colors['WHITE']
        pawns[p]['color_select'] = colors['TURN_YELLOW']
        pawns[p]['rect'] = pygame.rect.Rect(pawns[p]['x'], pawns[p]['y'], size, size)
        n += 1
    return pawns        
        

def draw_pawns(screen, pawns, game):
    for p in pawns:
        pygame.draw.rect(screen, pawns[p]['color'], pawns[p]['rect'])
        pygame.draw.rect(screen, pawns[p]['color_border'], pawns[p]['rect'], width=1)   
        # TODO: desenhar as cartas em algum lugar do tabuleiro (tipo, embaixo)

def draw_centers(screen, game, colors, citypos):
    for code in citypos:
        rc = game.board[code].research_center
        if rc:            
            x = citypos[code][0]
            y = citypos[code][1]
            pygame.draw.rect(screen, colors['WHITE'], (x - 30, y-20, 8, 12))            
    pass

def draw_diseases(screen, game, colors, citypos):
    for code in citypos:
        dis = game.board[code].disease
        n = 0  # n = diseases_in_city
        for dc in game.board[code].disease: 
            for i in range(dis[dc]):                
                color = colors[dc]
                x = citypos[code][0]
                y = citypos[code][1]
                pygame.draw.rect(screen, color, (x + 22, y-20 + n*10, 8, 8))
                pygame.draw.rect(screen, colors['WHITE'], (x + 22, y-20 + n*10, 8, 8), width=1)
                n += 1
                

def selectable_buttons(these_buttons):
    for b in these_buttons:        
        b['box'] = pygame.rect.Rect(b['rectValue'])
    return these_buttons
  

def draw_buttons(screen, colors, buttons, fonte):    
    for b in buttons:
        color = colors['SECONDARY']
        pygame.draw.rect(screen, color, b['box'])
        text = fonte.render(b['name'], True, colors['FONTCOLOR'], 0x6C757DFF)
        textRect = text.get_rect()
        rv = b['rectValue']
        if 'subname' in b:
            textRect.center = (rv[0] + rv[2]/2, rv[1] + rv[3]/2 - 8) 
            screen.blit(text, textRect)
            text = fonte.render(b['subname'], True, colors['FONTCOLOR'], 0x6C757DFF)
            textRect = text.get_rect()
            textRect.center = (rv[0] + rv[2]/2, rv[1] + rv[3]/2 + 8)             
        else:
            textRect.center = (rv[0] + rv[2]/2, rv[1] + rv[3]/2)         
        screen.blit(text, textRect)


def draw_cards(screen, colors, cards, fonte):    
    for b in cards['cards']:
        color = colors['SECONDARY']
        if b['free'] == True:
            pygame.draw.rect(screen, color, b['box'], 1)
        if b['free'] == False:
            pass
        if b['code'] == 'EXTRA':
            pygame.draw.rect(screen, color, b['box'])
    
    # TODO: colocar o texto do título das cartas
    # TODO: colocar o texto das cartas
    # TODO: implementar o código visual (as cartas serão coloridas ?  terão borda colorida ?  terão um quadrado que marca a cor ? )
    # TODO: criar a regra para o local da 'carta nova' = 'EXTRA'



from engine import Game

def main():
    pygame.init()

    game = Game(num_players=4, level='Normal')
    running = True
    
    cities, citypos, colors, buttons, cards = get_config()
    FPS = 5
    DIMENSIONS = (1600, 800)
    CAPTION = "Boardgame"
    screen = pygame.display.set_mode(DIMENSIONS)
    clock = pygame.time.Clock()
    pygame.display.set_caption(CAPTION)
    fonte = pygame.font.Font('freesansbold.ttf', 10)
    fonte_maior = pygame.font.Font('freesansbold.ttf', 14)
    selected = ''
    
    pawns = define_pawns(game, colors, citypos)

    buttons = selectable_buttons(buttons)
    cards['cards'] = selectable_buttons(cards['cards'])

    while running:
        # black
        screen.fill(colors['BACKGROUND'])
        clickables = city_clicks(cities)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for r in clickables:
                        if r['rect'].collidepoint(event.pos):
                            selected = r['code']
            """
            elif event.type == pygame.MOUSEMOTION:
                if caixa.collidepoint(event.pos):
                    cor_caixa = colors['HOVER']
                else:
                    cor_caixa = colors['PRIMARY']
            """
                            

        draw_lines(screen, colors, cities, citypos)
        draw_cities(screen, colors, cities, fonte, selected)

        draw_pawns(screen, pawns, game)
        draw_centers(screen, game, colors, citypos)
        draw_diseases(screen, game, colors, citypos)

        draw_buttons(screen, colors, buttons, fonte_maior)    
        draw_cards(screen, colors, cards, fonte_maior)
            
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()


