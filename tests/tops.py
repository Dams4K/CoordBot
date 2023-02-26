from operator import itemgetter, attrgetter

class MemberData:
    def __init__(self, name, level, xp):
        self.name = name
        self.level = level
        self.xp = xp
    def __repr__(self):
        return repr((self.name, self.level, self.xp))

members = [
    MemberData("Dams4K", 14, 784),
    MemberData("Partof", 4, 779),
    MemberData("Partof2", 4, 456),
    MemberData("Paelos", 7, 415)      
]

members.sort(key=attrgetter("level", "xp"), reverse=True)
print(members)