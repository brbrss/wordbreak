from inspect import signature


class Step:
    def __init__(self, name, f, kparams, output_name):
        self.name = name
        self.f = f
        self.kparams = kparams
        self.output_name = output_name

    def _validate(self):
        sig = signature(self.f)
        for k in sig.parameters.keys():
            if k not in self.kparams:
                err_msg = 'Parameter not found: ' + \
                    str(k)+' in function '+self.name
                raise RuntimeError(err_msg)
        pass

    def __call__(self, kargs):
        return self.f(**kargs)


class Pipeline:
    '''Class for running a pipeline of operations.
    Allows setting params and running from any position 
    in pipeline'''

    def __init__(self):
        self.L: list[Step] = []
        self.config = {}
        pass

    def add(self, name, f, params: dict[str, str], output_name=None):
        '''Register a function in pipeline

        Example: after registering

        `pipeline.add('foo',f,{'s':'greeting'})`

        Calling `pipeline._call(f)` will execute
        `f(s=pipeline.config['greeting'])`
        '''
        if output_name is None:
            output_name = name
        st = Step(name, f, params, output_name)
        self.L.append(st)
        return len(self.L)

    def set_config(self, d):
        '''Set parameters in pipeline'''
        self.config.update(d)

    def _call(self, st: Step):
        args = {t: self.config[st.kparams[t]] for t in st.kparams}
        res = st(args)
        self.config[st.output_name] = res
        return res

    def run_from(self, name):
        flag = False
        for st in self.L:
            if st.name == name:
                flag = True
            if flag:
                self._call(st)
        return

    def run_all(self):
        for st in self.L:
            self._call(st)
        return

    def run_one(self, name):
        for st in self.L:
            if st.name == name:
                self._call(st)
                return
        pass

    def name_list(self):
        '''list of name of steps'''
        return [st.name for st in self.L]

    def validate(self):
        ''' Validates that parameters are passed in config
        or `output_name`.
        Throws error if not found'''
        oset = {t.output_name for t in self.L}
        used = set()
        for t in self.L:
            for k in t.kparams:
                used.add(k)
                b = k in self.config or k in oset
                if not b:
                    err_msg = 'Parameter not found in config or output names. \n'
                    err_msg += 'In function '+t.name+' param ' + k
                    raise RuntimeError(err_msg)
        print('unused config', set(self.config.keys()).difference(used))
        return


def array_dict(arr):
    '''converts list of str to dict 
    such that key and val are the same'''
    return {s: s for s in arr}
