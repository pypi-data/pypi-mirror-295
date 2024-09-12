class Howe:
    def __init__(self, *args):
        self._args = [iter(x) for x in args]

    def __iter__(self):
        return self

    def __next__(self):
        elements = list()
        errors = list()
        for arg in self._args:
            try:
                element = next(arg)
            except StopIteration as error:
                errors.append(error)
            else:
                elements.append(element)
        if not len(errors):
            return tuple(elements)
        if len(elements):
            raise ExceptionGroup("Howe failed.", errors)
        raise StopIteration
