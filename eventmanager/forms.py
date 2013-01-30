from django import forms
from django.utils.datastructures import SortedDict

from eventmanager.models import *
from eventmanager.view_utils import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Team

#class ImportForm(forms.ModelForm):
#   class Meta:
#      model = Import

_common_fields = ('edited_score', 'best_algorithm_design', 'best_mechanical_design', 'comments')

class LumosFirstRoundForm(forms.ModelForm):
    class Meta:
        model = LumosFirstRound
        fields = ('team', 'stationaryLight_deactivated', 'movingLight_deactivated', 'incorrect_source',
                   'num_restarts', 'num_timeouts','max_time_to_be_allotted', 'time_taken') + _common_fields

class LumosSecondRoundForm(forms.ModelForm):
    class Meta:
        model = LumosSecondRound
        fields = ('team', 'stationaryLight_deactivated', 'movingLight_deactivated', 'incorrect_source',
                   'num_restarts', 'num_timeouts','max_time_to_be_allotted', 'time_taken') + _common_fields

class LumosThirdRoundForm(forms.ModelForm):
    class Meta:
        model = LumosThirdRound
        fields = ('team', 'stationaryLight_deactivated', 'movingLight_deactivated', 'incorrect_source',
                   'num_restarts', 'num_timeouts','max_time_to_be_allotted', 'time_taken') + _common_fields

class OverhaulFirstRoundForm(forms.ModelForm):
    class Meta:
        model = OverhaulFirstRound
        fields = ('team', 'black_cylinders', 'white_cylinders', 'candles_put_out', 'cylinders_in_safe_zone',
                  'fires_touched', 'fires_dropped', 'cylinder_in_contact_with_candle', 'restarts', 'timeouts', 'time_taken') + _common_fields

class OverhaulSecondRoundForm(forms.ModelForm):
    class Meta:
        model = OverhaulSecondRound
        fields = ('team', 'black_cylinders', 'white_cylinders', 'candles_put_out', 'cylinders_in_safe_zone', 
                  'fires_touched', 'fires_dropped', 'cylinder_in_contact_with_candle', 'restarts', 'timeouts', 'time_taken') + _common_fields

class OverhaulThirdRoundForm(forms.ModelForm):
    class Meta:
        model = OverhaulThirdRound
        fields = ('team', 'black_cylinders', 'white_cylinders', 'candles_put_out', 'cylinders_in_safe_zone',
                  'fires_touched', 'fires_dropped', 'cylinder_in_contact_with_candle', 'restarts', 'timeouts', 'time_taken') + _common_fields

class AbyssFirstRoundForm(forms.ModelForm):
    class Meta:
        model = AbyssFirstRound
        fields = ('team', 'cylinder1_red_zone_15', 'cylinder2_red_zone_15', 'cylinder3_red_zone_15', 'cylinder4_red_zone_15',
                  'cylinder1_yellow_zone_10', 'cylinder2_yellow_zone_10', 'cylinder3_yellow_zone_10', 'cylinder4_yellow_zone_10',
                  'cylinder1_green_zone_5', 'cylinder2_green_zone_5', 'cylinder3_green_zone_5', 'cylinder4_green_zone_5',
                  'time_taken', 'self_clasping_mechanism_bonus', 'one_bounce_out_partial_score','restarts','timeouts',
                  'outside_penalty', 'bot_falling_off_the_zipline_penalty', 'refill_penalty') + _common_fields

class AbyssSecondRoundForm(forms.ModelForm):
    class Meta:
        model = AbyssSecondRound
        fields = ('team', 'cylinder1_red_zone_15', 'cylinder2_red_zone_15', 'cylinder3_red_zone_15', 'cylinder4_red_zone_15',
                  'cylinder1_yellow_zone_10', 'cylinder2_yellow_zone_10', 'cylinder3_yellow_zone_10', 'cylinder4_yellow_zone_10',
                  'cylinder1_green_zone_5', 'cylinder2_green_zone_5', 'cylinder3_green_zone_5', 'cylinder4_green_zone_5',
                  'clampings_done_right', 'bot_falling_off_after_clamping',     
                  'time_taken', 'self_clasping_mechanism_bonus', 'one_bounce_out_partial_score','restarts','timeouts',
                  'outside_penalty', 'bot_falling_off_the_zipline_penalty', 'refill_penalty') + _common_fields

class AbyssThirdRoundForm(forms.ModelForm):
    class Meta:
        model = AbyssThirdRound
        fields = ('team', 'cylinder1_red_zone_15', 'cylinder2_red_zone_15', 'cylinder3_red_zone_15', 'cylinder4_red_zone_15',
                  'cylinder1_yellow_zone_10', 'cylinder2_yellow_zone_10', 'cylinder3_yellow_zone_10', 'cylinder4_yellow_zone_10',
                  'cylinder1_green_zone_5', 'cylinder2_green_zone_5', 'cylinder3_green_zone_5', 'cylinder4_green_zone_5',
                  'clampings_done_right', 'bot_falling_off_after_clamping',  
                  'time_taken', 'self_clasping_mechanism_bonus', 'one_bounce_out_partial_score','restarts','timeouts',
                  'outside_penalty', 'bot_falling_off_the_zipline_penalty', 'refill_penalty') + _common_fields

class ACROSSFirstRoundForm(forms.ModelForm):
    class Meta:
        model = ACROSSFirstRound
        fields = ('team', 'd_speed_breakers', 'd_uneven_speed_breakers', 'd_steps', 'd_hill', 'd_incline',
                  'd_wedge', 'd_bend', 'y_water_outer_tumbler', 'num_restarts', 'num_timeouts', 
                  'fully_autonomous', 'semi_autonomous', 'time_taken') + _common_fields  

class ACROSSSecondRoundForm(forms.ModelForm):
    class Meta:
        model = ACROSSSecondRound
        fields = ('team', 'd_speed_breakers', 'd_uneven_speed_breakers', 'd_steps', 'd_hill', 'd_incline',
                  'd_wedge', 'd_bend', 'y_water_outer_tumbler', 'num_restarts', 'num_timeouts', 
                  'fully_autonomous', 'semi_autonomous', 'time_taken') + _common_fields

class ACROSSThirdRoundForm(forms.ModelForm):
    class Meta:
        model = ACROSSThirdRound
        fields = ('team', 'd_speed_breakers', 'd_uneven_speed_breakers', 'd_steps', 'd_hill', 'd_incline',
                  'd_wedge', 'd_bend', 'y_water_outer_tumbler', 'num_restarts', 'num_timeouts', 
                  'fully_autonomous', 'semi_autonomous', 'time_taken') + _common_fields

class SeekerFirstRoundForm(forms.ModelForm):
    class Meta:
        model = SeekerFirstRound
        fields = ('team', 'time_taken', 'score') + _common_fields

class SeekerSecondRoundForm(forms.ModelForm):
    class Meta:
        model = SeekerSecondRound
        fields = ('team', 'time_taken', 'score') + _common_fields

"""class SeekerThirdRoundForm(forms.ModelForm):
    class Meta:
        model = SeekerThirdRound
        fields = ('team', 'time_taken', 'score') + _common_fields  """
 

def rbtx_get_form_class_by_code_and_round(code, rnd):
    """ rbtx_get_form_class_by_code_and_round ('OV', 2) will return OverhaulSecondRoundForm etc. """
    if not rbtx_is_valid_event_code(code):
        return None
    code = upper(code)

    try:
        rnd = int(rnd)
    except ValueError:
        return None
    
    if code == 'LU':
        if rnd == 1:
            return LumosFirstRoundForm
        elif rnd == 2:
            return LumosSecondRoundForm
        elif rnd == 3:
            return LumosThirdRoundForm
    elif code == 'OV':
        if rnd == 1:
            return OverhaulFirstRoundForm
        elif rnd == 2:
            return OverhaulSecondRoundForm
        elif rnd == 3:
            return OverhaulThirdRoundForm
    elif code == 'AB':
        if rnd == 1:
            return AbyssFirstRoundForm
        elif rnd == 2:
            return AbyssSecondRoundForm
        elif rnd == 3:
            return AbyssThirdRoundForm
    elif code == 'SE':
        if rnd == 1:
            return SeekerFirstRoundForm
        elif rnd == 2:
            return SeekerSecondRoundForm
    elif code == 'AC':
        if rnd == 1:
            return ACROSSFirstRoundForm
        elif rnd == 2:
            return ACROSSSecondRoundForm
        elif rnd ==3:
            return ACROSSThirdRoundForm
    return None
   
def rbtx_make_promotion_form(models, src_round):
    fields = SortedDict()
    i = 1
    for model in models:
        x = False
        if model.team.promoted_to == src_round + 1:
            msg = str (i) + ". " + str(model.team) + ' - ' + str(model.edited_score) + ' points (College: ' + model.team.college + ')'
            x = True
        elif model.team.promoted_to == src_round:
            msg = str (i) + ". " + str(model.team) + ' - ' + str(model.edited_score) + ' points (College: ' + model.team.college + ')'
        else:
            continue
        fields [model.team.get_decorated_team_id ()] = forms.BooleanField(label = msg, required = False,
                                                                          initial = x,
                                                                          help_text = '<a href="/info/' + model.team.get_decorated_team_id() + '" target="blank_">info</a>')
        fields.keyOrder.append(model.team.get_decorated_team_id ())
        i = i + 1
    return type('PromotionForm', (forms.BaseForm,), { 'base_fields' : fields} )
