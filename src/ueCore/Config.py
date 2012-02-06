import ueClient, ueSpec

import ueCore.Defaults as ueDefaults

class Config():
    def __init__(self, spec=ueSpec.Spec()):
        self.config = ueDefaults.Defaults()

#        if not spec.proj == None:
#            if "config" in ueDB.db[spec.proj]:
#                self.config = self.mergeConfig(self.config, ueDB.db[spec.proj]["config"].find_one())
#        if not spec.grp == None:
#            if "config" in ueDB.db[spec.proj][spec.grp]:
#                self.config = self.mergeConfig(self.config, ueDB.db[spec.proj][spec.grp]["config"].find_one())
#        if not spec.asst == None:
#            if "config" in ueDB.db[spec.proj][spec.grp][spec.asst]:
#                self.config = self.mergeConfig(self.config, ueDB.db[spec.proj][spec.grp][spec.asst]["config"].find_one())

    def mergeConfig(self, slave, master):
        config = dict(slave.items()+master.items())

        for c in config:
            if type(config[c]).__name__ == "dict":
                if c in slave and c in master:
                    config[c] = mergeConfig(slave[c], master[c])

        return config

