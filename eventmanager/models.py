from django.db import models
from string import upper
from django.contrib.auth.models import User

EVENT_CHOICES = (
    ('LU', 'Lumos'),
    ('OV', 'Overhaul'),
    ('AB', 'Abyss'),
    ('SE', 'Seeker'),
    ('AC', 'ACROSS'),
)

def rbtx_event_code_to_event_name(code):
    """ Return the event name corresponding to the event code code. """
    code = upper(code)
    for x in EVENT_CHOICES:
        if x [0] == code:
            return x [1]

def rbtx_is_valid_event_code(code):
    """ Check if code corresponds to a valid event code. """
    code = upper(code)
    for x in EVENT_CHOICES:
        if x [0] == code:
            return True
    return False

#class Import(models.Model):
 #   ref_num = models.IntegerField(blank = True, verbose_name='Reference Number:')

class Team(models.Model):
    """ Represents one team, to take part in one event. """

    team_name = models.CharField(max_length = 255, verbose_name = 'Team Name')
    author = models.ForeignKey(User, editable = False)

    # Event specific ID
    team_id = models.IntegerField(blank = True, verbose_name = 'Team ID', editable = False, default = 0)
    event = models.CharField(max_length = 2, choices = EVENT_CHOICES, verbose_name = 'Event')

    college = models.CharField(max_length = 255, verbose_name = 'College')
    number_a = models.CharField(max_length = 15, verbose_name = 'Primary Contact Number')
    number_b = models.CharField(max_length = 15, blank = True, verbose_name = 'Secondary Contact Number')
    email = models.EmailField(verbose_name = 'Contact Email', blank = True)

    participant_1 = models.CharField(max_length = 255, verbose_name = 'First Participant')
    participant_2 = models.CharField(max_length = 255, blank = True, verbose_name = 'Second Participant')
    participant_3 = models.CharField(max_length = 255, blank = True, verbose_name = 'Third Participant')
    participant_4 = models.CharField(max_length = 255, blank = True, verbose_name = 'Fourth Participant')

    registered_on = models.DateTimeField(auto_now_add = True)

    comments = models.TextField(blank = True)

    promoted_to = models.IntegerField(blank = True, editable = False, default = 1)
    best_mechanical_design = models.BooleanField(default = False, editable = False)
    best_algorithm_design = models.BooleanField(default = False, editable = False)

    def __unicode__(self):
        return self.get_decorated_team_id() + ' (' + self.team_name + ')'

    def assign_team_id(self):
        """ Assign a event-unique team ID to the object """
        objects = Team.objects.filter(event = self.event)
        if len(objects) == 0:
            self.team_id = 1
        else:
            self.team_id = objects.aggregate(models.Max('team_id')) ['team_id__max'] + 1
        self.save ()
        return self.get_decorated_team_id()

    def get_decorated_team_id(self):
        """ Get the decorated team ID, of the form RA123 """
        return self.event + str(self.team_id)

class _EventBase(models.Model):
    """ An abstract model describing the features common to all the event models. """

    author = models.ForeignKey(User, editable = False)
    comments = models.TextField(blank = True)
    edited_score = models.IntegerField(verbose_name = 'Score')
    conducted_on = models.DateTimeField(auto_now_add = True)
    best_algorithm_design = models.BooleanField(default = False)
    best_mechanical_design = models.BooleanField(default = False)

    class Meta:
        abstract = True

class LumosFirstRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = {'event__exact': 'LU', 'promoted_to__exact' : 1 })
    
    stationaryLight_deactivated = models.IntegerField(verbose_name = 'Number of Stationary Light Sources Deactivated:')
    movingLight_deactivated = models.IntegerField(verbose_name = 'Number of Moving Light Sources Deactivated:')
    incorrect_source=models.IntegerField(verbose_name='Number of times bot hits deactivated source:')
    num_restarts = models.IntegerField(verbose_name = 'Number of Restarts:')
    num_timeouts = models.IntegerField(verbose_name = 'Number of Time-Outs:')
    max_time_to_be_allotted = models.IntegerField(verbose_name = 'Alotted Run-Time(in s):')
    time_taken = models.IntegerField()

    def calculate_score(self):
        score = 0 
        score = score + 80 * self.stationaryLight_deactivated
        score = score + 120 * self.movingLight_deactivated
        score = score - 75 * self.incorrect_source 
        score = score - 50 * self.num_restarts
        score = score - 20 * self.num_timeouts
	score = score + ((self.max_time_to_be_allotted-self.time_taken)/2)
        return score

    def __unicode__(self):
        return 'First Lumos round for team \'' + str(self.team) + '\''

class LumosSecondRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = {'event__exact': 'LU', 'promoted_to__exact' : 2 })

    checkpoints_detected = models.IntegerField(verbose_name = 'Number of checkpoints detected')
    stationaryLight_deactivated = models.IntegerField(verbose_name = 'Number of Stationary Light Sources Deactivated:')
    movingLight_deactivated = models.IntegerField(verbose_name = 'Number of Moving Light Sources Deactivated:')
    incorrect_source=models.IntegerField(verbose_name='Number of times bot hits deactivated source:')
    num_restarts = models.IntegerField(verbose_name = 'Number of Restarts:')
    num_timeouts = models.IntegerField(verbose_name = 'Number of Time-Outs:')
    max_time_to_be_allotted = models.IntegerField(verbose_name = 'Alotted Run-Time(in s)')
    time_taken = models.IntegerField()

    def calculate_score(self):
        score = 0 
        score = score + 80 * self.stationaryLight_deactivated
        score = score + 120 * self.movingLight_deactivated
        score = score - 75 * self.incorrect_source 
        score = score - 50 * self.num_restarts
        score = score - 20 * self.num_timeouts
	score = score + ((max_time_to_be_allotted-time_taken)/2)
        return score

    def __unicode__(self):
        return 'Second Lumos round for team \'' + str(self.team) + '\''

class LumosThirdRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = {'event__exact': 'LU', 'promoted_to__exact' : 3 })

    stationaryLight_deactivated = models.IntegerField(verbose_name = 'Number of Stationary Light Sources Deactivated:')
    movingLight_deactivated = models.IntegerField(verbose_name = 'Number of Moving Light Sources Deactivated:')
    incorrect_source=models.IntegerField(verbose_name='Number of times bot hits deactivated source:')
    num_restarts = models.IntegerField(verbose_name = 'Number of Restarts:')
    num_timeouts = models.IntegerField(verbose_name = 'Number of Time-Outs:')
    max_time_to_be_allotted = models.IntegerField(verbose_name = 'Alotted Run-Time(in s)')
    time_taken = models.IntegerField()

    def calculate_score(self):
        score = 0 
        score = score + 80 * self.stationaryLight_deactivated
        score = score + 120 * self.movingLight_deactivated
        score = score - 75 * self.incorrect_source 
        score = score - 50 * self.num_restarts
        score = score - 20 * self.num_timeouts
	score = score + ((max_time_to_be_allotted-time_taken)/2)
        return score

class OverhaulFirstRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'LU', 'promoted_to__exact' : 1 })
    
    black_cylinders = models.IntegerField(verbose_name = 'Number of black cylinders retreived')
    white_cylinders = models.IntegerField(verbose_name = 'Number of white cylinders retreived')
    candles_put_out = models.IntegerField(verbose_name = 'Number of candles put out')
    cylinders_in_safe_zone = models.IntegerField(verbose_name = 'Number of cylinders in safe zone')

    fires_touched = models.IntegerField(verbose_name = 'Number of times the robot touches fire')
    fires_dropped = models.IntegerField(verbose_name = 'Number of fires dropped')
    cylinder_in_contact_with_candle = models.IntegerField(verbose_name = 'Number of times a cylinder comes in contact with a candle')
    time_taken = models.IntegerField(verbose_name = 'Time taken')
    timeouts = models.IntegerField(verbose_name = 'Number of time-outs taken')
    restarts = models.IntegerField(verbose_name = 'Number of restarts taken')

    def calculate_score(self):
        total = 0
        total = total + 150 * self.black_cylinders
        total = total + 100 * self.white_cylinders
        total = total + 250 * self.candles_put_out
        total = total + 50 * self.cylinders_in_safe_zone
        total = total - 50 * self.fires_touched
        total = total - 100 * self.fires_dropped
        total = total - 60 * self.cylinder_in_contact_with_candle
        total = total - 50 * self.timeouts
        total = total - 100 * self.restarts 
        total = total - (self.time_taken / 3)
        return total

    def __unicode__(self):
        return 'First Overhaul round for team \'' + str(self.team) + '\''

class OverhaulSecondRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'LU', 'promoted_to__exact' : 2 })
    
    black_cylinders = models.IntegerField(verbose_name = 'Number of black cylinders retreived')
    white_cylinders = models.IntegerField(verbose_name = 'Number of white cylinders retreived')
    candles_put_out = models.IntegerField(verbose_name = 'Number of candles put out')
    cylinders_in_safe_zone = models.IntegerField(verbose_name = 'Number of cylinders in safe zone')

    fires_touched = models.IntegerField(verbose_name = 'Number of times the robot touches fire')
    fires_dropped = models.IntegerField(verbose_name = 'Number of fires dropped')
    cylinder_in_contact_with_candle = models.IntegerField(verbose_name = 'Number of times a cylinder comes in contact with a candle')
    #ramp_manually_traversed = models.IntegerField(verbose_name = 'Number of times the bot had to be manually placed atop the ramp')
    time_taken = models.IntegerField(verbose_name = 'Time taken')
    timeouts = models.IntegerField(verbose_name = 'Number of time-outs taken')
    restarts = models.IntegerField(verbose_name = 'Number of restarts taken')

    def calculate_score(self):
        total = 0
        total = total + 150 * self.black_cylinders
        total = total + 100 * self.white_cylinders
        total = total + 250 * self.candles_put_out
        total = total + 50 * self.cylinders_in_safe_zone
        total = total - 50 * self.fires_touched
        total = total - 100 * self.fires_dropped
        total = total - 60 * self.cylinder_in_contact_with_candle
     #total = total - 100 * self.ramp_manually_traversed
        total = total - 50 * self.timeouts
        total = total - 100 * self.restarts 
        total = total - ((self.time_taken) / 3)
        return total

    def __unicode__(self):
        return 'Second Overhaul round for team \'' + str(self.team) + '\''

class OverhaulThirdRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'LU', 'promoted_to__exact' : 3 })
    
    black_cylinders = models.IntegerField(verbose_name = 'Number of black cylinders retreived')
    white_cylinders = models.IntegerField(verbose_name = 'Number of white cylinders retreived')
    candles_put_out = models.IntegerField(verbose_name = 'Number of candles put out')
    cylinders_in_safe_zone = models.IntegerField(verbose_name = 'Number of cylinders in safe zone')

    fires_touched = models.IntegerField(verbose_name = 'Number of times the robot touches fire')
    fires_dropped = models.IntegerField(verbose_name = 'Number of fires dropped')
    cylinder_in_contact_with_candle = models.IntegerField(verbose_name = 'Number of times a cylinder comes in contact with a candle')
    #ramp_manually_traversed = models.IntegerField(verbose_name = 'Number of times the bot had to be manually placed atop the ramp')
    time_taken = models.IntegerField(verbose_name = 'Time taken')
    timeouts = models.IntegerField(verbose_name = 'Number of time-outs taken')
    restarts = models.IntegerField(verbose_name = 'Number of restarts taken')

    def calculate_score(self):
        total = 0
        total = total + 150 * self.black_cylinders
        total = total + 100 * self.white_cylinders
        total = total + 250 * self.candles_put_out
        total = total + 50 * self.cylinders_in_safe_zone
        total = total - 50 * self.fires_touched
        total = total - 100 * self.fires_dropped
        total = total - 60 * self.cylinder_in_contact_with_candle
     #total = total - 100 * self.ramp_manually_traversed
        total = total - 50 * self.timeouts
        total = total - 100 * self.restarts 
        total = total - (self.time_taken / 3)
        return total

    def __unicode__(self):
        return 'Third Overhaul round for team \'' + str(self.team) + '\''

class AbyssFirstRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'AB', 'promoted_to__exact' : 1 })

    cylinder1_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, red-zone')
    cylinder2_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, red zone')
    cylinder3_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, red zone')
    cylinder4_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, red zone')
    
    cylinder1_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, yellow zone')
    cylinder2_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, yellow zone')
    cylinder3_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, yellow zone')
    cylinder4_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, yellow zone')
    
    cylinder1_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, green zone')
    cylinder2_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, green zone')
    cylinder3_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, green zone')
    cylinder4_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, green zone')
    
    time_taken = models.IntegerField(verbose_name = 'Time taken')

    self_clasping_mechanism_bonus = models.IntegerField(default = False, verbose_name = 'Self clasping mechanism bonus? 1 for YES and 0 for NO')
    one_bounce_out_partial_score = models.IntegerField(verbose_name = 'Number of times the ball bounced outside the drop zone after bouncing off a cylinder wall')  
    outside_penalty = models.IntegerField(verbose_name = 'Number of balls that fell outside')
    bot_falling_off_the_zipline_penalty = models.IntegerField(verbose_name = 'Number of times the bot fell off the zip-line')
    refill_penalty = models.IntegerField(verbose_name = 'Number of refills')
    restarts = models.IntegerField(verbose_name = 'Number of restarts')
    timeouts = models.IntegerField(verbose_name = 'Number of time-outs')
        

    def calculate_score(self):
        total = 180 - self.time_taken
        total = total + 45 * self.cylinder1_red_zone_15 + 30 * self.cylinder1_yellow_zone_10 + 15 * self.cylinder1_green_zone_5
        total = total + 60 * self.cylinder2_red_zone_15 + 40 * self.cylinder2_yellow_zone_10 + 20 * self.cylinder2_green_zone_5
        total = total + 90 * self.cylinder3_red_zone_15 + 60 * self.cylinder3_yellow_zone_10 + 30 * self.cylinder3_green_zone_5
        total = total + 180 * self.cylinder4_red_zone_15 + 120 * self.cylinder4_yellow_zone_10 + 60 * self.cylinder4_green_zone_5
         
        if self.self_clasping_mechanism_bonus == 1:
            total = total + 80
        else:
            total = total + 0
 
        total = total + 20 * self.one_bounce_out_partial_score
        total = total - 50 * self.restarts
        total = total - 25 * self.timeouts
        total = total - 20 * self.outside_penalty
        total = total - 150 * self.bot_falling_off_the_zipline_penalty
        total = total - 100 * self.refill_penalty
        return total

    def __unicode__(self):
        return 'First Abyss round for team \'' + str(self.team) + '\''

class AbyssSecondRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'AB', 'promoted_to__exact' : 2 })

    
    cylinder1_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, red-zone')
    cylinder2_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, red zone')
    cylinder3_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, red zone')
    cylinder4_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, red zone')
    
    cylinder1_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, yellow zone')
    cylinder2_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, yellow zone')
    cylinder3_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, yellow zone')
    cylinder4_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, yellow zone')
    
    cylinder1_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, green zone')
    cylinder2_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, green zone')
    cylinder3_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, green zone')
    cylinder4_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, green zone')
    
    time_taken = models.IntegerField(verbose_name = 'Time taken')

    self_clasping_mechanism_bonus = models.IntegerField(default = False, verbose_name = 'Self clasping mechanism bonus? 1 for YES and 0 for NO')
    one_bounce_out_partial_score = models.IntegerField(verbose_name = 'Number of times the ball bounced outside the drop zone after bouncing off a cylinder wall')  
    outside_penalty = models.IntegerField(verbose_name = 'Number of balls that fell outside')
    bot_falling_off_the_zipline_penalty = models.IntegerField(verbose_name = 'Number of times the bot fell off the zip-line')
    bot_falling_off_after_clamping = models.IntegerField(verbose_name = 'Number of times the bot fell off after clamping') 
    clampings_done_right = models.IntegerField(verbose_name = 'Number of clampings done right')
    refill_penalty = models.IntegerField(verbose_name = 'Number of refills')
    restarts = models.IntegerField(verbose_name = 'Number of restarts')
    timeouts = models.IntegerField(verbose_name = 'Number of time-outs')
        

    def calculate_score(self):
        total = 390 - self.time_taken
        total = total + 1.5 * 15 * self.cylinder1_red_zone_15 + 15 * self.cylinder1_yellow_zone_10 + 1.5 * 5 * self.cylinder1_green_zone_5
        total = total + 30 * self.cylinder2_red_zone_15 + 20 * self.cylinder2_yellow_zone_10 + 10 * self.cylinder2_green_zone_5
        total = total + 45 * self.cylinder3_red_zone_15 + 30 * self.cylinder3_yellow_zone_10 + 15 * self.cylinder3_green_zone_5
        total = total + 90 * self.cylinder4_red_zone_15 + 60 * self.cylinder4_yellow_zone_10 + 30 * self.cylinder4_green_zone_5
        total = total + 250 * self.clampings_done_right

        if self.self_clasping_mechanism_bonus == 1:
            total = total + 80
        else: 
            total = total + 0 
         
        total = total + 20 * self.one_bounce_out_partial_score
        total = total - 50 * self.restarts
        total = total - 25 * self.timeouts
        total = total - 20 * self.outside_penalty
        total = total - 150 * self.bot_falling_off_the_zipline_penalty
        total = total - 100 * self.refill_penalty
        total = total - 30 * self.bot_falling_off_after_clamping
        return total

    def __unicode__(self):
        return 'Second Abyss round for team \'' + str(self.team) + '\''

class AbyssThirdRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'AB', 'promoted_to__exact' : 3 })
    
    cylinder1_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, red-zone')
    cylinder2_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, red zone')
    cylinder3_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, red zone')
    cylinder4_red_zone_15 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, red zone')
    
    cylinder1_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, yellow zone')
    cylinder2_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, yellow zone')
    cylinder3_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, yellow zone')
    cylinder4_yellow_zone_10 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, yellow zone')
    
    cylinder1_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 80cm high cylinder, green zone')
    cylinder2_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 60cm high cylinder, green zone')
    cylinder3_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 40cm high cylinder, green zone')
    cylinder4_green_zone_5 = models.IntegerField(verbose_name = 'Number of balls that fell in the 20cm high cylinder, green zone')
    
    time_taken = models.IntegerField(verbose_name = 'Time taken')

    self_clasping_mechanism_bonus = models.IntegerField(default = False, verbose_name = 'Self clasping mechanism bonus? 1 for YES and 0 for NO')
    one_bounce_out_partial_score = models.IntegerField(verbose_name = 'Number of times the ball bounced outside the drop zone after bouncing off a cylinder wall')  
    outside_penalty = models.IntegerField(verbose_name = 'Number of balls that fell outside')
    bot_falling_off_the_zipline_penalty = models.IntegerField(verbose_name = 'Number of times the bot fell off the zip-line')
    bot_falling_off_after_clamping = models.IntegerField(verbose_name = 'Number of times the bot fell off after clamping') 
    clampings_done_right = models.IntegerField(verbose_name = 'Number of clampings done right')
    refill_penalty = models.IntegerField(verbose_name = 'Number of refills')
    restarts = models.IntegerField(verbose_name = 'Number of restarts')
    timeouts = models.IntegerField(verbose_name = 'Number of time-outs')
        

    def calculate_score(self):
        total = 390 - self.time_taken 
        total = total + 1.5 * 15 * self.cylinder1_red_zone_15 + 15 * self.cylinder1_yellow_zone_10 + 1.5 * 5 * self.cylinder1_green_zone_5
        total = total + 30 * self.cylinder2_red_zone_15 + 20 * self.cylinder2_yellow_zone_10 + 10 * self.cylinder2_green_zone_5
        total = total + 45 * self.cylinder3_red_zone_15 + 30 * self.cylinder3_yellow_zone_10 + 15 * self.cylinder3_green_zone_5
        total = total + 90 * self.cylinder4_red_zone_15 + 60 * self.cylinder4_yellow_zone_10 + 30 * self.cylinder4_green_zone_5
        total = total + 250 * self.clampings_done_right

        if self.self_clasping_mechanism_bonus == 1:
            total = total + 80
        else: 
            total = total + 0 
         
        total = total + 20 * self.one_bounce_out_partial_score
        total = total - 50 * self.restarts
        total = total - 25 * self.timeouts
        total = total - 20 * self.outside_penalty
        total = total - 150 * self.bot_falling_off_the_zipline_penalty
        total = total - 100 * self.refill_penalty
        total = total - 30 * self.bot_falling_off_after_clamping
        return total

    def __unicode__(self):
        return 'Third Abyss round for team \'' + str(self.team) + '\''


class SeekerFirstRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'SE', 'promoted_to__exact' : 1 })

    time_taken = models.IntegerField(verbose_name='Time Taken')
    score= models.IntegerField(verbose_name='Final Score')
    restarts = models.IntegerField()
    number_of_fugitives_imprisoned = models.IntegerField()
    number_of_collisions = models.IntegerField()

    def calculate_score(self):
        total = 2000
        total = total - self.time_taken
        total = total - 1200 * self.restarts
        total = total + 600 * self.number_of_fugitives_imprisoned
        total = total - 450 * self.number_of_collisions
        return self.total

    def __unicode__(self):
        return 'First Nuke Clear round for team \'' + str(self.team) + '\'' 


class SeekerSecondRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'SE', 'promoted_to__exact' : 2 })
    time_taken = models.IntegerField(verbose_name='Time Taken')
    score= models.IntegerField(verbose_name='Final Score')
    
class ACROSSFirstRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'AC', 'promoted_to__exact' : 1 })
    
    d_speed_breakers = models.FloatField(verbose_name = 'Distance travelled on speed breakers')
    d_uneven_speed_breakers = models.FloatField(verbose_name = 'Distance travelled on continuous and uneven speed breakers')
    d_steps = models.FloatField(verbose_name = 'Distance travelled on steps')
    d_hill = models.FloatField(verbose_name = 'Distance travelled on hill')
    d_incline = models.FloatField(verbose_name = 'Distance travelled on compound incline')
    d_wedge = models.FloatField(verbose_name = 'Distance travelled on the wedge')
    d_bend = models.FloatField(verbose_name = 'Distance travelled on bends')

    y_water_outer_tumbler = models.FloatField(verbose_name = 'Volume of tumbler in outer tumbler (in ml)')
    num_restarts = models.IntegerField(verbose_name = 'Number of restarts')
    num_timeouts = models.IntegerField(verbose_name = 'Number of time-outs')
   
    fully_autonomous = models.IntegerField(verbose_name = 'Is the bot fully autonomous? Enter 1 for YES and 0 for NO. The bot cannot be both fully autonomous as well as semi autonomous. ') 
    semi_autonomous = models.IntegerField(verbose_name = 'Is the bot semi-autonomous? Enter 1 for YES and 0 for NO. ')

    time_taken = models.IntegerField(verbose_name = 'Time taken')

    def calculate_score(self):
        x = (self.y_water_outer_tumbler) / 80
        score = 0
        score = (5 * self.d_speed_breakers) + (6 * self.d_uneven_speed_breakers) + (7 * self.d_steps)
        score = score + (5 * self.d_hill) + (3 * self.d_incline) + (4 * self.d_wedge) + (2 * self.d_bend)
        score = score + (13 - x ) * (12 - x) * (25 - 2*x)
        score = score - 500 * self.num_restarts - 250 * self.num_timeouts - 3 * self.time_taken

        if self.fully_autonomous == 1:
            score = 1.2 * score


        if self.semi_autonomous == 1:
            score = 1.15 * score

        return score

    def __unicode__(self):
        return 'First ACROSS round for team \'' + str(self.team) + '\''
    
class ACROSSSecondRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'AC', 'promoted_to__exact' : 2 })
    
    
    d_speed_breakers = models.FloatField(verbose_name = 'Distance travelled on speed breakers')
    d_uneven_speed_breakers = models.FloatField(verbose_name = 'Distance travelled on continuous and uneven speed breakers')
    d_steps = models.FloatField(verbose_name = 'Distance travelled on steps')
    d_hill = models.FloatField(verbose_name = 'Distance travelled on hill')
    d_incline = models.FloatField(verbose_name = 'Distance travelled on compound incline')
    d_wedge = models.FloatField(verbose_name = 'Distance travelled on the wedge')
    d_bend = models.FloatField(verbose_name = 'Distance travelled on bends')

    y_water_outer_tumbler = models.FloatField(verbose_name = 'Volume of tumbler in outer tumbler (in ml)')
    num_restarts = models.IntegerField(verbose_name = 'Number of restarts')
    num_timeouts = models.IntegerField(verbose_name = 'Number of time-outs')
   
    fully_autonomous = models.IntegerField(verbose_name = 'Is the bot fully autonomous? Enter 1 for YES and 0 for NO ') 
    semi_autonomous = models.IntegerField(verbose_name = 'Is the bot semi-autonomous? Enter 1 for YES and 0 for NO ')

    time_taken = models.IntegerField(verbose_name = 'Time taken')

    def calculate_score(self):
        x = (self.y_water_outer_tumbler) / 80
        score = 0
        score = (5 * self.d_speed_breakers) + (6 * self.d_uneven_speed_breakers) + (7 * self.d_steps)
        score = score + (5 * self.d_hill) + (3 * self.d_incline) + (4 * self.d_wedge) + (2 * self.d_bend)
        score = score + (13 - x ) * (12 - x) * (25 - 2*x)
        score = score - 500 * self.num_restarts - 250 * self.num_timeouts - 3 * self.time_taken

        if self.fully_autonomous == 1:
            score = 1.2 * score


        if self.semi_autonomous == 1:
            score = 1.15 * score

        return score

def __unicode__(self):
        return 'Second ACROSS round for team \'' + str(self.team) + '\''

class ACROSSThirdRound(_EventBase):
    team = models.ForeignKey(Team, limit_choices_to = { 'event__exact' : 'AC', 'promoted_to__exact' : 3 })
    
    d_speed_breakers = models.FloatField(verbose_name = 'Distance travelled on speed breakers')
    d_uneven_speed_breakers = models.FloatField(verbose_name = 'Distance travelled on continuous and uneven speed breakers')
    d_steps = models.FloatField(verbose_name = 'Distance travelled on steps')
    d_hill = models.FloatField(verbose_name = 'Distance travelled on hill')
    d_incline = models.FloatField(verbose_name = 'Distance travelled on compound incline')
    d_wedge = models.FloatField(verbose_name = 'Distance travelled on the wedge')
    d_bend = models.FloatField(verbose_name = 'Distance travelled on bends')

    y_water_outer_tumbler = models.FloatField(verbose_name = 'Volume of tumbler in outer tumbler (in ml)')
    num_restarts = models.IntegerField(verbose_name = 'Number of restarts')
    num_timeouts = models.IntegerField(verbose_name = 'Number of time-outs')
   
    fully_autonomous = models.IntegerField(verbose_name = 'Is the bot fully autonomous? Enter 1 for YES and 0 for NO ') 
    semi_autonomous = models.IntegerField(verbose_name = 'Is the bot semi-autonomous? Enter 1 for YES and 0 for NO ')

    time_taken = models.IntegerField(verbose_name = 'Time taken')

    def calculate_score(self):
        x = (self.y_water_outer_tumbler) / 80
        score = 0
        score = (5 * self.d_speed_breakers) + (6 * self.d_uneven_speed_breakers) + (7 * self.d_steps)
        score = score + (5 * self.d_hill) + (3 * self.d_incline) + (4 * self.d_wedge) + (2 * self.d_bend)
        score = score + (13 - x ) * (12 - x) * (25 - 2*x)
        score = score - 500 * self.num_restarts - 250 * self.num_timeouts - 3 * self.time_taken

        if self.fully_autonomous == 1:
            score = 1.2 * score


        if self.semi_autonomous == 1:
            score = 1.15 * score

        return score

    def __unicode__(self):
        return 'Third ACROSS round for team \'' + str(self.team) + '\''


def rbtx_get_model_class_by_code_and_round(code, rnd):
    """ rbtx_get_model_class_by_code_and_round ('OV', 2) will return OverhaulSecondRound etc. """
    if not rbtx_is_valid_event_code(code):
        return None
    code = upper(code)

    try:
        rnd = int(rnd)
    except ValueError:
        return None

    if code == 'LU':
        if rnd == 1:
            return LumosFirstRound
        elif rnd == 2:
            return LumosSecondRound
        elif rnd == 3:
            return LumosThirdRound
    elif code == 'OV':
        if rnd == 1:
            return OverhaulFirstRound
        elif rnd == 2:
            return OverhaulSecondRound
        elif rnd == 3:
            return OverhaulThirdRound
    elif code == 'AB':
        if rnd == 1:
            return AbyssFirstRound
        elif rnd == 2:
            return AbyssSecondRound
        elif rnd == 3:
            return AbyssThirdRound
    elif code == 'SE':
        if rnd == 1:
            return SeekerFirstRound
        elif rnd == 2:
            return SeekerSecondRound
    elif code == 'AC':
        if rnd == 1:
            return ACROSSFirstRound
        elif rnd == 2:
            return ACROSSSecondRound
        elif rnd ==3:
            return ACROSSThirdRound
    return None

def rbtx_get_model_list():
    return [ LumosFirstRound, LumosSecondRound, LumosThirdRound, OverhaulFirstRound, OverhaulSecondRound, OverhaulThirdRound, AbyssFirstRound, AbyssSecondRound, AbyssThirdRound, ACROSSFirstRound, ACROSSSecondRound, ACROSSThirdRound ]

