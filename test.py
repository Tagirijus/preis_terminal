class A(object):
	def __init__(self):
		print "Class A erstellt"

class B(object):
	def __init__(self):
		print "Class B erstellt"

	def testB(self):
		print "Making Test"

class C(B, A):
	pass

d = C()
d.testB()