




def test(t, **keywords):
    test2(**keywords)
    print(keywords)

def test2(**set):
    print(set)

test(1, a = 5)
