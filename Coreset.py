#! /usr/bin/python
# *-* encoding: utf-8 *-*

import config
from itertools import combinations_with_replacement


class Coreset:

    def __init__(self, name=""):
        self.name = name

    def set_Coreset_Conf(self, option=1):
        if option == 1:
            self.biglittle_model = 1
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.core_num = config.CORE_NUM
            self.bigcore_freq = config.BIGCORE_FREQ_HAS_SLEEP
            self.littlecore_freq = config.LITTLECORE_FREQ_HAS_SLEEP
            self.bigcore_power = config.BIGCORE_POWER_HAS_SLEEP
            self.littlecore_power = config.LITTLECORE_POWER_HAS_SLEEP
        elif option == 2:
            self.biglittle_model = 2
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.core_num = config.CORE_NUM
            self.bigcore_freq = config.BIGCORE_FREQ
            self.littlecore_freq = config.LITTLECORE_FREQ
            self.bigcore_power = config.BIGCORE_POWER
            self.littlecore_power = config.LITTLECORE_POWER
        elif option == 3:
            self.biglittle_model = 3
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.corepair_num = config.CORE_PAIR_NUM
            self.bigcore_freq = config.BIGCORE_FREQ_HAS_SLEEP
            self.littlecore_freq = config.LITTLECORE_FREQ_HAS_SLEEP
            self.bigcore_power = config.BIGCORE_POWER_HAS_SLEEP
            self.littlecore_power = config.LITTLECORE_POWER_HAS_SLEEP
        elif option == 4:
            self.biglittle_model = 4
            self.bigcore_num = config.BIGCORE_NUM
            self.littlecore_num = config.LITTLECORE_NUM
            self.corepair_num = config.CORE_PAIR_NUM
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

    def set_corepair_num(self, newvalue):
        self.corepair_num = newvalue

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
                                                                self.corepair_num)]
            self.core_freqlist.reverse()
            self.core_powerlist = [list(i) for i in
                                   combinations_with_replacement(self.corepair_power,
                                                                 self.corepair_num)]
            self.core_powerlist.reverse()

    def get_Coresetlist(self):
        return self.core_freqlist, self.core_powerlist

    def get_Coreset_freqlist(self):
        return self.core_freqlist

    def get_Coreset_powerlist(self):
        return self.core_powerlist

    def delete_Coreset(self):
        self.core_freqlist = []
        self.core_powerlist = []

    def print_Coreset_Status(self):
        print("Coresetname {0}" .format(self.name))
        print("biglittle_model:  {0}, bigcore_num {1} littlecore_num {2}"
              .format(self.biglittle_model, self.bigcore_num, self.littlecore_num))
        print("core_freqlist")
        print self.core_freqlist
        print("core_powerlist")
        print self.core_powerlist

    def print_Coresetname(self):
        print("Coresetname {0}" .format(self.name))

#t = Coreset("coreset1")
#t.set_Coreset_Conf()
#t.create_Coresets()
#print t.get_Coreset_freq()
#t.print_Coreset_Status()
