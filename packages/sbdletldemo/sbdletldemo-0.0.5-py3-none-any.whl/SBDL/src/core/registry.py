from SBDL.src.core.entity import Entity
from SBDL.src.entity.acctload import AcctLoad




class Registry:
    def getEntity(entity_name: str) -> Entity:
        switch = {
            "acctload" : AcctLoad()
        }
        return switch.get(entity_name.lower(), None)