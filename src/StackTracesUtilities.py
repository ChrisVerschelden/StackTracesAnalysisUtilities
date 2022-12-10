from colors import colored_background, colored_text, print_result, print_error, print_warning, print_status, print_success
import os 
import sys
import csv

class StackTracesUtilities:
    def __init__(self):
        self.SOURCE = ""
        self.WORK_FILE = ""
        self.create_tmp_file = False
        self.update_tmp_file = False
        self.NB_FILLERS = 0
        self.NB_SPACE = 20
        self.nb_rows = 0
        self.all_rows = []
        self.header = []  
        self.stacktraceIdHeader = "" 
        self.header_index_of_stacktraceID = 0   

    def get_nb_rows(self):
        return self.nb_rows
    
    def get_header(self):
        return self.header

    def waiting_indicator(self, nb_stacktrace_total, nb_stacktrace_anoma,filler='#'):
        sys.stdout.flush()
        sys.stdout.write("[\033[%s] current stacktrace: %i | stacktraces containing anomalies: %i\r" % (colored_text(self.NB_FILLERS*"#" + self.NB_SPACE*' ', 'green'), nb_stacktrace_total, nb_stacktrace_anoma+1) )
        
        self.NB_FILLERS += 1
        self.NB_SPACE -= 1
        if self.NB_SPACE == 0:
            self.NB_FILLERS = 0
            self.NB_SPACE = 20

    def satisfy_all_params(self, row, params):
        """
        check if the row from a csv satisfy the parameters of a request

        arguments:
        row -- a list of strings representing a row of cells from a csv file 
        header -- a list of string representing the header of a csv file
        params -- a list of tuples of the form (Header, Value) where Header is the name of a column of the csv file 
                  and Value the content of the cell
        """
        satisfy = True
        for param, value in params:
            if param not in self.header:
                print_error("%s his not a valid header for the current data" % param)
                
            if row[self.header.index(param)] != value:
                satisfy = False

        return satisfy

    def F(self, params):
        if self.nb_rows == 0:
            print_error("you haven't loaded any data yet")
            
        for row in self.all_rows:
            if self.satisfy_all_params(row, params):
                print_result('first record matching your request :')
                print_result(' '.join(row))
                break

    def P_F_by_stacktrace(self, stacktraceIdHeader, params, display_anomaly=False):
        if self.nb_rows == 0:
            print_error("you need to load data and sort it by stacktraces before running this command")
            return

        #initialise loop and stats variables
        nb_rows_passed = 0
        nb_stacktrace_anoma = 0
        nb_stacktrace_total = 0
        stacktraceID_current = ""
        anomaly_found = False
        self.header_index_of_stacktraceID = self.header.index(stacktraceIdHeader)

        #passing through all stacktraces (determined by stacktraceID)
        print_status("proccessing your request...")
        for row in self.all_rows:

            #initialise current stacktraceID on first iteration
            if stacktraceID_current == "":
                nb_stacktrace_total += 1
                stacktraceID_current = row[self.header_index_of_stacktraceID]

            #change stacktraceID on stacktrace change
            if row[self.header_index_of_stacktraceID] != stacktraceID_current:
                self.waiting_indicator(nb_stacktrace_total, nb_stacktrace_anoma)
                stacktraceID_current  = row[self.header_index_of_stacktraceID]
                nb_stacktrace_total += 1
                anomaly_found = False
            
            #find the first row (if it exists) that matches the params in the current stacktrace 
            #and set state as found to skip rows until the next stacktrace 
            if (not anomaly_found) and row[self.header_index_of_stacktraceID] == stacktraceID_current and self.satisfy_all_params(row, params):
                nb_stacktrace_anoma += 1
                anomaly_found = True
                if display_anomaly:
                    print_status(stacktraceID_current)                

        print_result("\n%i%s (%i out of %i) of stacktraces match your request : %s \n" % ((nb_stacktrace_anoma*100)/nb_stacktrace_total, '%', nb_stacktrace_anoma, nb_stacktrace_total, ' && '.join([h+':'+v for h, v in params])))

    def load_data(self, source, refresh=True):
        if not os.path.isfile(source) or source.split('.')[-1:][0] != "csv":
            print_error("%s is not a valid file" % source)
            return

        #store relative path of data file and the eventual work file
        self.SOURCE = source
        self.WORK_FILE = './work_files/' + self.SOURCE.split('/')[-1:][0]
        
        #if user doesn't want to reload the original data and a corresponding workfile exist then load workfile data
        if (not refresh) and os.path.isfile(self.WORK_FILE):
            self.load_data_from_work_file()
            return

        #if user ask to load work file but file doesn't exist
        if not refresh:
            print_warning("no corresponding work file, loading %s instead. /!\ data will not be sorted automaticaly" % (self.SOURCE))

        #if user want to load or reload data 
        with open(self.SOURCE, newline='\n', encoding='UTF8') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            #get the header
            self.header = next(reader)
            print_status("loading data from %s..." % (self.SOURCE))
            self.all_rows = list(reader)
            self.nb_rows = len(self.all_rows)
            print_success("finished loading")

    def load_data_from_work_file(self):
        if not os.path.isfile(self.WORK_FILE): 
            print_error("file doesn't exist")
            return

        with open(self.WORK_FILE, newline='\n', encoding='UTF8') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            
            #get the header
            self.header = next(reader)

            print_status("loading data from corresponding work file %s..." % (self.WORK_FILE))
            self.all_rows = list(reader)
            self.nb_rows = len(self.all_rows)
            print_success('finished loading')

    def sort_data(self, stacktraceIdHeader):
        if self.nb_rows == 0:
            print_error("you haven't loaded any data yet")
            return
        if stacktraceIdHeader not in self.header:
            print_error("header doesn't exist in the provided data")
            return

        print_status('sorting rows...')
        #get the index of the stacktraceIdHeader in the row
        self.header_index_of_stacktraceID = self.header.index(stacktraceIdHeader)
        self.all_rows.sort(key = lambda x: x[self.header_index_of_stacktraceID])
        print_success('finished sort')

    def create_work_file(self):
        if self.nb_rows == 0:
            print_error('you have no data to store in a work file')

        if not os.path.exists('./work_files'):
            os.mkdir('./work_files')

        self.delete_work_file()

        print_status('creating work file...')
        with open(self.WORK_FILE, newline='\n', mode='w', encoding='UTF8') as file_out:
            writer = csv.writer(file_out,delimiter=',')
            writer.writerow(self.header)
            for row in self.all_rows:
                writer.writerow(row)
        print_success('work file created')

    def delete_work_file(self):
        if not os.path.isfile(self.WORK_FILE) : return

        print_status('deleting old work file...')
        os.remove(self.WORK_FILE)
        print_success('old work file deleted')


          
