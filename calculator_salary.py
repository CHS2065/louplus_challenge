#!/usr/bin/env python3
					
import sys
import csv

#get the command line parameter, then get the path of all files
class Args(object):
    def __init__(self):
        args = sys.argv[1:]
        self.configFile = args [ args.index('-c')+1 ]
        self.userData = args [ args.index('-d')+1 ]
        self.outputFile = args [ args.index('-o')+1 ]

args = Args()


class Config(object):
                                                    
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = {'sum_shebao': 0}

        with open(args.configFile) as file:
            for line in file.readlines():
                a, b = line.split('=')
                if float(b) > 1:
                    config[a.strip()] = float(b)
                else:
                    config['sum_shebao'] += float(b)
        return config

config = Config().config
   
class UserData(object):
    def __init__(self):
        with open(args.userData) as f:
            data = list(csv.reader(f))
        self.userData = data
    
userdata = UserData().userData

class IncomeTaxCalculator(object):
    def calc_for_all_userdata(self,salary):
        shebao = salary * config.get('sum_shebao')
        if salary < config.get('JiShuL'):
            shebao = config.get('JiShuL') * config.get('sum_shebao')
        if salary > config.get('JiShuH'):       
            shebao = config.get('JiShuH') * config.get('sum_shebao')
        tax_income = salary - shebao - 3500
        if tax_income < 0:
            tax = 0
        elif tax_income <= 1500:
            tax = tax_income * 0.03 - 0

        elif tax_income <= 4500:
            tax =  tax_income * 0.10 - 105 

        elif tax_income <= 9000:
            tax =  tax_income * 0.20 - 555 

        elif tax_income <= 35000:
            tax = tax_income * 0.25 - 1005

        elif tax_income <= 55000:
            tax = tax_income * 0.30 - 2755

        elif tax_income <= 80000:
            tax = tax_income * 0.35 - 5505

        else:
            tax = tax_income * 0.45 - 13505
        after_tax_salary = salary - shebao - tax

        return [salary, format(shebao, '.2f'), format(tax, '.2f'),
            format(after_tax_salary, '.2f')]


    def export(self):
        l = []
        for i in userdata:
            id, salary = i[0], int(i[1])
            result = self.calc_for_all_userdata(salary)
            result.insert(0, id)
            l.append(result)

        with open(args.outputFile, 'w') as file:
            #csv.writer(file).writerows(l)
            writer = csv.writer(file)
            writer.writerows(l)

def main():
    incomecal =  IncomeTaxCalculator()
    incomecal.export()


if __name__ == '__main__':
    main()
