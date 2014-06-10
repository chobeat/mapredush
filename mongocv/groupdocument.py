from document import Document


class GroupDocument(Document):
    def __init__(self, idfield):
        Document.__init__(self)
        self.insidedoc = Document()
        if isinstance(idfield, Document):
            idfield = idfield.getdoc()
            for key in idfield:
                if not idfield[key].startswith("$"):
                    idfield[key] = "$"+idfield[key]
        elif not idfield.startswith("$"):
            idfield = "$"+idfield

        self.insidedoc.add("_id", idfield)

    def addsum(self, key, value):
        self.addnormalaggregator("$sum", key, value)

    def addavg(self,key,value):
        self.addnormalaggregator("$avg", key, value)

    def addmin(self,key,value):
        self.addnormalaggregator("$min", key, value)

    def addmax(self,key,value):
        self.addnormalaggregator("$max", key, value)

    def addfirst(self, key, value):
        self.addnormalaggregator("$first", key, value)

    def addlast(self, key, value):
        self.addnormalaggregator("$last", key, value)

    def addtoset(self, key, value):
        self.addnormalaggregator("$addToSet", key, value)

    def addpush(self,key,value):
        if isinstance(value, Document):
            temp = value.getdoc()
            for key in temp:
                if not temp[key].startswith("$"):
                    temp[key] = "$"+temp[key]
        self.addnormalaggregator("$push", key, value)

    def addnormalaggregator(self, name, key, value):
        tempdoc = Document()
        if isinstance(value, str):
            if not value.startswith("$"):
                value = "$"+value

        tempdoc.add(name, value)
        self.insidedoc.add(key, tempdoc)

    def __str__(self):
        self.add("$group", self.insidedoc)
        return str(self.doc)

    def getdoc(self):
        self.add("$group", self.insidedoc.getdoc())
        return self.doc