from kmean import init_centers_random, init_centers_first_k, train_kmean, sum_of_within_group_ss
from data import load_data

import matplotlib.pyplot as plt


# TODO: Please submit your plot and answers for Q2.4.1 - Q2.4.6 in your write up.
def main():
    val_names, data_set = load_data()
    iter_limit = 20

    # Q2.4.1: The values of sum of within group sum of squares for k = 5, k = 10 and k = 20.
    print "Q 2.4.1"
    for k in [5, 10, 20]:
        init_centers = init_centers_first_k(data_set, k)
        centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
        print "k =", str(k) + ": " + str(sum_of_within_group_ss(clusters, centers))
        
        print
    print
    
    # Q2.4.2: The number of iterations that k-means ran for k = 5.
    print "Q 2.4.2"
    k = 5
    init_centers = init_centers_first_k(data_set, k)
    centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
    print "k =", str(k) + ", num_iter: " + str(num_iterations)
    print
    #look at clusters
    for i in range(len(clusters)):
        print
        if len(clusters[i]) > 1:
            print "Cluster " + str(i+1) + "**************"
            for j in range(len(clusters[i])):
                print clusters[i][j]['country']
    print

    # Q2.4.3: A plot of the sum of within group sum of squares versus k for k = 1 - 50.
    # Please start your centers randomly (choose k points from the dataset at random).
    print "Q 2.4.3"
    xVals = []
    yVals = []
    zVals = []
    minSSS = 1
    mink = 0
    for k in range(1, 51):
        init_centers = init_centers_random(data_set, k)
        centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
        print str(k) + ", " + str(sum_of_within_group_ss(clusters, centers))
        #save data
        xVals.append(k)
        yVals.append(sum_of_within_group_ss(clusters, centers))
        zVals.append(num_iterations)
        if sum_of_within_group_ss(clusters, centers) < minSSS:
            minSSS = sum_of_within_group_ss(clusters, centers)
            mink = k
        if k == 50:
            for i in range(len(clusters)):
                if len(clusters[i]) > 5:
                    print
                    print "Cluster " + str(i+1) + "**************"
                    for j in range(len(clusters[i])):
                        print clusters[i][j]['country']

    plt.plot(xVals,yVals)
    plt.title('SSS vs. k')
    plt.xlabel('Number of Centers')
    plt.ylabel('Sum of Within Group Sum of Squares')
    plt.show()
    print mink
    print len(data_set)
if __name__ == "__main__":
    main()
