class City():

    def __init__(self, player_number, max_health, damage, xcoord, ycoord):
        self.player_number = player_number
        self.max_health = max_health
        self.damage = damage
        self.current_health = max_health #The city is brand new when initialised.
        self.xcoord = xcoord
        self.ycoord = ycoord

    def on_destruction(self):
        pass
        #TODO : sort this out.

    def on_attack(self):
        pass
        #TODO : sort this out.

    def on_click(self, player_number):
        pass
        '''
        TODO : If the player that clicks it is the player that owns the city,
        allow them to access the information and build queue etc. Otherwise just
        display the name of the city.
        '''
