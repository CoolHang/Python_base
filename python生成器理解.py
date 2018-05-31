
通过列表生成式，我们可以直接创建一个列表。但是，受到内存限制，列表容量肯定是有限的。而且，创建一个包含100万个元素的列表，不仅占用很大的存储空间，如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。

所以，如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list，从而节省大量的空间。在Python中，这种一边循环一边计算的机制，称为生成器（Generator）。

简单生成器

要创建一个generator，有很多种方法。第一种方法很简单，只要把一个列表生成式的[]改成()，就创建了一个generator：
复制代码
>>> L = [x * x for x in range(10)]

>>> L

[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

>>> g = (x * x for x in range(10))

>>> g

<generator object <genexpr> at 0x104feab40>

创建L和g的区别仅在于最外层的[]和()，L是一个list，而g是一个generator。
我们可以直接打印出list的每一个元素，但我们怎么打印出generator的每一个元素呢？

如果要一个一个打印出来，可以通过generator的next()方法：
复制代码

>>> g.next()

0

>>> g.next()

1

>>> g.next()

4

>>> g.next()

9

>>> g.next()

16

>>> g.next()

25

>>> g.next()

36

>>> g.next()

49

>>> g.next()

64

>>> g.next()

81

>>> g.next()

Traceback (most recent call last):

  File "<stdin>", line 1, in <module>

StopIteration


我们讲过，generator保存的是算法，每次调用next()，就计算出下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。

当然，上面这种不断调用next()方法实在是太变态了，正确的方法是使用for循环，因为generator也是可迭代对象：

>>> g = (x * x for x in range(10))

>>> for n in g:

...     print n

...

0

1

4

9

16

25

36

49

64

81

所以，我们创建了一个generator后，基本上永远不会调用next()方法，而是通过for循环来迭代它。

带yield 语句的生成器

仔细观察，可以看出，fib函数实际上是定义了斐波拉契数列的推算规则，可以从第一个元素开始，推算出后续任意的元素，这种逻辑其实非常类似generator。

也就是说，上面的函数和generator仅一步之遥。要把fib函数变成generator，只需要把print b改为yield b就可以了：
复制代码

def fib(max):

    n, a, b = 0, 0, 1

    while n < max:

        yield b

        a, b = b, a + b

        n += 1

复制代码

 这就是定义generator的另一种方法。如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator：
代码如下:

>>> fib(6)
< generator object fib at 0x104feaaa0>

 

这里，最难理解的就是generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。

举个简单的例子，定义一个generator，依次返回数字1，3，5：
复制代码

>>> def odd():

...     print 'step 1'

...     yield 1

...     print 'step 2'

...     yield 3

...     print 'step 3'

...     yield 5

...

>>> o = odd()

>>> o.next()

step 1

1

>>> o.next()

step 2

3

>>> o.next()

step 3

5

>>> o.next()

Traceback (most recent call last):

  File "<stdin>", line 1, in <module>

StopIteration

可以看到，odd不是普通函数，而是generator，在执行过程中，遇到yield就中断，下次又继续执行。执行3次yield后，已经没有yield可以执行了，所以，第4次调用next()就报错。

回到fib的例子，我们在循环过程中不断调用yield，就会不断中断。当然要给循环设置一个条件来退出循环，不然就会产生一个无限数列出来。

同样的，把函数改成generator后，我们基本上从来不会用next()来调用它，而是直接使用for循环来迭代：

>>> for n in fib(6):

...     print n

...

1

1

2

3

5

8

加强的生成器

在 python2.5 中,一些加强特性加入到生成器中,所以除了 next()来获得下个生成的值,用户可以将值回送给生成器[send()],在生成器中抛出异常,以及要求生成器退出[close()]

def gen(x):

    count = x

    while True:

        val = (yield count) 

        if val is not None:

            count = val

        else:

            count += 1
f = gen(5)

print f.next()

print f.next()

print f.next()

print '===================='

print f.send(9)#发送数字9给生成器

print f.next()

print f.next()


输出：

5

6

7

====================

9

10

11
