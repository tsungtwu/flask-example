import re


class RegToolBox():

    cvePattern = r"CVE-[0-9]{4}-[0-9]{4}"
    wordPattern = r"^\w[\w.\-#&\s]*$"
    md5Pattern = r"^[a-f0-9]{32}$"
    vtDirPattern = r"all|iotpot|cznic"
    def checkCveId(self, cveId):
        """" check cveId Format  """
        if cveId == None:
            return False
        prog = re.compile(self.cvePattern)
        return False if prog.match(cveId) == None else True


    def checkWord(self, words):
        """" check normail words or not  """
        if words == None:
            return False
        prog = re.compile(self.wordPattern)
        return False if prog.match(words) == None else True

    def checkMd5(self, words):
        """" check md5 format """
        if words == None:
            return False
        prog = re.compile(self.md5Pattern)
        return False if prog.match(words) == None else True

    def checkVtDir(self, words):
        """" check vtDir format """
        if words == None:
            return False
        prog = re.compile(self.vtDirPattern)
        return False if prog.match(words) == None else True