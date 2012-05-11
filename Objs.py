from Reference import UnitRef

class AA(object):
    UNIT_REF = UnitRef()
    __slots__ = "player_index","unit_name","born_frame","died_frame","simple_cost"
    def __init__(self, player_index, unit_name, born_frame, died_frame):
        self.player_index = player_index
        self.unit_name = unit_name
        self.born_frame = born_frame
        self.died_frame = died_frame
        self.simple_cost = AA.UNIT_REF.lookup[unit_name].simple_cost

    def __repr__(self):
        return str(AA.get_raw(self))

    @staticmethod
    def get_raw(aa):
        return aa.player_index, aa.unit_name, aa.born_frame, aa.died_frame

    @staticmethod
    def from_raw(raw):
        return AA(*raw)

class Fight(object):
    def __init__(self, game_id, start_index, end_index, start_frame, end_frame):
        self.game_id = game_id
        self.start_index = start_index
        self.end_index = end_index
        self.start_frame = start_frame
        self.end_frame = end_frame
    def __repr__(self):
        return str(Fight.get_raw(self))

    @staticmethod
    def get_raw(fight):
        return fight.game_id, fight.start_index, fight.end_index, fight.start_frame, fight.end_frame

    @staticmethod
    def from_raw(raw):
        return Fight(*raw)


class Game(object):
    __slots__ = "game_id","players","aa_list"
    def __init__(self, game_id, players, aa_list):
        self.game_id = game_id
        self.players = players
        self.aa_list = aa_list

        for i in range(1, len(aa_list)):
            if(aa_list[i-1].died_frame > aa_list[i].died_frame):
                raise Exception("units must be sorted by died_frame!")

    def __repr__(self):
        return str(Game.get_raw(self))

    @staticmethod
    def get_raw(game):
        return game.game_id, game.players, [AA.get_raw(aa) for aa in game.aa_list]

    @staticmethod
    def from_raw(raw):
        return Game(raw[0], raw[1], [AA.from_raw(raw_aa) for raw_aa in raw[2]])


