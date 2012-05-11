import math
import Costs
import FightUtils

def get_report(games, max_frame_gap = 16*20, ignore_end_frames = 16*10, minimum_gross_losses = 1000, limit_ratio_change_mult = 1.5):
    # cost_data contains 3 dict each map game to list of Fights, player_fight_costs, or NetFightCosts respectively
    cost_data = _get_fight_costs(games, max_frame_gap, ignore_end_frames, limit_ratio_change_mult)
    game_fights, game_player_fight_costs, game_net_fight_costs = cost_data

    working_buckets = {}
    log_count_by_bucket = {}
    for game_id, fight_net_costs in game_net_fight_costs.iteritems():
        for net_costs in fight_net_costs:
            if net_costs.army_ratio: # false if skipped due to zeros
                if net_costs.gross_kills >= minimum_gross_losses:
                    key = get_rounded_bucket(net_costs.army_ratio, .05)
                    # if domain problem, this is None, so adjust our log_count denominator accordingly
                    if net_costs.log_ratio_change:
                        log_count = log_count_by_bucket.setdefault(key, 0)
                        log_count_by_bucket[key] = log_count + 1
                    working_buckets.setdefault(key,[]).append(net_costs)

    complete_buckets = {}
    for army_ratio_bucket, net_costs in working_buckets.iteritems():
        count = len( net_costs )
        log_count = log_count_by_bucket[army_ratio_bucket] if army_ratio_bucket in log_count_by_bucket else 1

        # wasteful for clarity
        net_start        = sum( nc.net_start        for nc in net_costs ) / count
        net_rein         = sum( nc.net_rein         for nc in net_costs ) / count
        net_remain       = sum( nc.net_remaining    for nc in net_costs ) / count
        net_kill         = sum( nc.net_kills        for nc in net_costs ) / count
        army_ratio_after = sum( nc.army_ratio_after for nc in net_costs ) / count - army_ratio_bucket

        log_change       = math.exp( sum( nc.log_ratio_change for nc in net_costs if nc.log_ratio_change ) / log_count )

        gross_kills      = sum( nc.gross_kills  for nc in net_costs ) / count
        gross_start      = sum( nc.gross_start  for nc in net_costs ) / count
        gross_remain     = sum( nc.gross_remain for nc in net_costs ) / count
        gross_rein       = sum( nc.gross_rein   for nc in net_costs ) / count

        complete_buckets[army_ratio_bucket] = [army_ratio_bucket, net_start, net_rein, net_remain,
                                               net_kill, log_change, army_ratio_after, gross_kills, gross_start,
                                               gross_remain, gross_rein, count ]

    return ['army_ratio_bucket', 'net_start', 'net_rein', 'net_remain',
            'net_kill', 'log_change', 'army_ratio_change', 'gross_kills', 'gross_start',
            'gross_remain', 'gross rein', 'count'], complete_buckets


def _get_fight_costs( games, max_frame_gap, ignore_end_frames, limit_ratio_change_mult ):
    game_fights = {}
    game_fight_player_costs = {}
    game_fight_net_costs = {}

    for game in games:
        fights, fight_player_costs,fight_net_costs = [],[],[]

        game_fights[game.game_id] = fights
        game_fight_player_costs[game.game_id] = fight_player_costs
        game_fight_net_costs[game.game_id] = fight_net_costs
        for fight in FightUtils.iter_fights(game, max_frame_gap):
            fights.append(fight)
            player_costs = Costs.get_player_fight_costs(game,fight, ignore_end_frames)
            net_costs = Costs.NetFightCosts(player_costs[0], player_costs[1], limit_ratio_change_mult)

            fight_player_costs.append(player_costs)
            fight_net_costs.append(net_costs)

    return game_fights, game_fight_player_costs, game_fight_net_costs


# return a number floored to width, allows floats
def get_rounded_bucket(value, width):
    sizer = int( width * 100 )
    value = int( value * 100 )
    return ( ( value / sizer ) * sizer ) / float( 100 )
