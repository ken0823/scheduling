#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config
from itertools import combinations_with_replacement


class Coreset:

    def __init__(self, name=""):
        self.name = name
        self.core_num = None
        self.corepair_num = None

    def set_CoresetConf(self, option=1, biglittle_model=None, core_num=None,
                        bigcore_num=None, littlecore_num=None,
                        bigcore_freq=None, littlecore_freq=None,
                        bigcore_power=None, littlecore_power=None):
        if option == 0:
            self.biglittle_model = biglittle_model
            self.core_num = core_num
            self.bigcore_num = bigcore_num
            self.littlecore_num = littlecore_num
            self.bigcore_freq = bigcore_freq
            self.littlecore_freq = littlecore_freq
            self.bigcore_power = bigcore_power
            self.littlecore_power = littlecore_power
        elif option == 1:
            self.biglittle_model = 1
            self.core_num = config.CORE_NUM
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.bigcore_freq = config.BIGCORE_FREQ_HAS_SLEEP
            self.littlecore_freq = config.LITTLECORE_FREQ_HAS_SLEEP
            self.bigcore_power = config.BIGCORE_POWER_HAS_SLEEP
            self.littlecore_power = config.LITTLECORE_POWER_HAS_SLEEP
        elif option == 2:
            self.biglittle_model = 2
            self.core_num = config.CORE_NUM
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.bigcore_freq = config.BIGCORE_FREQ
            self.littlecore_freq = config.LITTLECORE_FREQ
            self.bigcore_power = config.BIGCORE_POWER
            self.littlecore_power = config.LITTLECORE_POWER
        elif option == 3:
            self.biglittle_model = 3
            self.core_num = config.CORE_PAIR_NUM
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.bigcore_freq = config.BIGCORE_FREQ_HAS_SLEEP
            self.littlecore_freq = config.LITTLECORE_FREQ_HAS_SLEEP
            self.bigcore_power = config.BIGCORE_POWER_HAS_SLEEP
            self.littlecore_power = config.LITTLECORE_POWER_HAS_SLEEP
        elif option == 4:
            self.biglittle_model = 4
            self.core_num = config.CORE_PAIR_NUM
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.bigcore_freq = config.BIGCORE_FREQ
            self.littlecore_freq = config.LITTLECORE_FREQ
            self.bigcore_power = config.BIGCORE_POWER
            self.littlecore_power = config.LITTLECORE_POWER
        else:
            print("Error: in function set_Coreset_Conf, Unexpected Option {0}"
                  .format(option))
            exit()

    def set_bigcore_num(self, newvalue):
        self.bigcore_num = newvalue

    def set_littlecore_num(self, newvalue):
        self.littlecore_num = newvalue

    def set_core_num(self, newvalue):
        self.core_num = newvalue

    def set_bigcore_freq(self, newlist):
        self.bigcore_freq = newlist

    def set_bigcore_power(self, newlist):
        self.bigcore_power = newlist

    def set_littlecore_freq(self, newlist):
        self.littlecore_freq = newlist

    def set_littlecore_power(self, newlist):
        self.littlecore_power = newlist

    def create_Coresets(self, option=1):
        self.bigcore_freqlist = []
        self.littlecore_freqlist = []
        self.core_freqlist = []
        self.bigcore_powerlist = []
        self.littlecore_powerlist = []
        self.core_powerlist = []
        if option == 1:
            self.bigcore_freqlist = [list(i) for i in
                                     combinations_with_replacement(self.bigcore_freq,
                                                                   self.bigcore_num)]
            self.littlecore_freqlist = [list(i) for i in
                                        combinations_with_replacement(self.littlecore_freq,
                                                                      self.littlecore_num)]
            for i in range(len(self.bigcore_freqlist)):
                for j in range(len(self.littlecore_freqlist)):
                    self.core_freqlist.append(list(self.bigcore_freqlist[i] +
                                                   self.littlecore_freqlist[j]))
            self.core_freqlist.reverse()
            self.bigcore_powerlist = [list(i) for i in
                                      combinations_with_replacement(self.bigcore_power,
                                                                    self.bigcore_num)]
            self.littlecore_powerlist = [list(i) for i in
                                         combinations_with_replacement(self.littlecore_power,
                                                                       self.littlecore_num)]
            for i in range(len(self.bigcore_powerlist)):
                for j in range(len(self.littlecore_powerlist)):
                    self.core_powerlist.append(list(self.bigcore_powerlist[i] +
                                                    self.littlecore_powerlist[j]))
            self.core_powerlist.reverse()
        elif option == 2:
            self.corepair_freq = self.bigcore_freq + self.littlecore_freq
            self.corepair_power = self.bigcore_power + self.littlecore_power
            self.core_freqlist = [list(i) for i in
                                  combinations_with_replacement(self.corepair_freq,
                                                                self.core_num)]
            self.core_freqlist.reverse()
            self.core_powerlist = [list(i) for i in
                                   combinations_with_replacement(self.corepair_power,
                                                                 self.core_num)]
            self.core_powerlist.reverse()

    def get_CoresetList(self):
        return self.core_freqlist, self.core_powerlist

    def get_CoresetFreqList(self):
        return self.core_freqlist

    def get_CoresetPowerList(self):
        return self.core_powerlist

    def get_CoresetCoreNum(self):
        return self.core_num

    def get_CoresetBigCoreNum(self):
        return self.bigcore_num

    def get_CoresetLittleCoreNum(self):
        return self.littlecore_num

    def delete_Coreset(self):
        self.core_freqlist = []
        self.core_powerlist = []

    def print_CoresetStatus(self):
        print("CoresetName: {0}" .format(self.name))
        print("biglittle_model: {0}, bigcore_num {1}, littlecore_num {2}"
              .format(self.biglittle_model, self.bigcore_num, self.littlecore_num))
        print("core_freqlist")
        print self.core_freqlist
        print("core_powerlist")
        print self.core_powerlist

    def print_CoresetName(self):
        print("CoresetName: {0}" .format(self.name))

#t = Coreset("coreset1")
#t.set_Coreset_Conf()
#t.create_Coresets()
#print t.get_Coreset_freq()
#t.print_Coreset_Status()
