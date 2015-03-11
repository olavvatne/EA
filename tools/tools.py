def validate( list, locally):
        p = list

        if locally:
            total = len(p)-1
            iteration = 2
        else:
            iteration =len(p)
            total = ((len(p)-1)*(len(p))/2)

        #Penality for nr of not surprising errors
        errors = 0
        for k in range(1, iteration):
            found_sequences = {}
            for i in range(len(p)-k):

                seq = str(p[i]) + "," + str(p[i+k])
                if seq in found_sequences:
                    print(k)
                    print(seq)
                    errors += 1
                else:
                    found_sequences[seq] = (i, i+k)

        print(errors)
        print(total)
        score = 1 - errors/total
        #score = 1/(1.+errors)
        return score

l = [4, 5, 3, 0, 4, 6, 1, 2, 3, 2, 6, 0, 3, 1, 0, 5, 4, 3]
print(validate(l, False))