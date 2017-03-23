#!/usr/bin/python
import sys
import random


class Problem(object):
    ''' Read input problem -> [generate interpretation <> find Solution <]'''

    def __init__(self):
        self.num_vars = 0
        self.num_clauses = 0
        self.clauses = []
        self.inter = []

    def read_clauses(self, cnf_file):
        ''' Read input and save clauses in a list of lists '''
        clause = []
        clauses = []

        data = open(cnf_file, 'r')
        for line in data:
            line = line.split()
            if line[0] not in ('c', 'p'):
                for i in line:
                    if i != '0':
                        clause.append(int(i))
                clauses.append(clause)
                clause = []

            elif line[0] == 'p':
                self.num_vars = int(line[2])
                self.num_clauses = int(line[3])
        self.clauses = clauses
        self.solve()

    def solve(self):
        '''Check if all clauses are satisfied with diferents interpretations'''
        max_tries = 9999999
        max_flips = 200000
        for i in xrange(0, max_tries):
            inter = self.generate_interpretation()
            for j in xrange(0, max_flips):
                is_sat = self.is_satisfiable(inter)
                inter = self.flip_inter(inter, is_sat)
        self.print_nosolution()

    def is_satisfiable(self, inter):
        ''' Check if the given clause is satisfied '''
        for clause in self.clauses:
            sat = False
            for i in clause:
                if i == inter[abs(i) - 1]:
                    sat = True
                    break
            if not sat:
                return clause

        self.inter = inter
        self.print_solution()

    @staticmethod
    def flip_inter(inter, sat):
        ''' Change a variable randomly'''
        lit = sat[random.randint(0, len(sat) - 1)]
        inter[abs(lit) - 1] = inter[abs(lit) - 1] * -1
        return inter

    def generate_interpretation(self):
        ''' Generate a random interpretation '''
        inter = list(xrange(1, self.num_vars + 1))
        for i in xrange(0, len(inter) - 1):
            if random.random() > 0.5:
                inter[i] = inter[i] * -1
        return inter

    def print_solution(self):
        ''' s SATISFIABLE
            v 1 2 3 -4 -5 -6 7 8 9 -10
        '''
        print "s SATISFIABLE"
        print "v",
        for item in self.inter:
            print item,
        sys.exit(0)

    @staticmethod
    def print_nosolution():
        ''' Print no solution '''
        print "s No Solution Found"
        sys.exit(0)


if __name__ == '__main__':
    random.seed()
    Problem().read_clauses(sys.argv[1])
