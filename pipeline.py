
class Step:
    def __init__(self, name, f, kparams, output_name):
        self.name = name
        self.f = f
        self.kparams = kparams
        self.output_name = output_name

    def __call__(self, kargs):
        return self.f(**kargs)


class Pipeline:
    '''Class for running a pipeline of operations.
    Allows setting params and running from any position 
    in pipeline'''

    def __init__(self):
        self.L = []
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
        return st(args)

    def run_from(self, name):
        flag = False
        for st in self.L:
            if st.name == name:
                flag = True
            if flag:
                res = self._call(st)
                self.config[st.output_name] = res
        return

    def run_one(self, name):
        for st in self.L:
            if st.name == name:
                res = self._call(st)
                self.config[st.output_name] = res
                return
        pass
