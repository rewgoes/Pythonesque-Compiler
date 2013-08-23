__author__ = 'Matheus'


class Token:

    def __init__(self, name, category, bad=None):
        """

        :param name:
        :param category:
        """
        self.name = name
        self.category = category
        if bad is None:
            self.bad = False
        else:
            self.bad = bad