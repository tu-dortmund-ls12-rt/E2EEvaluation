from framework import *
import getopt

def replace_value(dict, key, new_value):
    old_value = dict[key]
    if new_value == '':
        dict[key] = True
        return
    if isinstance(old_value, int):
        dict[key] = int(new_value)
        return
    if isinstance(old_value, float):
        dict[key] = float(new_value)
        return
    raise ValueError('Could not parse value for', key)


def runCLIMode(args):

    # cli mode has two options:
    # 1. create cause-effect chains and store them in a file
    # 2. load cause-effect chains from a file and analyse them

    # get default parameters
    general_params = dict(default_general_params)
    taskset_generation_params = dict(default_taskset_generation_params)
    cec_generation_params = dict(default_cec_generation_params)
    selected_analysis_methods = []
    selected_normalization_methods = []
    output_params = dict(default_output_params)

    ##################
    #### Read args ###
    ##################

    if args[0] == 'generate-cecs':

        general_params['generate_cecs'] = True
        general_params['store_generated_cecs'] = True

        options, arguments = getopt.getopt(
            args[1:],
            "t:o:",
            [param + '=' for param in list(taskset_generation_params.keys()) if not isinstance(taskset_generation_params[param], bool)] + 
            [param for param in list(taskset_generation_params.keys()) if isinstance(taskset_generation_params[param], bool)] +
            [param + '=' for param in list(cec_generation_params.keys()) if not isinstance(cec_generation_params[param], bool)] + 
            [param for param in list(cec_generation_params.keys()) if isinstance(cec_generation_params[param], bool)] + 
            ['debug']
        )

        for option, value in options:
            option = option.replace('-', '')
            if option in taskset_generation_params.keys():
                replace_value(taskset_generation_params, option, value)
            if option in cec_generation_params.keys():
                replace_value(cec_generation_params, option, value)
            if option == 't':
                general_params['number_of_threads'] = int(value)
            if option == 'o':
                output_params['output_dir'] = value
            if option == 'debug':
                general_params['debug_output'] = True

    elif args[0] == 'analyze-cecs':

        general_params['load_cecs_from_file'] = True

        i = 1
        while i < len(args):

            if args[i] == '--normalized-plots':
                output_params['normalized_plots'] = True
                i+=1
                continue

            if args[i] == '--absolute-plots':
                output_params['absolute_plots'] = True
                i+=1
                continue

            if args[i] == '--csv-export':
                output_params['raw_analyses_results'] = True
                i+=1
                continue

            if args[i] == '--debug':
                general_params['debug_output'] = True
                i+=1
                continue

            if args[i] == '-a':
                # add analysis method
                if i+1 == len(args):
                    print("[ERROR] Missing argument after flag:", args[i])
                    print("[ERROR] Terminating")
                    return
                selected_analysis_methods.append(analysesDict[args[i+1]])
                i+=2
            elif args[i] == '-n':
                # add normalization method
                if i+1 == len(args):
                    print("[ERROR] Missing argument after flag:", args[i])
                    print("[ERROR] Terminating")
                    return
                selected_normalization_methods.append(analysesDict[args[i+1]])
                i+=2
            elif args[i] == '-f':
                # use specified file
                if i+1 == len(args):
                    print("[ERROR] Missing argument after flag:", args[i])
                    print("[ERROR] Terminating")
                    return
                general_params['cecs_file_path'] = args[i+1]
                i+=2
            elif args[i] == '-t':
                # use specified file
                if i+1 == len(args):
                    print("[ERROR] Missing argument after flag:", args[i])
                    print("[ERROR] Terminating")
                    return
                general_params['number_of_threads'] = int(args[i+1])
                i+=2
            else:
                # unknown option
                print("[ERROR] Passed unknown option:", args[i])
                print("[ERROR] Terminating")
                return

    elif len(args) == 2 or len(args) == 3:
        # simplest mode
        # first argument is the analysis method
        # second argument is the file to analyze
        # (optional) third argument is the number of threads

        general_params['load_cecs_from_file'] = True
        general_params['cecs_file_path'] = args[1]
        general_params['number_of_threads'] = int(args[2]) if len(args) == 3 else 1
        output_params['print_to_console'] = True
        selected_analysis_methods.append(analysesDict[args[0]])

    else:
        print('[ERROR] Could not parse input parameters')
        return
    

    ################################
    ### Run Evaluation Framework ###
    ################################

    # Debug Output
    if general_params['debug_output']:
        print('[Info] general params:', general_params)
        print('[Info] taskset_generation_params:', taskset_generation_params)
        print('[Info] cec_generation_params:', cec_generation_params)
        print('[Info] selected analysis methods:', selected_analysis_methods)
        print('[Info] selected normalization methods:', selected_normalization_methods)
        print('[Info] output params:', output_params)

    run_evaluation(
        general_params,
        taskset_generation_params,
        cec_generation_params,
        selected_analysis_methods,
        selected_normalization_methods,
        output_params
    )

    # Debug Output
    if general_params['debug_output']:
        print('[Info] Run finished without any errors')
        print('[Info] Results are saved in:', output_params['output_dir'])
        



