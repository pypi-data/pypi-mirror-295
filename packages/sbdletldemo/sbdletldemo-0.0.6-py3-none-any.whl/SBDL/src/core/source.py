from SBDL.lib.utils import spark

class Source:
    def loadSource(self):...

class S3Source(Source):
    pass

class PostgresSource(Source):
    pass

class LocalSource(Source):

    def __init__(self, path: str, filetype: str, delimiter: str, tempViemName : str, header: bool = True):
        self.path = path
        self.filetype = filetype
        self.delimiter = delimiter
        self.header = header
        self.tempViewName = tempViemName
    
    def loadSource(self):
        spark.read \
            .format(self.filetype) \
            .option("header", self.header) \
            .option("delimiter", self.delimiter)\
            .load(self.path).createOrReplaceTempView(self.tempViewName)
        


    