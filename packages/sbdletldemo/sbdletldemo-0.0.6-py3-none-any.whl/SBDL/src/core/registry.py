from SBDL.src.core.entity import Entity
from SBDL.src.entity.acctload import AcctLoad
from SBDL.src.entity.custload import CustLoad




class Registry:
    def getEntity(entity_name: str) -> Entity:
        switch = {
            "acctload" : AcctLoad(),
            "custload" : CustLoad()
        }
        return switch.get(entity_name.lower(), None)