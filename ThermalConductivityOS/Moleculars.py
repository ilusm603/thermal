from ThermalConductivityOS.SingleMolecular import SingleMolecular


class Moleculars:

    def __init__(self, df):
        self.df = df

    def __str__(self):
        return "This datasheet contains {} entries of thermal conductivity".format(len(self.df))

    def __len__(self):
        return len(self.df)

    def head(self, num=5):
        return self.df.head(num)

    def addSingleMolecular(self, dic):
        if type(dic) == dict:
            self.df.append(dic)
        else:
            raise TypeError(
                "The input must be a dict object or SingleMolecular object!")

    def addSingleMolecular(self, sm):
        if type(sm) == SingleMolecular:
            dic = {"MF": sm.getMF(), "Name": sm.getName(),
                   "100K": sm.getValueOfK(100), "200K": sm.getValueOfK(200),
                   "300K": sm.getValueOfK(300), "400K": sm.getValueOfK(400),
                   "500K": sm.getValueOfK(500), "600K": sm.getValueOfK(600)}
            self.df.append(dic)
        else:
            raise TypeError(
                "The input must be a dict object or SingleMolecular object!")

    def deleteSingleMolecular(self, MF):
        MFList = self.df["MF"].tolist()
        if MF in MFList:
            index = self.df[self.df["MF"] == MF].index
            self.df.drop(index, axis=0, inplace=True)
            self.df.reset_index(drop=True)
        else:
            raise ValueError("Not Found!")

    def deleteSingleMolecular(self, index):
        if index < len(self.df) and index >= 0:
            self.df.drop(index, axis=0, inplace=True)
            self.df.reset_index(drop=True)
        else:
            raise ValueError("Wrong index!")

    def getByIndex(self, index):
        if index < len(self.df) and index >= 0:
            tmp = self.df.iloc[index, :].tolist()
            return SingleMolecular(tmp[0], tmp[1], [tmp[2], tmp[3], 
                                    tmp[4], tmp[5], tmp[6], tmp[7]])
        else:
            raise ValueError("Wrong index!")

    def getByMF(self, MF):
        MFList = self.df["MF"].tolist()
        if MF in MFList:
            index = self.df[self.df["MF"] == MF].index
            tmp = self.df.iloc[index, :].tolist()
            return SingleMolecular(tmp[0], tmp[1], tmp[2], tmp[3], 
                                    tmp[4], tmp[5], tmp[6], tmp[8])
        else:
            raise ValueError("Wrong MF!")

    def getByName(self, Name):
        NameList = self.df["Name"].tolist()
        if Name in NameList:
            index = self.df[self.df["Name"] == Name].index
            tmp = self.df.iloc[index, :].tolist()
            return SingleMolecular(tmp[0], tmp[1], tmp[2], tmp[3], 
                                   tmp[4], tmp[5], tmp[6], tmp[8])
        else:
            raise ValueError("Wrong Name!")

    def sortBy(self, col, ascending=True):
        columns = self.df.columns.tolist()
        if col in columns:
            self.df.sort_values(by=col, inplace=True,
                                ignore_index=True, ascending=ascending)
            return self.df
        else:
            raise ValueError("Wrong column!")

    def toPandas(self):
        return self.df

    def save_csv(self, file_name):
        self.df.to_csv(file_name, index=False)
