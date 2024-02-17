class InvalidAccountException(Exception):
    def __init__(self, *args):
        super().__init__(args)
    
    def __str__(self):
        return "You cannot perform transactions on a non-active account"

class InvalidTransferException(Exception):
    def __init__(self, *args):
        super().__init__(args)
    
    def __str__(self):
        return "The destination account cannot be inactive, deactivated, or the same as the source account"

