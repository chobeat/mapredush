
class Aggregate:
    def __init__(self):
        self.pipeline = list()

    def add(self, operatordocument):
        doc = operatordocument.getdoc()
        self.pipeline.append(doc)

    def __str__(self):
        return str(self.pipeline)

    def getaggregate(self):
        return self.pipeline

