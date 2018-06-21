在Python中，没有类似 private 之类的关键字来声明私有方法或属性。

Python中要声明私有属性，需要在属性前加上双下划线（但是结尾处不能有双下划线），如：self.__a。然而这样的什么方式并不是真正私有，而是“伪私有”。

Python的伪私有属性，实际是通过变量名压缩（mangling）来实现变量名局部化。变量名压缩的规则：在初始的变量名头部加上一个下划线，再加上类的名称，最后是初始变量名的名称。

执行以下代码来验证：
class A(object):
    def __func(self):pass

if __name__ == '__main__':
    print(A.__dict__)

运行结果：
{'__weakref__': <attribute '__weakref__' of 'A' objects>, '__module__': '__main__', '__doc__': None, '_A__func': <function A.__func at 0x10cfa037
8>, '__dict__': <attribute '__dict__' of 'A' objects>}

我们通过类的__dict__属性，将class A的所有属性打印出来，从打印的结果可以发现：原先定义的伪私有属性（方法）：__func 在__dict__中并不存在，取而代之的是_A_func这个方法，方法__func的变量名被压缩。

如此在外部调用class A的__func方法时，会提示无法找到。修改代码进行测试：
复制代码

class A(object):
    def __func(self):pass

if __name__ == '__main__':
    a = A()
    a.__func()


运行后出现异常，提示A没有属性__func，从而实现类似私有属性的功能。

AttributeError: 'A' object has no attribute '__func'

之所以说它是“伪私有”，是因为在了解伪私有变量的变量名压缩规则后，可以根据压缩规则进行调用。

再次修改代码进行验证：

class A(object):
    def __func(self):print('Hello Python')

if __name__ == '__main__':
    a = A()
    a._A__func()

运行结果正常， 成功打印“Hello Python”字符串。

Hello Python

 所以，Python的类并不存在正在的私有属性，通过双下划线实现的伪私有属性，本质上是对变量名进行压缩，使之无法直接在外部调用。

为什么要使用伪私有属性

使用伪私有属性是为了避免在类树中，多个类赋值相同的属性引发冲突问题。

假设有两个类，C1 和 C2，他们都有相同的属性X。

class C1():
    def meth1(self):
        self.x = 'Hello World'
    def meth2(self):
        print(self.x)

c1 = C1()
c1.meth1()
c1.meth2()

class C2():
    def meth3(self):
        self.x = 'Hello Python'
    def meth4(self):
        print(self.x)

c2 = C2()
c2.meth3()
c2.meth4()

类C1和C2在单独调用时，输出结果没有问题，符合预期：调用meth2方法时，打印meth1的赋值结果；调用meth4方法时，打印meth3的赋值结果。

此时增加一个新的类C3，继承自C1、C2（多重继承）：

class C1():
    def meth1(self):
        self.x = 'Hello World'
    def meth2(self):
        print(self.x)

class C2():
    def meth3(self):
        self.x = 'Hello Python'
    def meth4(self):
        print(self.x)

class C3(C1, C2):
    pass

c3 = C3()
c3.meth1()
c3.meth3()
c3.meth2()
c3.meth4()

从运行结果可以看出，每次 print(self.x)的内容，取决于 self.x 最后一次赋值的内容。

Hello Python
Hello Python

在示例代码中，先调用 c3.meth1() 进行赋值，self.x的值为“Hello World”，再调用 c3.meth3() 进行赋值时，self.x的值被覆盖，目前的值为“Hello Python”。

后续再调用c3.meth2()打印self.x的值时，实际上打印的是最后一次赋值结果，这在有些情况下跟类的设计初衷是相违背的：在C1中，meth2希望打印的是在meth1中赋值的内容：“Hello World”。

在使用伪私有属性后可以解决变量名self.x相互覆盖的问题（因为self.__x 被压缩成了 self._C1__x 和 self._C2__x，变量名不同，不会互相覆盖）：

class C1():
    def meth1(self):
        self.__x = 'Hello World'
    def meth2(self):
        print(self.__x)

class C2():
    def meth3(self):
        self.__x = 'Hello Python'
    def meth4(self):
        print(self.__x)

class C3(C1, C2):
    pass

c3 = C3()
c3.meth1()
c3.meth3()
c3.meth2()
c3.meth4()


运行结果符合C1的设计初衷:调用meth2时应该打印出meth1的赋值结果：

Hello World
Hello Python
