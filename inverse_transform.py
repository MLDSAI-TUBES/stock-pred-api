class InverseTransform(object):
    def __init__(self, ticker, scalerClose):
        self.ticker = ticker
        self.scalerClose = scalerClose
    
    def inverseTransform(self, scaledClose):
        """
        Returns np array of inversed scaled close
        """
        try:
            inversed = self.scalerClose.inverse_transform(scaledClose)
            return inversed
        except:
            print('Error in inversing the transformed close price')
            