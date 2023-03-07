import sys
import getopt
import configparser
from deap.benchmarks import sphere, rastrigin, schwefel, rosenbrock, ackley, rand, plane, cigar, h1, himmelblau, schaffer, griewank, rastrigin_scaled, rastrigin_skew, bohachevsky
import os


class Config:

    def __init__(self, argv):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + '/ABC.ini')
        # ####SETTINGS FILE######
        self.OBJECTIVE_FUNCTION = self.objFunctionSelector.get(config['DEFAULT']['ObjectiveFunction'], "Error")
        self.NUMBER_OF_POPULATION = int(config['DEFAULT']['NumberOfPopulation'])
        self.MAXIMUM_EVALUATION = int(config['DEFAULT']['MaximumEvaluation'])
        self.LIMIT = int(config['DEFAULT']['Limit'])
        self.FOOD_NUMBER = int(self.NUMBER_OF_POPULATION / 2)
        self.DIMENSION = int(config['DEFAULT']['Dimension'])
        self.UPPER_BOUND = float(config['DEFAULT']['UpperBound'])
        self.LOWER_BOUND = float(config['DEFAULT']['LowerBound'])
        self.RUN_TIME = int(config['DEFAULT']['RunTime'])
        self.SHOW_PROGRESS = bool(config['REPORT']['ShowProgress'] == 'True')
        self.PRINT_PARAMETERS = bool(config['REPORT']['PrintParameters'] == 'True')
        self.RUN_INFO = bool(config['REPORT']['RunInfo'] == 'True')
        self.RUN_INFO_COMMANDLINE = bool(config['REPORT']['CommandLine'] == 'True')
        self.SAVE_RESULTS = bool(config['REPORT']['SaveResults'] == 'True')
        self.RESULT_REPORT_FILE_NAME = config['REPORT']['ResultReportFileName']
        self.PARAMETER_REPORT_FILE_NAME = config['REPORT']['ParameterReportFileName']
        self.RESULT_BY_CYCLE_FOLDER = config['REPORT']['ResultByCycleFolder']
        self.OUTPUTS_FOLDER_NAME = str(config['REPORT']['OutputsFolderName'])
        self.RANDOM_SEED = config['SEED']['RandomSeed'] == 'True'
        self.SEED = int(config['SEED']['Seed'])
        # ####SETTINGS FILE######

        # ####SETTINGS ARGUMENTS######
        try:
            opts, args = getopt.getopt(argv, 'hn:m:t:d:l:u:r:o:',
                                       ['help', 'np=', 'max_eval=', 'trial=', 'dim=', 'lower_bound=', 'upper_bound=', 'runtime=',
                                        'obj_fun=', 'output_folder=', 'file_name=', 'param_name=', 'res_cycle_folder=', 'show_functions'])
        except getopt.GetoptError:
            print('Usage: ABCAlgorithm.py -h or --help')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('-h or --help : Show Usage')
                print('-n or --np : Number of Population')
                print('-m or --max_eval : Maximum Evaluation')
                # print('-t or --trial : Maximum Trial')
                print('-d or --dim : Dimension')
                print('-l or --lower_bound : Lower Bound')
                print('-u or --upper_bound : Upper Bound')
                print('-r or --runtime : Run Time')
                print('-o or --obj_fun : Objective Function')
                print('--show_functions : Show Objective Functions')
                print('--output_folder= [DEFAULT: Outputs]')
                print('--file_name= [DEFAULT: Run_Results.csv]')
                print('--param_name= [DEFAULT: Param_Results.csv]')
                print('--res_cycle_folder= [DEFAULT: ResultByCycle]')

                sys.exit()
            elif opt in ('-n', '--np'):
                self.NUMBER_OF_POPULATION = int(arg)
            elif opt in ('-m', '--max_eval'):
                self.MAXIMUM_EVALUATION = int(arg)
            elif opt in ('-d', '--dim'):
                self.DIMENSION = int(arg)
            elif opt in ('-t', '--trial'):
                self.LIMIT = int(arg)
            elif opt in ('-l', '--lower_bound'):
                self.LOWER_BOUND = float(arg)
            elif opt in ('-u', '--upper_bound'):
                self.UPPER_BOUND = float(arg)
            elif opt in ('-r', '--runtime'):
                self.RUN_TIME = int(arg)
            elif opt in ('-o', '--obj_fun'):
                self.OBJECTIVE_FUNCTION = self.objFunctionSelector.get(arg, "sphere")
            elif opt in ('--output_folder'):
                self.OUTPUTS_FOLDER_NAME = arg
            elif opt in ('--param_name'):
                self.PARAMETER_REPORT_FILE_NAME = arg
            elif opt in ('--file_name'):
                self.RESULT_REPORT_FILE_NAME = arg
            elif opt in ('--res_cycle_folder'):
                self.RESULT_BY_CYCLE_FOLDER = arg
            elif opt in ('--show_functions'):
                print("We use deap.benchmarks functions. Available functions are listed below:")
                for i in self.objFunctionSelector:
                    print(i)
                sys.exit()
        # ####SETTINGS ARGUMENTS######

    def user_defined_function(individual):
        return (individual[0] - individual[1]),

    # ######FUNCTION_LIST######
    objFunctionSelector = {
        'sphere': sphere,
        'rastrigin': rastrigin,
        'rosenbrock': rosenbrock,
        'rand': rand,
        'plane': plane,
        'cigar': cigar,
        'h1': h1,
        'ackley': ackley,
        'bohachevsky': bohachevsky,
        'griewank': griewank,
        'rastrigin_scaled': rastrigin_scaled,
        'rastrigin_skew': rastrigin_skew,
        'schaffer': schaffer,
        'schwefel': schwefel,
        'himmelblau': himmelblau,
        'user_defined': user_defined_function
    }
    # ######FUNCTION_LIST######
