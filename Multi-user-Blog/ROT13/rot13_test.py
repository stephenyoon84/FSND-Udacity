rot13_set = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
            'Q','R','S','T','U','V','W','X','Y','Z','A','B','C','D','E','F','G',
            'H','I','J','K','L','M',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
            'q','r','s','t','u','v','w','x','y','z','a','b','c','d','e','f','g',
            'h','i','j','k','l','m']

test1 = "Hello, Udacidy!!"

# print len(test1)
# print test1.find(test1[1])
# print rot13_set.index(test1[0])
# print test1[0]
# print rot13_set[rot13_set.index(test1[0]) + 13]

result = ""

for i in test1:
    if i in rot13_set:
        result += rot13_set[rot13_set.index(i) + 13]
    else:
        result += i
print result




# def rot13(input):
#     result = ''
#
