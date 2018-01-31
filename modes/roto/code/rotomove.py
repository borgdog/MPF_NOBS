#NOBS scriptlet to control Roto Target moving

from mpf.core.mode import Mode

class RotoMove(Mode):

    def mode_start(self, **kwargs):
        self.add_mode_event_handler('extraball_hit', self.moveit)
        self.add_mode_event_handler('rototarget_hit', self.moveit)


    def moveit(self, **kwargs):
        self.log.info('rotopos start -> '+str(self.machine.get_machine_var('rotopos')))
        self.log.info('rotocount start -> '+str (self.machine.counters.rotocount.value))
        if self.machine.get_machine_var('rotodir') == 1:                               #turning counterclockwise
            if self.machine.get_machine_var('rotopos') + self.machine.counters.rotocount.value > 39:                    #will go past end?
               self.machine.set_machine_var('rotodir', -1)                                    #reverse direction
               self.machine.set_machine_var('rotopos',(self.machine.get_machine_var('rotopos') - self.machine.counters.rotocount.value)) 
            else:                                            #not past end
               self.machine.set_machine_var('rotopos',(self.machine.get_machine_var('rotopos') + self.machine.counters.rotocount.value))
        else:                                           #turning clockwise
            if self.machine.get_machine_var('rotopos') - self.machine.counters.rotocount.value < 1:                      #will go past end?
               self.machine.set_machine_var('rotodir',1)                                     #reverse direction
               self.machine.set_machine_var('rotopos',(self.machine.get_machine_var('rotopos') + self.machine.counters.rotocount.value))
            else:                                           #not past end
               self.machine.set_machine_var('rotopos',(self.machine.get_machine_var('rotopos') - self.machine.counters.rotocount.value))

        self.log.info('rotopos end -> '+str(self.machine.get_machine_var('rotopos')))

        self.delay.add(name='move_now', ms=500, callback=self.reallymove) #move the roto after 1/2 second
     
    def reallymove(self, **kwargs):
        if self.machine.get_machine_var('rotopos') > 26:
           self.machine.set_machine_var('roto',(self.machine.get_machine_var('rotopos') - 26))
        elif self.machine.get_machine_var('rotopos') > 13:
           self.machine.set_machine_var('roto',(self.machine.get_machine_var('rotopos') - 13)) 
        else:
           self.machine.set_machine_var('roto',self.machine.get_machine_var('rotopos'))

        self.log.info('rotopos end -> '+str(self.machine.get_machine_var('rotopos')))
        self.log.info('rotocount end -> '+str (self.machine.counters.rotocount.value))

        # self.machine.events.post('machine_var_roto')

        