import json

from SBDL.src.core.registry import Registry
from SBDL.src.core.entity import Entity

from SBDL.lib.logger import logger

class Publisher:
    
    def readSources(self, entity : Entity):
        for source in entity.sources:
            logger.info("Reading source : {}".format(source.__class__.__name__))
            source.loadSource()
        

    def save():
        pass


    def write():
        pass

    def getConfiguration(self, config: str) -> dict:
        logger.info(config)
        return json.loads(config)

    def run(self, config: str):
        print("Fetching entity from registry")
        config = self.getConfiguration(config)
        entity: Entity = Registry.getEntity(config["entity"])
        logger.info(entity.name+" is running")
        self.readSources(entity)
        df = entity.transform()
        entity.target.write(df)
        # print(entity.name)
        # self.readSources()