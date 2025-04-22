import tkinter as tk
from PIL import Image, ImageTk
import random
import liste_chainee_double as lc
import math
import open_img_tk as open
# import pygame

class Menu:
    """
    classe utilisé pour créer le menu
    """
    def __init__(self) -> None:
        # self.menu_bg_img = None
        pass

    def launch_game(self):
        # ------enlève le menu------
        button.place_forget()
        # ------lance le jeu------
        canvas.create_image(width/2,height/2,image = bg_img)
        player.instantiate(player_img)
        list_missile.continuous_forward()
        list_missile.delete()
        list_monster.continuous_fall()
        list_missile.kaboom_trigger()
        list_monster.collide()
        list_monster.spawn_monster_continuous()
        logic.logic()
        logic.add_score()

    def launch_menu(self):
        canvas.create_image(width/2,height/2,image = menu_img)
        button.place(x=width/2-100, y=height/2-200)

class Player:
    """
    classe utilisé pour représenter un joueur

    -----attributs-----
    -player_img : pour générer l'image du joueur
    -x et y : les coordonnées en 2D du joueur
    -speed : la vitesse à laquelle le joueur pourra se déplacer
    -is_alive : booléen si vrai, le joueur est en vie, si faux, le joueur est mort
    -key_pressed : booléen si vrai, une touche est appuyée, si faux, aucune touche n'est appuyée
    utile lorsqu'on veut éviter le spam d'une attaque
    -atk_speed : la vitesse à laquelle le joueur pourra tirer
    -hp : représente les points de vie du joueur

    -----methodes----
    -instantiate : instantie le joueur
    -player_mvt : permet les mouvements du joueur et de tirer
    -damage : permet au joueur de prendre des dégats et perd un coeur
    -player_death : méthode pour faire mourir le joueur quand il a perdu et affiche game over
    """
    def __init__(self, speed = 10, atk_speed=1000, hp = 3) -> None:
        """
        constructeur de la classe
        speed, atk_speed et hp sont les 3 paramètres int pour les 2 attributs du même nom
        """
        super().__init__()
        self.player_img = None
        self.x = 500
        self.y = 500
        self.speed = speed
        self.is_alive = False
        self.key_pressed = False
        self.atk_speed = atk_speed
        self.hp = hp
        self.hearts = []

    def instantiate(self, img, x=500, y=500):
        """instantie le joueur"""
        canvas.delete(self.player_img)
        self.is_alive = True
        self.player_img = canvas.create_image(x,y, image = img)
        # crée les coeurs du joueur représentant sa barre de vie
        for i in range(25, self.hp*75, 75): # boucle autant de fois que le joueur a de point de vie(x75 car on a un pas de 75 pour l'espacement des coeurs)
        # le 1er coeur apparaît à x = 25 et le suivant 75 sur la droite depuis ce point
            self.hearts.append(canvas.create_rectangle((i, 25),(i+50,75), fill="red", outline="#787878"))

    def player_mvt(self, event):
        """permet les mouvements du joueur et de tirer"""
        Key = event.keysym  # récupere la touche en mémoire pour etre utilisé
        if self.is_alive:   # regarde si le joueur est encore en vie
            # -----------mouvement---------------
            if Key in ['q','Left']:
                self.x -= self.speed
            if Key in ['d','Right']:
                self.x += self.speed
            if Key in ['z','Up']:
                self.y -= self.speed
            if Key in ['s','Down']:
                self.y += self.speed
            canvas.coords(self.player_img, self.x, self.y)
            # ------bordures-------
            if self.x < 0:
                self.x = width - 5
            if self.x > width:
                self.x = 5
            if self.y > height:
                self.y -= self.speed
            if self.y < height/1.5:
                 self.y += self.speed
            #------- tir ------
            if Key in ['space', 'Return']:
                list_missile.launch_missile()

    def damage(self):
        """permet au joueur de prendre des dégats et perd un coeur"""
        if self.hp > 0: # pour arrêter de boucler quand il est mort
            # damage_sfx.set_volume(0.5)
            # damage_sfx.play()
            self.hp -= 1
            canvas.itemconfig(player.hearts[self.hp], fill='#787878')

    def player_death(self):
        """méthode pour faire mourir le joueur quand il a perdu et affiche game over"""
        player.is_alive = False
        canvas.create_text(width//2, height//2, text="GAME OVER", font=('bold', 100), fill="red")
        # game_over_sfx.set_volume(0.5)
        # game_over_sfx.play()

class Logic(Player):
    """
    classe qui s'occupe de gérer la logique du jeu en cour

    -----attributs-----
    -score --> le score du joueur, s'incrémente à l'élimination d'un monstre
    -labelled_score --> l'affichage du score

    -----methodes----
    -add_score --> affiche le score
    -logic --> méthode principale et récursive qui gére le jeu
    """
    def __init__(self, dif) -> None:
        self.score = 0
        self.labelled_score = canvas.create_text((width-20, 25), text='0', fill="#0c9400", font=" Arial 30 bold")
        self.dificulty = dif

    def add_score(self):
        """affiche le score"""
        self.labelled_score = canvas.create_text((width-20, 25), text='0', fill="#0c9400", font=" Arial 30 bold")

    def logic(self):
        """méthode principale et récursive qui gére le jeu"""
        global monster_info
        if player.hp <= 0:  
            # mort du joueur si ses points de vie sont inférieur à 0
            player.player_death()
        # petit reminder : TOUT SE FAIT LA' QUAND LE JOUEUR EST EN VIE
        else:   
            canvas.itemconfigure(self.labelled_score, text=str(self.score)) # met à jour le score
            for i in range(1,len(str(self.score))):
                # bouge le score un peu à droite à chaque fois qu'il y a un nombre en plus pour ne pas qu'il soit caché
                canvas.coords(self.labelled_score, width - 20*i ,25)
            monster_info["speed_monster"] = self.dificulty  # les monstres accélèrent à mesure de la difficulté
            canvas.after(100, self.logic)   # appel récursif de la méthode

class Missile(Player):
    """
    classe utilisé pour représenter un missile sans pouvoir le gérer

    -----attributs-----
    -player : le joueur qui tirera le missile
    -x et y : les coordonnées du missile
    -missile_img : l'image du joueur
    -exploding : booléen donnant l'état du missile, en train d'exploser ou non
    -explosion : l'image de l'explosion

    -----méthodes-----
    -forward : fait avancer le missile une fois
    -kaboom : méthode donnant la possibilité au missile d'exploser
    """
    def __init__(self, player) -> None:
        """
        constructeur de la classe
        player est le seul paramètre pour référencer le joueur qui tirera le missile
        """
        super().__init__()
        self.player = player
        self.x= player.x
        self.y=player.y
        self.exploding = False
        self.explosion = None
        self.missile_img = canvas.create_image( player.x, player.y , image = missile_img)

    def forward(self):
        """fait avancer le missile une fois"""
        self.y -= 3
        canvas.coords(self.missile_img, self.x, self.y)

    def kaboom(self, i):
        """méthode donnant la possibilité au missile d'exploser"""
        if self.exploding == False:
            # explosion_sfx.set_volume(0.5)
            # explosion_sfx.play()
            # commence l'explosion en instantiant la 1ere image et explosion = True
            self.explosion = canvas.create_image(self.x, self.y, image=explosion_img[0][0])
            self.exploding = True
        elif i < 30:
            # change l'image toute les 0,02 sec jusqu'à la dernière
            canvas.itemconfig(self.explosion, image=explosion_img[0][i])
            canvas.after(20, lambda: self.kaboom(i+1))
        elif i >=30:
            # lorque l'explosion est terminé, exploding = False et enlève l'explosion
            self.exploding = False
            canvas.delete(self.explosion)

class Liste_missile(Missile):
    """
    classe utilisé pour gérer tous les missiles

    -----attributs-----
    -player : référence le joueur
    -list_mis : une liste_chaînée contenant tous les missiles

    -----méthodes-----
    -launch_missile : méthode où est instantié un missile de la classe Missile
    -continuous_forward : méthode qui fait avancer continuellement les missiles
    -delete : éfface le missile
    -kaboom_trigger : crée une explosion lors d'un impact avec un ennemi
    """
    def __init__(self, player1) -> None:
        """
        constructeur de la classe
        un paramètre pour référencer le joueur
        """
        self.player = player1
        self.list_mis = lc.Liste_chainee()

    def launch_missile(self):
        """ méthode où est instantié un missile de la classe Missile"""
        m = Missile(self.player)
        self.list_mis.insert(m,0)

    def continuous_forward(self):
        """
        méthode qui fait avancer continuellement les missiles
        utilise la méthode forward du missile
        """
        for i in range(self.list_mis.length()): # boucle sur tous les missiles
            missile = self.list_mis.get(i)      # récupère le missile d'indice i avec une liste chaînée
            missile.forward()
        canvas.after(10, self.continuous_forward)   # appel récursif

    def delete(self):
        """éfface le missile"""
        for i in range(self.list_mis.length()): # boucle sur tous les missiles
            missile1 = self.list_mis.get(i)     # récupère le missile d'indice i avec une liste chaînée
            if missile1.y < -100:               # éfface le missile s'il sort de la toile
                canvas.delete(missile1.missile_img)
                self.list_mis.delete(i)
            break   # évite de boucler sur un missile déjà détruit et résoudre à une erreur
        canvas.after(100, self.delete)    # appel récursif

    def kaboom_trigger(self):
        """crée une explosion lors d'un impact avec un ennemi"""
        for i in range(self.list_mis.length()):
            # boucle sur tous les missiles présents
            for j in range(list_monster.list_monster.length()):
                # et tous les monstres présents
                # récupère avec une liste chaînée le monstre et le missile
                monster = list_monster.list_monster.get(j)
                missile = self.list_mis.get(i)
                if math.sqrt((monster.xm - missile.x)**2+(monster.ym-missile.y)**2) < 30:
                    # s'ils se touchent, le missile explose
                    missile.kaboom(0)
        canvas.after(10, self.kaboom_trigger)  # appel récursif

class Monster:
    """
    Classe représentant un monstre

    -----attributs-----
    -speedm : la vitesse à la laquelle le monstre se déplace
    -alive : booléen, true --> en vie/false --> mort
    -xm et ym : ses coordonnées, xm choisi au hasard
    -img : son image

     -----methodes----
    -fall : permet au monstre de descendre une fois
    """
    def __init__(self, speedm = 5, x = random.randint(0, 1000), y = -200) -> None:
        self.speedm = speedm
        self.alive = True
        self.xm = x
        self.ym = y
        self.img = canvas.create_image(self.xm, self.ym, image = monster_img)

    def fall(self):
        """permet au monstre de descendre une fois"""
        self.ym += self.speedm
        canvas.coords(self.img, self.xm, self.ym)

class List_monster(Liste_missile, Missile, Monster):
    """
    Classe qui gère tous les monstres

    -----attributs-----
    -les attributs des classes Liste_missile, Missile et Monster avec player1=player
    -list_monster : une chaînée contenant les monstres

    -----methodes----
    - spawn_monster_continuous : méthode initialisé au début de la partie et récursive .
        elle fait apparaître les monstres à un intervalle de temps
    - spawn_monster : méthode faisant apparaître un monstre à des coordonnées précises
    -continuous_fall : méthode récursive qui fait tomber les monstres en continu
    -collide : vérifie les collision et réagit en conséquence
    """
    def __init__(self, monster_dif = 5) -> None:
        super().__init__(player1=player)
        self.list_monster = lc.Liste_chainee()
        self.monster_diff = monster_dif  # plus c'est petit, plus c'est dur

    def spawn_monster_continuous(self):
        """méthode initialisé au début de la partie et récursive.
        elle fait apparaître les monstres à un intervalle de temps
        """
        m = Monster(speedm = monster_info["speed_monster"], x = random.randint(0, width), y = -200)   
        self.list_monster.insert(m,0)
        canvas.after(2000, self.spawn_monster_continuous)  # appel récursif

    def spawn_monster(self, coords):
        """méthode faisant apparaître un monstre à des coordonnées précises
        paramètre coords pour les coordonnées initiale du monstre"""
        m = Monster(coords[0], coords[1])
        self.list_monster.insert(m,0)

    def continuous_fall(self):
        """méthode récursive qui fait tomber les monstres en continu"""
        for i in range(self.list_monster.length()):
        # boucle sur tous les monstres
            monster = self.list_monster.get(i)
            monster.fall()  # les fait tomber
        canvas.after(50, self.continuous_fall)  # récursif tous les 50ms

    def collide(self):
        """
        vérifie les collision et réagit en conséquence
        monstre détruit si il sort de la scène et fait perdre une vie au joueur
        monstre détruit si il s'est fait tiré dessus et incrémente le score
        """
        monsters_to_delete = [] # crée une liste qui donnera quels monstres seront à effacer       
        # boucle sur tous les monstres
        for j in range(self.list_monster.length()):
            monster = self.list_monster.get(j)            
            # vérifie si le monstre sort de la scène
            if monster.ym > 640 and monster.alive:
                canvas.delete(monster.img)
                monsters_to_delete.append(j)
                monster.alive = False
                player.damage()
            # collision avec les missiles
            for i in range(list_missile.list_mis.length()):
                missile = list_missile.list_mis.get(i)                
                # détecte une collision si le missile est proche du monstre
                if math.sqrt((monster.xm - missile.x)**2 + (monster.ym - missile.y)**2) < 30 and monster.alive:
                    missile.kaboom(0)  # crée l'explosion
                    canvas.delete(monster.img)
                    monsters_to_delete.append(j)
                    missile.y = -1000
                    monster.alive = False  # rend le monstre mort
                    logic.score += 1
                    if logic.score % self.monster_diff == 0 and logic.score > 0:
                        logic.dificulty += 1    # incrémente la difficulté
                    break  # évite que la boucle continue sur un monstre déjà mort      
        # éfface les monstres morts
        for i in sorted(monsters_to_delete, reverse=True):
        # monstres détruits en 1er avec l'indice le plus haut, évite un problème d'indice
            self.list_monster.delete(i)
        canvas.after(10, self.collide) # méthode récursive tous les 10ms

class Monster_hord:
    def __init__(self) -> None:
        self.stage = 0
        self.direction = 0  # 0 = gauche; 1 = droite
    
    def hord_spawn(self):
        pass

if __name__ == "__main__":
    # ---------------------------fenetre---------------------------
    window = tk.Tk()
    # pygame.init()
    width=1000
    height=600
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.pack()

    # ---------------------------variables---------------------------

    monster_info = {"speed_monster" : 5}
    dif_monster = 5
    dif_logic = 5
    
    # ---------------------------objects instantiate---------------------------
    player = Player()
    logic = Logic(dif=dif_logic)
    list_missile = Liste_missile(player1=player)
    list_monster = List_monster(monster_dif=dif_monster)

    window.bind('<Key>', player.player_mvt)

    # ---------------------------ouverture image---------------------------
    temp_menu_img = Image.open('img/menu_bg.jpg')
    temp_menu_img=temp_menu_img.resize((1200,600))
    menu_img = ImageTk.PhotoImage(temp_menu_img)
    play2 = Image.open("img/play.png")
    play1 = ImageTk.PhotoImage(play2)

    temp_missile_img = Image.open('img/missile.png')
    temp_missile_img=temp_missile_img.resize((20,50))
    missile_img = ImageTk.PhotoImage(temp_missile_img)

    temp_player_img = Image.open('img/vaisseau.png')
    temp_player_img=temp_player_img.resize((160,80))
    player_img = ImageTk.PhotoImage(temp_player_img)

    temp_bg_img = Image.open('img/fond2.png')
    bg_img = ImageTk.PhotoImage(temp_bg_img)

    temp_monster_img = Image.open('img/adversaire1.png')
    temp_monster_img=temp_monster_img.resize((50,50))
    monster_img = ImageTk.PhotoImage(temp_monster_img)

    explosion_img = [[]]
    explosion_img[0].extend(open.charger_image(master=window, taille=(150,150), chemin="img/explosion/Effect_Explosion_1_0",nb_image=30,index_debut=0))

    # explosion_sfx = pygame.mixer.Sound("sound/explosion.wav")
    # game_over_sfx = pygame.mixer.Sound("sound/game_over.mp3")
    # damage_sfx = pygame.mixer.Sound("sound/damage.mp3")
    
    # ---------------------------instantiate---------------------------
    
    menu = Menu()
    button = tk.Button(window, image=play1, text="TEST", command=menu.launch_game)
    menu.launch_menu()

    window.mainloop()

# wr = 52 par axel b.