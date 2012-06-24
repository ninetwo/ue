import os

class Context():
    def __init__(self):
        self.spec = Spec(proj=os.getenv("PROJ", None),
                         grp=os.getenv("GRP", None),
                         asst=os.getenv("ASST", None))
        self.proj = self.spec.proj
        self.grp = self.spec.grp
        self.asst = self.spec.asst

    def toArray(self):
        return self.spec.toArray()

    def __str__(self):
        return str(self.spec)


class Spec():
    def __init__(self, proj=None, grp=None, asst=None,
                 elclass=None, eltype=None, elname=None,
                 vers=None, elpass=None):

        self.proj = proj
        self.grp = grp
        self.asst = asst
        self.elclass = elclass
        self.eltype = eltype
        self.elname = elname
        self.vers = vers
        if not self.vers == None:
            self.vers = int(self.vers)
        self.elpass = elpass

        if not proj == None and grp == None:
            self.parseString(proj)

    def parseString(self, spec):
        s = spec.split(":")
        if len(s) > 0:
            self.proj = s[0]
        if len(s) > 1:
            self.grp = s[1]
        if len(s) > 2:
            self.asst = s[2]
        if len(s) > 3:
            self.elname = s[3]
        if len(s) > 4:
            self.eltype = s[4]
        if len(s) > 5:
            self.elclass = s[5]
        if len(s) > 6:
            self.vers = int(s[6])
        if len(s) > 7:
            self.elpass = s[7]

    def toArray(self):
        a = []
        if not self.proj == None:
            a.append(self.proj)
        if not self.grp == None:
            a.append(self.grp)
        if not self.asst == None:
            a.append(self.asst)
        if not self.elclass == None:
            a.append(self.elclass)
        if not self.eltype == None:
            a.append(self.eltype)
        if not self.elname == None:
            a.append(self.elname)
        if not self.vers == None:
            a.append(str(self.vers))
        if not self.elpass == None:
            a.append(self.elpass)
        return a

    def __str__(self):
        s = ""
        if not self.proj == None:
            s += self.proj
        if not self.grp == None:
            s += ":"+self.grp
        if not self.asst == None:
            s += ":"+self.asst
        if not self.elname == None:
            s += ":"+self.elname
        if not self.eltype == None:
            s += ":"+self.eltype
        if not self.elclass == None:
            s += ":"+self.elclass
        if not self.vers == None:
            s += ":%04d" % int(self.vers)
        if not self.elpass == None:
            s += ":"+self.elpass
        return s

