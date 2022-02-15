import os

import numpy as np
from decimal import Decimal


class Reporter:
    def __init__(self, abcList):
        self.abcList = abcList
        if abcList[0].conf.PRINT_PARAMETERS:
            self.print_parameters()

        if abcList[0].conf.RUN_INFO:
            self.run_info()
        if abcList[0].conf.SAVE_RESULTS:
            self.save_results()
        if abcList[0].conf.RUN_INFO_COMMANDLINE:
            self.command_line_print()

    def print_parameters(self):
        for i in range(self.abcList[0].conf.RUN_TIME):
            print(self.abcList[i].experimentID, ". run")
            for j in range(self.abcList[0].conf.DIMENSION):
                print("Global Param[", j + 1, "] ", self.abcList[i].globalParams[j])

    def run_info(self):
        summary = []
        write_text = "%s run: %s Cycle: %s Time: %s"
        for i in range(self.abcList[0].conf.RUN_TIME):
            print_text = write_text % (self.abcList[i].experimentID, self.abcList[i].globalOpt, self.abcList[i].cycle, self.abcList[i].globalTime)
            print(print_text)
            summary.append(self.abcList[i].globalOpt)
        print("Mean: ", np.mean(summary), " Std: ", np.std(summary), " Median: ", np.median(summary))

    def command_line_print(self):
        sum = []
        for i in range(self.abcList[0].conf.RUN_TIME):
            sum.append(self.abcList[i].globalOpt)
        print('%1.5E' % Decimal(np.mean(sum)))

    def save_results(self):
        output_folder = self.abcList[0].conf.OUTPUTS_FOLDER_NAME
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        header = "experimentID; Number of Population; Maximum Evaluation; Limit; Function; Dimension; Upper Bound; Lower Bound; Result; Time \n"
        csvText = "{}; {}; {}; {}; {}; {}; {}; {}; {}; {} \n"

        file_path = "%s/%s" % (output_folder, self.abcList[0].conf.RESULT_REPORT_FILE_NAME)
        with open(file_path, 'a') as saveRes:
            is_header = sum(1 for line in open(file_path)) < 1
            if is_header:
                saveRes.write(header)

            for i in range(self.abcList[0].conf.RUN_TIME):
                saveRes.write(csvText.format(
                    self.abcList[i].experimentID,
                    self.abcList[i].conf.NUMBER_OF_POPULATION,
                    self.abcList[i].conf.MAXIMUM_EVALUATION,
                    self.abcList[i].conf.LIMIT,
                    self.abcList[i].conf.OBJECTIVE_FUNCTION.__name__,
                    self.abcList[i].conf.DIMENSION,
                    self.abcList[i].conf.UPPER_BOUND,
                    self.abcList[i].conf.LOWER_BOUND,
                    self.abcList[i].globalOpt,
                    self.abcList[i].globalTime,
                ))

            header = "experimentID;"
            for j in range(self.abcList[0].conf.DIMENSION):

                if j < self.abcList[0].conf.DIMENSION - 1:
                    header = header + "param" + str(j) + ";"
                else:
                    header = header + "param" + str(j) + "\n"

            file_path = "%s/%s" % (output_folder, self.abcList[0].conf.PARAMETER_REPORT_FILE_NAME)

            with open(file_path, 'a') as saveRes:
                is_header = sum(1 for line in open(file_path)) < 1
                if is_header:
                    saveRes.write(header)

                for i in range(self.abcList[0].conf.RUN_TIME):
                    csv_text = str(self.abcList[i].experimentID) + ";"
                    for j in range(self.abcList[0].conf.DIMENSION):
                        if j < self.abcList[0].conf.DIMENSION - 1:
                            csv_text = "%s%s;" % (csv_text, str(self.abcList[i].globalParams[j]))
                        else:
                            csv_text = "%s%s \n" % (csv_text, str(self.abcList[i].globalParams[j]))
                    saveRes.write(csv_text)
            saveRes.close()

            for i in range(self.abcList[0].conf.RUN_TIME):
                folder_path = "%s/%s" % (output_folder, self.abcList[i].conf.RESULT_BY_CYCLE_FOLDER)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = "%s/%s.txt" % (folder_path, self.abcList[i].experimentID)
                with open(file_path, 'a') as saveRes:
                    for j in range(self.abcList[i].cycle):
                        saveRes.write(str(self.abcList[i].globalOpts[j]) + "\n")
