def main():
    '''
    This is the main body of the program.
    '''
    
    filename = input('Which csv file should be analyzed? ')

    data = dict()               # Or data = {}
    with open(filename, 'r') as h:
        for line in h:
            four_vals = line.split(',')
            batch = four_vals[0]
            if not batch in data:
                data[batch] = []
            data[batch] += [(float(four_vals[1]), float(four_vals[2]), float(four_vals[3]))] # Collect data from an experiment

    print("Batch\t Average")
    for batch, sample in data.items(): 
        n = 0
        x_sum = 0
        for (x, y, val) in sample:
            if x**2 + y**2 <= 1:
                x_sum += val
                n += 1
            average = x_sum/n
        print(batch, "\t", average)