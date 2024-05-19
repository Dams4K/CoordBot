import os
from datetime import datetime

from ddm import *
from utils.references import References


class StatsData(Saveable):
    BYPASS_UNKNOWN_VARIABLES = True

    def __init__(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_timestamp = int(today.timestamp())
        super().__init__(os.path.join(References.DATA_FOLDER, "stats", "%s.json" % today_timestamp))
    
    @Saveable.update()
    def increment_cmd(self, ctx):
        cog_name = ctx.cog.__class__.__name__

        cog_stats = getattr(self, cog_name, 0)
        setattr(self, cog_name, cog_stats+1)