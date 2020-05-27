import datetime
import sys
import time
import ABC
import Config
from Reporter import Reporter


def main(argv):

    abcConf = Config.Config(argv)
    abcList = list()
    expT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(" ","").replace(":","")
    for run in range(abcConf.RUN_TIME):

        abc = ABC.ABC(abcConf)
        abc.setExperimentID(run,expT)
        start_time = time.time() * 1000
        abc.initial()
        abc.memorize_best_source()
        while(not(abc.stopping_condition())):
            abc.send_employed_bees()
            abc.calculate_probabilities()
            abc.send_onlooker_bees()
            abc.memorize_best_source()
            abc.send_scout_bees()
            abc.increase_cycle()

        abc.globalTime = time.time() * 1000 - start_time
        abcList.append(abc)
    Reporter(abcList)


if __name__ == '__main__':
    main(sys.argv[1:])
