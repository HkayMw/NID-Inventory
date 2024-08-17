import datetime
text = "~John~Doe~Smith~M~123456~01/01/2000~extra~data~here"

array = text.split('~')

sorting_key= array[1][:7].upper()


print(sorting_key)