__author__ = 'Bruno_Matheus_Rafael_Thiago'


class Token:
    # Constructor
    def __init__(self, name, token, bad=None):
        """

        :param name:
        :param token:
        """
        self.name = name
        self.token = token
        if bad is None:
            self.bad = False
        else:
            self.bad = bad