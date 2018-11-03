class gen(object):

    def generator(self, idx):
        print idx

    def executor(self):
        for i in range(3):
            yield self.generator, i

if __name__ == '__main__':
    obj = gen()
    obj.executor()
    obj.executor()
    obj.generator(1)
    print 'bingo'