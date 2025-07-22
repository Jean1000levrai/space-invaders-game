

class Maillon:

    """maillon d'une liste chaînée"""

    def __init__(self, v=None, p=None, s=None):
        self.valeur=v
        self.precedent=p
        self.suivant=s
    
    def __str__(self): # méthode pour l'affichage
        if self.suivant==None:
            return str(self.valeur)
        else:
            return str(self.valeur) + " - " + str(self.suivant)
        
class Liste_chainee:

    def __init__(self):
        self.premier=None
        self.dernier=None
   
    def __str__(self):
        return str(self.premier)
    
    def length(self):
        """methode qui retourne la longueur de la liste chainee"""
        if self.premier == None:
            return 0
        p = self.premier
        i = 1
        while p.suivant != None:
            p = p.suivant
            i += 1
        return i

    def get(self, i):
        assert isinstance(i, int), "ERROR : parameter given should be an integer "
        assert self.premier != None, "ERROR : list is empty"
        assert i < self.length(), "ERROR : parameter given greater than list's length"

        p = self.premier
        for _ in range(i):
            p = p.suivant
        return p.valeur
    
    def modify(self, v, i=0):
        assert self.premier != None, "ERROR : list is empty"
        assert i < self.length(), "ERROR : parameter given greater than list's length"
        p = self.premier
        for _ in range(i):
            p = p.suivant
        p.valeur = v

    def find(self, x):
        p = self.premier
        while p.suivant != None:
            if x == p.valeur:
                return True
            p = p.suivant
        return False
    
    def nombre_valeur(self, x):
        p = self.premier
        n = 0
        while p.suivant != None:
            if x == p.valeur:
                n += 1
            p = p.suivant
        if x == p.valeur:
                n += 1 
        return n
    
    def insert(self, x, i=None):
        v = Maillon(x)
        n=self.length()
        p = self.premier
        if i == None: i=n
        if i == 0:  # lorsqu'on veut inserer en debut de liste
            if n != 0:  # le cas où la liste est vide
                v.suivant=self.premier
                self.premier.precedent=v
            self.premier=v
        elif i == n:
            p=self.premier
            while p.suivant != None:
                p=p.suivant
            p.suivant = v
            v.precedent = p
            self.dernier = v
        else:
            for _ in range(i-1):
                p = p.suivant
            v.suivant=p.suivant
            v.precedent = p
            p.suivant.precedent = v
            p.suivant = v

    def delete(self, i=None):
        p = self.premier
        if i==None: i = self.length()-1
        if i == 0:
            self.premier.precedent = None
            self.premier = self.premier.suivant
        else:
            for i in range(i-1):
                p=p.suivant
            if p.suivant.suivant!=None:
                p.suivant = p.suivant.suivant
                p.suivant.precedent = p
            else:
                p.suivant = None
                self.dernier=p

'''class Liste_chainee:

    """liste chaînée"""

    def __init__(self):
        self.premier=None

    def ajoute(self, v):
        """Méthode pour ajouter un élément en fin de liste"""
        m=Maillon(v)
        if self.premier==None: # si la liste est vide
            self.premier=m
        else :
            p=self.premier
            while p.suivant!=None: # on remonte la liste jusqu'au dernier élément
                p=p.suivant
            p.suivant=m

    def __str__(self): 
        """méthode pour l'affichage"""
        return str(self.premier)
    
    def longueur(self):
        """methode qui retourne la longueur de la liste chainee"""
        if self.premier == None:
            return 0
        p = self.premier
        i = 1
        while p.suivant != None:
            p = p.suivant
            i += 1
        return i
    
    def donner_valeur(self, i):
        assert isinstance(i, int), "ERROR : parameter given should be an integer "
        assert self.premier != None, "ERROR : list is empty"
        assert i < self.longueur(), "ERROR : parameter given greater than list's length"

        p = self.premier
        for _ in range(i):
            p = p.suivant
        return p.valeur
    
    def modifier_valeur(self, v, i=0):
        assert self.premier != None, "ERROR : list is empty"
        assert i < self.longueur(), "ERROR : parameter given greater than list's length"
        p = self.premier
        for _ in range(i):
            p = p.suivant
        p.valeur = v

    def trouver_valeur(self, x):
        p = self.premier
        while p.suivant != None:
            if x == p.valeur:
                return True
            p = p.suivant
        return False
    
    def nombre_valeur(self, x):
        p = self.premier
        n = 0
        while p.suivant != None:
            if x == p.valeur:
                n += 1
            p = p.suivant
        if x == p.valeur:
                n += 1 
        return n
    
    def insert_valeur2(self, x, i=0):
        v = Maillon(x)
        p = self.premier
        for _ in range(i):
            p = p.suivant
        v.suivant=p.suivant
        p.suivant=v
 
    def insert_valeur(self, x, i = 0):
        p = self.premier
        temp = x
        for _ in range(i):
            p=p.suivant
        for _ in range(self.longueur() - i):
            p.valeur, temp = temp, p.valeur
            p=p.suivant
        self.ajoute(temp)

    def delete_valeur(self, i=0):
        p = self.premier
        if i == 0:
            self.premier = self.premier.suivant
            return
        for i in range(i-1):
            p=p.suivant
        p.suivant = p.suivant.suivant'''



if __name__ == "__main__":
    lc = Liste_chainee()
    for i in range(10):
        lc.insert_valeur(i+5)
    print(lc)
    lc.delete_valeur()
    print(lc)



