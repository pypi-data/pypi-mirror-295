var = 90

def outer():
    nonlo  = "Global Variable"
    global fg
    fg = '[p[p[pp[]]]]'
    def manipulate_nonlo():
        nonlocal nonlo
        nonlo = 78
        print(fg)

    def printt():
        print(nonlo)
        
    manipulate_nonlo()
    printt()

outer()


