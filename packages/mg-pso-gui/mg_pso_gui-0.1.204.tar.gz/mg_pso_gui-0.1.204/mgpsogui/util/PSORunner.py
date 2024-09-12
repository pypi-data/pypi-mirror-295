
import sys
from multiprocessing import Process, Queue
from queue import Empty
import threading
import time
import os
from .recosu.sampling.sampling import run_sampler
from .recosu.pso import global_best
from csip import Client
import traceback
import urllib
import shutil
import json

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def run_process(stdout_queue, stderr_queue, results_queue, data, folder):
    steps = data['steps']
    args = data['arguments']
    calib = data['calibration_parameters']
    
    my_mode = args["mode"]

    # If "mode" in args remove it
    if "mode" in args:
        del args["mode"]
    
    calibration_map = {}
    for param in calib:
        param_name = param['name']
        param_value = param['value']
        calibration_map[param_name] = param_value
        
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(os.path.join(folder, "results")):
        os.makedirs(os.path.join(folder, "results"))

    if (os.path.exists(os.path.join(folder, 'output.txt'))):
        os.remove(os.path.join(folder, 'output.txt'))
        
    if (os.path.exists(os.path.join(folder, 'error.txt'))):
        os.remove(os.path.join(folder, 'error.txt'))
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    read_stdout, write_stdout = os.pipe()
    read_stderr, write_stderr = os.pipe()
    
    sys.stdout = os.fdopen(write_stdout, 'w')
    sys.stderr = os.fdopen(write_stderr, 'w')
    
    stdout_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stdout, 'r'), stdout_queue))
    stderr_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stderr, 'r'), stderr_queue))
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()
    
    try:
        
        options = {}
        oh_strategy = {}
        
        for key in calibration_map.keys():
            if "options_" in key:
                options[key.replace("options_", "")] = float(calibration_map[key])
            if "strategy_" in key:
                oh_strategy[key.replace("strategy_", "")] = calibration_map[key]

        config = {}

        if my_mode == "Sampling: Halton" or my_mode == "Sampling: Random":
            config = {
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'conn_timeout': int(calibration_map['conn_timeout']),
                'read_timeout': int(calibration_map['read_timeout']),
                'step_trace': os.path.join(folder, 'pso_step_trace.json')
            }
        elif my_mode == "Optimization: MG-PSO":
            config = {
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'http_allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'http_conn_timeout': int(calibration_map['conn_timeout']),
                'http_read_timeout': int(calibration_map['read_timeout']),
                'particles_fail': int(calibration_map['particles_fail']),
                'step_trace': os.path.join(folder, 'pso_step_trace.json')
            }

        print("\n")
        print(steps)
        print("\n")
        print(args)
        print("\n")
        print(calibration_map)
        print("\n")
        print(options)
        print("\n")
        print(oh_strategy)
        print("\n")
        print(config)
        print("\n", flush=True)

        if my_mode == "Sampling: Halton":
            print("Running Halton Sampling..\n", flush=True)
            trace = run_sampler(steps, 
                                args, 
                                int(calibration_map['count']), 
                                int(calibration_map['num_threads']), 
                                "halton", 
                                conf=config, 
                                trace_file=os.path.join(folder, 'results', 'halton_trace.csv'),
                                offset=int(calibration_map['offset']))
            results_queue.put(trace)
            print(trace, flush=True)
            print("\n", flush=True)
            
        elif my_mode == "Sampling: Random":
            print("Running Random Sampling...\n", flush=True)
            trace = run_sampler(steps, 
                    args, 
                    int(calibration_map['count']), 
                    int(calibration_map['num_threads']), 
                    "random", 
                    conf=config, 
                    trace_file=os.path.join(folder, 'results', 'random_trace.csv'))
            results_queue.put(trace)
            print(trace, flush=True)
            print("\n", flush=True)

        elif my_mode == "Sensitivity: Halton":
            
            print("Running Halton Sensitivity Analysis", flush=True)

            shutil.copyfile(os.path.join(folder, 'results', 'halton_trace.csv'), os.path.join(folder, 'results', 'trace.csv'))
            trace_path = os.path.join(folder, 'results', 'trace.csv')

            # Get list of parameters from steps
            parameters = []
            for param in steps[0]['param']:
                parameters.append(param['name'])

            request_json = {
                "metainfo": {
                    "service_url": None,
                    "description": "",
                    "name": "",
                    "mode": "async"
                },
                "parameter": [
                    {
                    "name": "parameters",
                    "value": parameters
                    },
                    {
                    "name": "positiveBestMetrics",
                    "value": ["ns","kge","mns","kge09","nslog2"]
                    },
                    {
                    "name": "zeroBestMetrics",
                    "value": ["pbias","rmse"]
                    }
                ]
            }
            
            with open(os.path.join(folder, 'results', 'request.json'), 'w') as json_file:
                json.dump(request_json, json_file, indent=4)
            
            request_path = os.path.join(folder, 'results', 'request.json')

            output_directory = os.path.join(folder, 'results')

            print("Starting ", args['url'], request_path, trace_path, output_directory, flush=True)

            sensitivity_analysis(args['url'], request_path, trace_path, output_directory)

            print("Finished Sensitivity Analysis", flush=True)
        elif my_mode == "Sensitivity: Random":
            
            print("Running Random Sensitivity Analysis", flush=True)

            shutil.copyfile(os.path.join(folder, 'results', 'random_trace.csv'), os.path.join(folder, 'results', 'trace.csv'))
            trace_path = os.path.join(folder, 'results', 'trace.csv')
            
            # Get list of parameters from steps
            parameters = []
            for param in steps[0]['param']:
                parameters.append(param['name'])

            request_json = {
                "metainfo": {
                    "service_url": None,
                    "description": "",
                    "name": "",
                    "mode": "async"
                },
                "parameter": [
                    {
                    "name": "parameters",
                    "value": parameters
                    },
                    {
                    "name": "positiveBestMetrics",
                    "value": ["ns","kge","mns","kge09","nslog2"]
                    },
                    {
                    "name": "zeroBestMetrics",
                    "value": ["pbias","rmse"]
                    }
                ]
            }
            
            with open(os.path.join(folder, 'results', 'request.json'), 'w') as json_file:
                json.dump(request_json, json_file, indent=4)

            request_path = os.path.join(folder, 'results', 'request.json')

            output_directory = os.path.join(folder, 'results')

            print("Starting ", args['url'], request_path, trace_path, output_directory, flush=True)

            sensitivity_analysis(args['url'], request_path, trace_path, output_directory)

            print("Finished Sensitivity Analysis", flush=True)
        else:
            print("Running MG-PSO Optimization...\n", flush=True)
            optimizer, trace = global_best(steps,   
                    rounds=(int(calibration_map['min_rounds']), int(calibration_map['max_rounds'])),              
                    args=args,      
                    n_particles=int(calibration_map['n_particles']),      
                    iters=int(calibration_map['iters']),  
                    n_threads=int(calibration_map['n_threads']),      
                    options=options,
                    oh_strategy=oh_strategy, 
                    conf=config
                )
            
            results_queue.put(trace)
            print(trace, flush=True)
        
        print("Finishing up...", flush=True)
        time.sleep(5)
    except Exception as e:
        print("An exception occurred: ", flush=True)
        print(str(e))
        # Print stack trace
        import traceback
        traceback.print_exc()

        # Write all of this information to a crash file
        with open(os.path.join(folder, 'crash.txt'), 'w') as f:
            f.write(str(e))
            f.write("\n")
            traceback.print_exc(file=f)
    finally:
        stdout_thread.join()
        stderr_thread.join()
        
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def create_request(request_file: str) -> Client:
    request: Client = Client.from_file(request_file)
    return request

def download_output(response: Client, target_directory) -> None:
    data_names: list[str] = response.get_data_names()
    for name in data_names:
        url = response.get_data_value(name)
        file_path = os.path.join(target_directory, name)
        urllib.request.urlretrieve(url, file_path)

def sensitivity_analysis(url, request_file, trace_file, output_directory):
    request: Client = create_request(request_file)
    files: list[str] = [trace_file] if os.path.isfile(trace_file) else []
    conf = {
        'service_timeout': 60.0,  # (sec)
    }
    result: Client = Client()
    try:
        result = request.execute(url, files=files, sync=True, conf=conf)
    except Exception as ex:
        traceback.print_exc()
        exit(1)

    if result.is_finished():
        download_output(result, output_directory)