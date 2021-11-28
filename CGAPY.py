"""
Created on Mon Nov 28 01:18:59 2021

@name: Can Genetic Algorithm Python
@author: Canberk Pitirli
@version: 0.0.1
@python: 3.8
"""

import collections
from collections.abc import Iterable
import time

import random
from difflib import SequenceMatcher

"""
Operators of the generic algorithm:
Selection: Select elite individuals
Crossover/Mate: Crossover genes of chromosomes and create new individuals
Mutation: Mutate these new created individuals
Calculate Fitness: Calculate new created individuals
Sorting: Sort all of the population and select next elite individuals

Basicly, a genetic algorithm follows these steps:
Select elite individuals to mate, mutation and product next generation
Kill previous generation
repeat until find the best solution

Elitism only means that the most fit handful of individuals are guaranteed a place in the next generation 
generally without undergoing mutation. They should still be able to be selected as parents
in addition to being brought forward themselves.
"""

GENES = 'abcçdefgğhıijklmnoöpqrstuüvwxyzABCÇDEFGĞHIİJKLMNOÖPQRSTUÜVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'

class Gen:
    '''
    Genes are smallest part of solution. They carry values which creates chromosomes with a group of genes
    Genes also represents itself if it is super gen or not. Super genes are genes that is correct both in position and value according to solution
    '''
    def __init__(self, value):
        if type(value) is not str:
            raise ValueError('Value must be a string')
        if type(value) is type(str): self._value = value[0]
        else: self._value = str(value)[0]
        self._super = False

    def __repr__(self):
        return self.Value

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, value):
        self._value = value

    @property
    def SuperGen(self):
        return self._super

    @SuperGen.setter
    def SuperGen(self, value):
        if value is True or value is False:
         self._super = value
        else:
            raise ValueError('You can only set True or False values')
    
    def Mutation(self):
        if not self.SuperGen:
            self.Value = random.choice(GENES)
            
class Chromosome:
    def __init__(self, Genes = None):
        if Genes is None:
            raise ValueError("Genes are not set!")
        self._genes = Genes
        self._eliteness = False
        self._isMutant = False
        self._length = len(Genes)
        self._fitness = 0

    def __getitem__(self, item):
           return self._genes[item]
       
    def __len__(self):
        return len(self._genes)
       
    def __repr__(self):
       return f"\n {Core.ListToStr(self._genes)} Fitness Score: %{int(self.Fitness)} Elite: {self.IsElite}" 
       
    def __iter__(self):
       self.loc = 0
       return self
    
    def __next__(self):
        if self.loc >= len(self._genes)-1:
            raise StopIteration
        self.loc += 1
        return self._genes[self.loc]
    
    def getIndex(self, gen):
        if type(gen) is Gen:
         return self._genes.index(gen)
        else:
            raise ValueError('You must pass a gen as argument')
    
    def AddGen(self,value):
        self._genes.append(value)

    @property
    def IsElite(self):
        return self._eliteness

    @IsElite.setter
    def IsElite(self, value):
        self._eliteness = value

    @property
    def IsMutant(self):
        return self._isMutant

    @IsMutant.setter
    def IsMutant(self, value):
        self._isMutant = value

    @property
    def Fitness(self):
        return self._fitness

    @Fitness.setter
    def Fitness(self, value):
        self._fitness = value

    @property
    def Length(self):
        return self._length

    @Length.setter
    def Length(self, value):
        self._length = value

    @property
    def Genes(self):
        return self._genes

    @Genes.setter
    def Length(self, value):
        self._genes = value

    def Mutation(self, MutationChance = 0.99):
        self.Genes[0].value = 'H'
        if MutationChance > 1 or MutationChance < 0:
            raise ValueError('Value must be between 1 and 0')
        
        chance = Population.Chance()
        if chance >= 1-MutationChance:
            for gen in self._genes:
                gen.Mutation()
            Core.Debug('Mutation is successfull for a chromosome!')

    def Crossover(self, target):
        if type(target) is not Chromosome:
            raise ValueError('Target value must be another chromosome!')
        child_gen = []
        for i in range(len(target)):
            rnd = random.random()
            
            if rnd >= 0.45:
                child_gen.append(self[i])
            else:
                child_gen.append(target[i])
            
        return Chromosome(Genes=child_gen)

class Population(collections.deque):
    def __init__(self , Input, InitialPopulation = None, Population_Length=10, Solution = None, EliteOffset = 0.80):
        self._genlen = len(Input)
        self._len = Population_Length
        self._chromosomes = []
        if InitialPopulation is not None and type(random.choice(InitialPopulation)) is Chromosome:
            self._chromosomes = InitialPopulation
        else:
            self._chromosomes = self.GenerateFirstGeneration(Population_Length, self._genlen)
        self.EliteOffset = EliteOffset
        self._generation = 1
        
    def __getitem__(self, item):
        return self._chromosomes[item]
    
    def __len__(self):
        return self._len

    def __repr__(self):
        return ' of {0} ->'.format(self.Generation) + str(self._chromosomes)
    
    def __iter__(self):
        self.value = 0
        return self
    
    def __next__(self):
        self.value += 1
        try:
            return self._chromosomes[self.value]
        except:
            raise StopIteration
        
    def getIndex(self, chrom):
        if type(chrom) is Chromosome:
         return self._chromosomes.index(chrom)
        else:
         raise ValueError('Argument must be a chromosome')
    
    @property
    def Generation(self):
        return self._generation
    
    @Generation.setter
    def Generation(self,value):
        self._generation = value

    @staticmethod
    def Chance():
        return random.random()

    def Sort(self):
        self._chromosomes.sort(key=lambda chrom: chrom.Fitness, reverse=True)
    
    def RefreshElits(self):
        TotalFitness = 0
        for chrom in self._chromosomes:
            TotalFitness += chrom.Fitness
        for chrom in self._chromosomes:
            if TotalFitness != 0 and chrom.Fitness >= TotalFitness/(len(self)):
                chrom.IsElite = True
            else:
                chrom.IsElite = False
    
    def Selection(self, Select_Elite = False):
        Selected = None
        
        if Select_Elite:
            Selected = random.choice(filter(lambda Elite: Elite.IsElite,self._chromosomes))
        else:
            Selected = random.choice(self._chromosomes)
        
        return Selected
        
    def AddChromosome(self, chrom):
        if type(chrom) is not Chromosome:
            raise ValueError('Argument must be a Chromosome!')
        self._chromosomes.append(chrom)
        self._len += 1
        
    def RemoveChromosome(self,chrom):
        if type(chrom) is not Chromosome:
            raise ValueError('Argument must be a Chromosome!')
        self._chromosomes.remove(chrom)
        self._len -= 1
    
    def SurvivalOfTheFitness(self):
        TotalFitness = sum(chrom.Fitness for chrom in self._chromosomes)
        for chrom in self._chromosomes:
            if self._chromosomes[int(len(self._chromosomes)/2)].Fitness > chrom.Fitness and not chrom.IsElite:
             self.RemoveChromosome(chrom)
                
    def GenerateFirstGeneration(self,PopLen,ChromLen):
        Chroms = []
        for n in range(PopLen):
            Genes = []
            for i in range(ChromLen):
             Genes.append(Gen(random.choice(GENES)))
            Chroms.append(Chromosome(Genes=Genes))
        return Chroms


class Core:
    def __init__(self, Population):
        self.pop = Population
        self.completed = False

    def Run(self,Input):
        Core.Debug('-------------------------------------------')
        Core.Debug('Genetic algorithm has been started! input -> %s' % Input)
        Core.Debug('First generation = %s' % str(self.pop))
        self._input = Input
        
        while not self.completed:
            self.CalculateFitness()
            self.pop.RefreshElits()
            self.pop.Sort()
            self.pop.AddChromosome(self.pop[0].Crossover(self.pop.Selection()))
            self.pop.Selection().Mutation()
            self.pop.SurvivalOfTheFitness()
            self.Info(self.pop)
            self.pop.Generation += 1
            time.sleep(0.05)
            if len(self.pop) == 1:
                print('OMG you killed the population, you monster!')
                self.completed = True
            if self.pop[0].Fitness >= 95:
                self.completed = True

    def CalculateFitness(self):
        inp = list(self._input)
        for chrom in self.pop:
            i = 0
            similiarity = 0
            for gen in chrom.Genes:
             chrom.fitness = 1
             index = chrom.getIndex(gen)
             if gen.Value == inp[index]:
              gen.SuperGen = True
              similiarity += 1
              chrom.Fitness = (100*similiarity)/len(chrom)
                
        
    def Info(self, Population):
        Core.Debug(str(Population) + f'Size of population:{str(len(Population))}') 

    @staticmethod
    def ListToStr(lst):
        string = ''
        for gen in lst:
            string = string + gen.Value
        return string
            
    @staticmethod
    def Debug(value):
        print(value)
        
    @staticmethod
    async def DebugAsync(value):
        await print(value)
        
    
if __name__ == '__main__':
    inp = input('Enter a value to start the algorithm...\n')
    starter = Core(Population(inp))
    starter.Run(inp)
    
