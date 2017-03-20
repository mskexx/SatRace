#!/usr/bin/python
import sys
import random


class Problem:

    def __init__(self):
        self.num_vars = 0
        self.num_clauses = 0
        self.clauses = []
        self.inter = []

    def read_clauses(self, cnf_file):
        clause = []
        clauses = []

        data = open(cnf_file, 'r')
        for line in data:
            line = line.split()
            if line[0] not in ('c', 'p'):
                for x in line:
                    if x != '0':
                        clause.append(int(x))
                clauses.append(clause)
                clause = []

            elif line[0] == 'p':
                self.num_vars = int(line[2])
                self.num_clauses = int(line[3])
        self.clauses = clauses
        self.solve()

    def solve(self):
        max_tries = 1000
        max_flips = 1500
        for i in xrange(0, max_tries):
            inter = self.generate_interpretation()
            for j in xrange(0, max_flips):
                cl = self.is_satisfiable(inter)
                inter = self.flip_inter(inter, cl)
        self.print_nosolution()


    def is_satisfiable(self, inter):
        for cl in self.clauses:
            sat = False
            for x in cl:
                if x == inter[abs(x)-1]:
                    sat = True
                    break
            if not sat:
                return cl

        self.inter = inter
        self.print_solution()

    def flip_inter(self, inter, cl):
        lit = cl[random.randint(0, len(cl)-1)]
        inter[abs(lit)-1] = inter[abs(lit)-1] * -1
        return inter

    def generate_interpretation(self):
        inter = list(xrange(1, self.num_vars+1))
        for x in xrange(0, len(inter)-1):
            if random.random() > 0.5:
                inter[x] = inter[x] * -1
        return inter

    def print_solution(self):
        print "s SATISFIABLE"
        print "v",
        for item in self.inter:
            print item,
        sys.exit(0)

    def print_nosolution(self):
        print "s No Solution Found"
        sys.exit(0)


if __name__ == '__main__':
    random.seed()
    solver = Problem()
    solver.read_clauses(sys.argv[1])
