__author__ = "Omur Sahin"

import sys
import numpy as np
from deap.benchmarks import *
import progressbar

class ABC:

    def __init__(_self, conf):
        _self.conf = conf
        _self.foods = np.zeros((_self.conf.FOOD_NUMBER, _self.conf.DIMENSION))
        _self.f = np.ones((_self.conf.FOOD_NUMBER))
        _self.fitness = np.ones((_self.conf.FOOD_NUMBER)) * np.iinfo(int).max
        _self.trial = np.zeros((_self.conf.FOOD_NUMBER))
        _self.prob = [0 for x in range(_self.conf.FOOD_NUMBER)]
        _self.solution = np.zeros((_self.conf.DIMENSION))
        _self.globalParams = [0 for x in range(_self.conf.DIMENSION)]
        _self.globalTime = 0
        _self.evalCount = 0
        _self.cycle = 0
        _self.experimentID = 0
        _self.globalOpts = list()

        if (_self.conf.SHOW_PROGRESS):
            _self.progressbar = progressbar.ProgressBar(max_value=_self.conf.MAXIMUM_EVALUATION)
        if (not(conf.RANDOM_SEED)):
            random.seed(conf.SEED)

    def calculate_function(_self, sol):
        try:
            if (_self.conf.SHOW_PROGRESS):
                _self.progressbar.update(_self.evalCount)
            return _self.conf.OBJECTIVE_FUNCTION(sol)

        except ValueError as err:
            print(
                "An exception occured: Upper and Lower Bounds might be wrong. (" + str(err) + " in calculate_function)")
            sys.exit()

    def calculate_fitness(_self, fun):
        _self.increase_eval()
        if fun >= 0:
            result = 1 / (fun + 1)
        else:
            result = 1 + abs(fun)
        return result

    def increase_eval(_self):
        _self.evalCount += 1

    def stopping_condition(_self):
        status = bool(_self.evalCount >= _self.conf.MAXIMUM_EVALUATION)
        if(_self.conf.SHOW_PROGRESS):
          if(status == True and not( _self.progressbar._finished )):
               _self.progressbar.finish()
        return status

    def memorize_best_source(_self):
        for i in range(_self.conf.FOOD_NUMBER):
            if (_self.f[i] < _self.globalOpt and _self.conf.MINIMIZE == True) or (_self.f[i] >= _self.globalOpt and _self.conf.MINIMIZE == False):
                _self.globalOpt = np.copy(_self.f[i])
                _self.globalParams = np.copy(_self.foods[i][:])

    def init(_self, index):
        if (not (_self.stopping_condition())):
            for i in range(_self.conf.DIMENSION):
                _self.foods[index][i] = random.random() * (_self.conf.UPPER_BOUND - _self.conf.LOWER_BOUND) + _self.conf.LOWER_BOUND
            _self.solution = np.copy(_self.foods[index][:])
            _self.f[index] = _self.calculate_function(_self.solution)[0]
            _self.fitness[index] = _self.calculate_fitness(_self.f[index])
            _self.trial[index] = 0

    def initial(_self):
        for i in range(_self.conf.FOOD_NUMBER):
            _self.init(i)
        _self.globalOpt = np.copy(_self.f[0])
        _self.globalParams = np.copy(_self.foods[0][:])

    def send_employed_bees(_self):
        i = 0
        while (i < _self.conf.FOOD_NUMBER) and (not (_self.stopping_condition())):
            r = random.random()
            _self.param2change = (int)(r * _self.conf.DIMENSION)

            r = random.random()
            _self.neighbour = (int)(r * _self.conf.FOOD_NUMBER)
            while _self.neighbour == i:
                r = random.random()
                _self.neighbour = (int)(r * _self.conf.FOOD_NUMBER)
            _self.solution = np.copy(_self.foods[i][:])

            r = random.random()
            _self.solution[_self.param2change] = _self.foods[i][_self.param2change] + (
                        _self.foods[i][_self.param2change] - _self.foods[_self.neighbour][_self.param2change]) * (
                                                             r - 0.5) * 2

            if _self.solution[_self.param2change] < _self.conf.LOWER_BOUND:
                _self.solution[_self.param2change] = _self.conf.LOWER_BOUND
            if _self.solution[_self.param2change] > _self.conf.UPPER_BOUND:
                _self.solution[_self.param2change] = _self.conf.UPPER_BOUND
            _self.ObjValSol = _self.calculate_function(_self.solution)[0]
            _self.FitnessSol = _self.calculate_fitness(_self.ObjValSol)
            if (_self.FitnessSol > _self.fitness[i] and _self.conf.MINIMIZE == True) or (_self.FitnessSol <= _self.fitness[i] and _self.conf.MINIMIZE == False):
                _self.trial[i] = 0
                _self.foods[i][:] = np.copy(_self.solution)
                _self.f[i] = _self.ObjValSol
                _self.fitness[i] = _self.FitnessSol
            else:
                _self.trial[i] = _self.trial[i] + 1
            i += 1

    def calculate_probabilities(_self):
        maxfit = np.copy(max(_self.fitness))
        for i in range(_self.conf.FOOD_NUMBER):
            _self.prob[i] = (0.9 * (_self.fitness[i] / maxfit)) + 0.1

    def send_onlooker_bees(_self):
        i = 0
        t = 0
        while (t < _self.conf.FOOD_NUMBER) and (not (_self.stopping_condition())):
            r = random.random()
            if ((r < _self.prob[i] and _self.conf.MINIMIZE == True) or (r > _self.prob[i] and _self.conf.MINIMIZE == False)):
                t+=1
                r = random.random()
                _self.param2change = (int)(r * _self.conf.DIMENSION)
                r = random.random()
                _self.neighbour = (int)(r * _self.conf.FOOD_NUMBER)
                while _self.neighbour == i:
                    r = random.random()
                    _self.neighbour = (int)(r * _self.conf.FOOD_NUMBER)
                _self.solution = np.copy(_self.foods[i][:])

                r = random.random()
                _self.solution[_self.param2change] = _self.foods[i][_self.param2change] + (
                            _self.foods[i][_self.param2change] - _self.foods[_self.neighbour][_self.param2change]) * (
                                                                 r - 0.5) * 2
                if _self.solution[_self.param2change] < _self.conf.LOWER_BOUND:
                    _self.solution[_self.param2change] = _self.conf.LOWER_BOUND
                if _self.solution[_self.param2change] > _self.conf.UPPER_BOUND:
                    _self.solution[_self.param2change] = _self.conf.UPPER_BOUND

                _self.ObjValSol = _self.calculate_function(_self.solution)[0]
                _self.FitnessSol = _self.calculate_fitness(_self.ObjValSol)
                if (_self.FitnessSol > _self.fitness[i] and _self.conf.MINIMIZE == True) or (_self.FitnessSol <= _self.fitness[i] and _self.conf.MINIMIZE == False):
                    _self.trial[i] = 0
                    _self.foods[i][:] = np.copy(_self.solution)
                    _self.f[i] = _self.ObjValSol
                    _self.fitness[i] = _self.FitnessSol
                else:
                    _self.trial[i] = _self.trial[i] + 1
            i += 1
            i = i % _self.conf.FOOD_NUMBER

    def send_scout_bees(_self):
        if np.amax(_self.trial) >= _self.conf.LIMIT:
            _self.init(_self.trial.argmax(axis = 0))

    def increase_cycle(_self):
        _self.globalOpts.append(_self.globalOpt)
        _self.cycle += 1
    def setExperimentID(_self,run,t):
        _self.experimentID = t+"-"+str(run)
