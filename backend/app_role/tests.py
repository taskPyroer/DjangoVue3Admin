from django.test import TestCase

# Create your tests here.
data1= [['admin', '/system/dept/', 'POST'], ['admin', '/system/apis/', 'POST'], ['admin', '/system/apis/', 'DELETE']]
data2=[['admin', '/system/dept/', 'GET'], ['admin', '/system/apis/', 'GET'], ['admin', '/system/apis/', 'DELETE']]

set_data1 = set(tuple(item) for item in data1)
set_data2 = set(tuple(item) for item in data2)

print(set_data1)
print(set_data2)