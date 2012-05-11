

class UnitType(object):
    def __init__(self, race, name, minerals, gas, supply):
        self.race = race
        self.unit_name = name
        self.minerals = minerals
        self.gas = gas
        self.supply = supply
        self.simple_cost = minerals + gas

class UnitRef(object):
    ZERG = "ZERG"
    TOSS = "TOSS"
    TERRAN = "TERRAN"

    def __init__(self):

        #UnitRef.TOSS
        self.zealot = UnitType( UnitRef.TOSS,'zealot', 100, 0, 2)
        self.stalker = UnitType( UnitRef.TOSS,'stalker', 125, 50, 2)
        self.sentry = UnitType( UnitRef.TOSS,'sentry', 50, 100, 2)
        self.phoenix = UnitType( UnitRef.TOSS,'phoenix', 150, 100, 2)
        self.voidray = UnitType( UnitRef.TOSS,'voidray',250, 150, 3)
        self.photoncannon = UnitType( UnitRef.TOSS,'photoncannon', 150, 0, 0)
        self.hightemplar = UnitType( UnitRef.TOSS,'hightemplar', 50, 150, 2)
        self.darktemplar = UnitType( UnitRef.TOSS,'darktemplar', 125, 125, 2)
        self.colossus = UnitType( UnitRef.TOSS,'colossus', 300, 200, 6)
        self.carrier = UnitType( UnitRef.TOSS,'carrier', 450, 250, 6)
        self.archon = UnitType( UnitRef.TOSS,'archon', 100, 300, 4) #cannot support archons
        self.mothership = UnitType( UnitRef.TOSS,'mothership',400, 400, 8)
        self.observer = UnitType( UnitRef.TOSS,'observer', 50,100, 1)
        self.immortal = UnitType( UnitRef.TOSS,'immortal', 250, 150, 4)
        self.warpprism = UnitType( UnitRef.TOSS,'warpprism', 200, 50,2 )

        #UnitRef.TERRAN
        self.marine = UnitType( UnitRef.TERRAN,'marine', 50, 0, 1)
        self.marauder = UnitType( UnitRef.TERRAN,'marauder', 100, 25, 2)
        self.banshee = UnitType( UnitRef.TERRAN,'banshee', 150, 100, 3 )
        self.battlecruiser = UnitType( UnitRef.TERRAN,'battlecruiser',400, 300, 6 )
        self.ghost = UnitType( UnitRef.TERRAN,'ghost',150, 150, 2 )
        self.hellion = UnitType( UnitRef.TERRAN,'hellion',100, 0, 2 )
        self.medivac = UnitType( UnitRef.TERRAN,'medivac',100, 100, 2 )
        self.missileturret = UnitType( UnitRef.TERRAN,'missileturret',100, 0, 0 )
        self.planetaryfortress = UnitType( UnitRef.TERRAN,'planetaryfortress',550, 150, 0 )
        self.raven = UnitType( UnitRef.TERRAN,'raven',100, 200, 2 )
        self.reaper = UnitType( UnitRef.TERRAN,'reaper',50, 50, 1 )
        self.siegetank_sieged = UnitType( UnitRef.TERRAN,'siegetank_sieged',150, 125, 3 )
        self.siegetank = UnitType( UnitRef.TERRAN,'siegetank',150, 125, 3 )
        self.thor = UnitType( UnitRef.TERRAN,'thor',300, 200, 6 )
        self.viking = UnitType( UnitRef.TERRAN,'viking',150, 75, 2 )

        #UnitRef.ZERG
        self.broodlord = UnitType( UnitRef.ZERG, 'broodlord', 150, 150, 4)
        self.baneling_burrowed = UnitType( UnitRef.ZERG, 'baneling_burrowed',50, 25, 0.5 )
        self.baneling = UnitType( UnitRef.ZERG, 'baneling',50, 25, 0.5 )
        self.corruptor_burrowed = UnitType( UnitRef.ZERG, 'corruptor_burrowed', 150, 100, 2 )
        self.corruptor = UnitType( UnitRef.ZERG, 'corruptor', 150, 100, 2 )
        self.hydralisk_burrowed = UnitType( UnitRef.ZERG, 'hydralisk_burrowed', 100, 50, 2 )
        self.hydralisk = UnitType( UnitRef.ZERG, 'hydralisk', 100, 50, 2 )
        self.infestor_burrowed = UnitType( UnitRef.ZERG, 'infestor_burrowed',100, 150, 2 )
        self.infestor = UnitType( UnitRef.ZERG, 'infestor',100, 150, 2 )
        self.infestedterran_burrowed = UnitType( UnitRef.ZERG, "infestedterran_burrowed", 0, 0, 0 )
        self.infestedterran = UnitType( UnitRef.ZERG, "infestedterran", 0, 0, 0 )
        self.mutalisk = UnitType( UnitRef.ZERG, 'mutalisk',100, 100, 2 )
        self.nydusworm = UnitType( UnitRef.ZERG, 'nydusworm',100, 100, 0 )
        self.overlord = UnitType( UnitRef.ZERG, 'overlord',100, 0, 0 )
        self.overseer = UnitType( UnitRef.ZERG, 'overseer',150, 100, 0 )
        self.queen_burrowed = UnitType( UnitRef.ZERG, 'queen_burrowed',125, 0, 2 )
        self.queen = UnitType( UnitRef.ZERG, 'queen',125, 0, 2 )
        self.roach_burrowed = UnitType( UnitRef.ZERG, 'roach_burrowed',75, 25, 2 )
        self.roach = UnitType( UnitRef.ZERG, 'roach',75, 25, 2 )
        self.spinecrawler_burrowed = UnitType( UnitRef.ZERG, 'spinecrawler_burrowed',150, 0, 0 )
        self.spinecrawler = UnitType( UnitRef.ZERG, 'spinecrawler',150, 0, 0 )
        self.sporecrawler_burrowed = UnitType( UnitRef.ZERG, 'sporecrawler_burrowed',125, 0, 0 )
        self.sporecrawler = UnitType( UnitRef.ZERG, 'sporecrawler',125, 0, 0 )
        self.ultralisk_burrowed = UnitType( UnitRef.ZERG, 'ultralisk_burrowed',300, 200, 6 )
        self.ultralisk = UnitType( UnitRef.ZERG, 'ultralisk',300, 200, 6 )
        self.zergling_burrowed = UnitType( UnitRef.ZERG, 'zergling_burrowed',25, 0, 0.5 )
        self.zergling = UnitType( UnitRef.ZERG, 'zergling',25, 0, 0.5 )

        list = []
        lookup = {}

        for name, value in self.__dict__.iteritems():
            lookup[name] = value
            list.append(value)

        self.list = list
        self.lookup = lookup
        