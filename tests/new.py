class A:
    def __new__(cls, arg0, arg1=True):
        return super(A, cls).__new__(cls)
    
    def __init__(self, arg0):
        print(arg0)

a = A(10, True)