# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:28:19 2024

@author: Ju Feng (jufen@dtu.dk)
"""


import numpy as np
try:
    import matlab.engine as engine
except ImportError:
    print('Warning: Matlab engine is not imported!')



class Model(object):
    def __init__(self, func=None, input_arg_keys=['x'], output_arg_keys=['y'], 
                 parameters_dict=None, name='unnamed', info=None):
        if func is not None:
            self.func=func
        self.input_arg_keys = input_arg_keys
        self.output_arg_keys = output_arg_keys
        self.parameters_dict = parameters_dict
        self.name = name
        self.info = info

        self.num_args_input = len(self.input_arg_keys)
        self.num_args_output = len(self.output_arg_keys)

        self.history_records = []
        self.num_eval = 0


    def evaluate(self, input_dict, recording=True):
        output_dict = self.func(input_dict)

        if recording:
            self.record_current_run(input_dict, output_dict)
        return output_dict
    

    def record_current_run(self, input_dict, ouput_dict):
        self.history_records.append([input_dict, ouput_dict])
        self.num_eval = self.num_eval + 1

    
    def clean_history_records(self):
        self.history_records = []
        self.num_eval = 0
        
    
    
class Adapter(Model):
    def __init__(self, func=None, input_arg_keys=['x'], output_arg_keys=None,
                 parameters_dict=None, name='adapter_unnamed', info=None):
        
        if func is None:
            def func(input_dict):
                output_dict = input_dict.copy()
                return output_dict
        
        if output_arg_keys is None:
            output_arg_keys = input_arg_keys.copy()
        super().__init__(func, input_arg_keys, output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
        

class ModelMatlab(Model):
    def __init__(self, matlab_func_name, matlab_func_folder=None, eng=None, 
                 input_arg_keys=['x'], output_arg_keys=['y'],
                 parameters_dict=None, name='matlab_model_unnamed', info=None):
        
        super().__init__(func=None, input_arg_keys=input_arg_keys, 
                         output_arg_keys=output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
        self.matlab_func_name = matlab_func_name
        self.matlab_func_folder = matlab_func_folder

        if eng is None:
            eng = engine.start_matlab()
        self.eng = eng

        if self.matlab_func_folder is not None:
            s = eng.genpath(self.matlab_func_folder)
            eng.addpath(s, nargout=0)

    
    def func(self, input_dict):
        args2matlab = []

        for key in self.input_arg_keys:
            if key not in input_dict.keys():
                raise ValueError(f'Error: {key} is in the defined ' +
                                 'input_arg_keys, but not provided!')
            args2matlab.append(input_dict[key])
        #print(in_args_dict)
        
        res = eval(f'self.eng.{self.matlab_fun_name}' + '(*tuple(args2matlab), ' +
                   'nargout=self.num_args_out)')

        output_dict = {}
        for i in range(self.num_args_out):
            res_i = np.array(res[i])
            
            output_dict[self.output_arg_keys[i]] = res_i

        return output_dict





if __name__ == '__main__':

    def square(x):
        y = x**2
        return y
    
    def square_decorated(input_dict):
        x = input_dict['x']
        y = square(x)
        output_dict = {'y': y}
        return output_dict
    
    model_square = Model(func=square_decorated,
                         input_arg_keys=['x'],
                         output_arg_keys=['y'],
                         parameters_dict=None)
    





        
    



