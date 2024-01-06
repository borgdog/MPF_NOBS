#NOBS scriptlet to control Cribbage Board leds

from mpf.core.custom_code import CustomCode

class Cboard(CustomCode):

    def on_load(self):
        self.machine.events.add_handler('player_gamescore', self.lightemup)

    def lightemup(self, value, prev_value, player_num, change, **kwargs):
        self.log.info('value '+str(value)+' change '+str(change))
        if value > 120:                                                             #game won at 121 points
            self.delay.add(name='blank_lights', ms=3000, callback=self.blankem)     #blank all after 3 seconds
            for x in range(1, 121):
                self.machine.shows['score_flash'].play(show_tokens=dict(led='l_p'+str(player_num)+'_'+str(x)), loops=5)  # flash all for 3 seconds 
        else:                                                                       #not at end of game
            for x in range(value-change+1, value+1):                                # flash the amount scored
                self.machine.shows['score_flash'].play(show_tokens=dict(led='l_p'+str(player_num)+'_'+str(x)), loops=5)  # flash change for 3 seconds
                lname = 'l_p'+str(player_num)+'_'+str(x)
                self.log.info('Setting rgb '+lname + ' on')
                self.machine.lights[lname ].on(key='cb')

    def blankem(self):
        self.log.info('blanking the board')
        for x in range(1, 121):
            lname = 'l_p1_'+str(x)
            self.machine.lights[lname ].off(fade_ms=100,key='cb')
            lname = 'l_p2_'+str(x)
            self.machine.lights[lname ].off(fade_ms=100,key='cb')

