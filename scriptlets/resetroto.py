#NOBS scriptlet to reset RotoTarget at machine power up

from mpf.core.mode import Mode

class RotoReset(Mode):

    def mode_start(self, **kwargs):
        self.add_mode_event_handler('machine_reset_phase3', self.resetit)
    
    def resetit(self, **kwargs):
        self.log.info('roto reset -> '+str(self.machine.get_machine_var('roto')))
        self.machine.servos.servo_roto.go_to_position('roto_'(self.machine.get_machine_var(roto)))
