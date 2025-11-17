import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.colors import LinearSegmentedColormap
from config import P, H, E, sig_u, sig_l, ai_l, ai_u

#DEFINE CONTOUR PLOTTING FUCTION
def contourplotfunc(objective_function, title, contours, result, constraints):
    #create 2D mesh to be used in plotting
    a1_values = np.linspace(ai_l, ai_u, 1000)
    a2_values = np.linspace(ai_l, ai_u, 1000)
    A1, A2 = np.meshgrid(a1_values, a2_values)

    # Calculate objective function values at each point in mesh
    Z = objective_function([A1, A2])
    
    #create boolean array of feasible region by checking constraints at 
    #each point in a 2D grid
    feasible_region = np.zeros((len(a1_values), len(a2_values)), dtype=bool)
    for j in range(0,len(a2_values)):
        for i in range(0, len(a1_values)):
            ##get constraint values fron ''constraints'##
            con_vals = constraints([a1_values[i],a2_values[j]])
            ##if all constraints > 0, return true##
            feasible_region[j, i] = all(v >= 0 for v in con_vals) 
    i = np.where(np.isclose(a1_values, 5))[0][0]
    j = np.where(np.isclose(a2_values, 5))[0][0]
 
    #create figure and axis and plot contours
    plt.figure(figsize=(9,6))
    ax = plt.gca()    
    start, stop, num = contours #expand contours tuple
    colors = ['#ff6b6b', '#e55b5b', '#b23a48','#a03c75','#8f3e87',
                           '#7646a5', '#4e4ca0', '#3a4e8c', '#2b4c7e']
    ##define custom colormap##
    cmap_custom = LinearSegmentedColormap.from_list('wider_purple_cmap', colors) 
    CS = plt.contour(A1, A2, Z, levels=np.linspace(start, stop, num), 
                     cmap=cmap_custom) 

    #calculate midpoint of longest contour component and plot contour labels
    def get_contour_label_positions(cs):
        positions = []
        for lvs in cs.allsegs:                #for each contour level...
            if lvs:                           #check that it exists on the plot
                long = max(lvs, key=lambda seg: len(seg))#get the longest segment
                mid_index = len(long) // 2         #half the length
                positions.append(long[mid_index])  #add position to label list
        return positions
    
    label_positions = get_contour_label_positions(CS)
    plt.clabel(CS, CS.levels, inline=True, fmt='%1.1f', fontsize=11, 
               manual=label_positions)

    #shade feasible region, add marker at optimal point, and set-up and show plot
    plt.contourf(A1, A2, feasible_region, levels=[0.5, 1], colors='darkgray', 
                 alpha=0.3)
    
    plt.plot(result.x[0], result.x[1], color='black', marker='x', markersize=12, 
             markeredgewidth=2, markeredgecolor='black', label="Optimal Point", 
             linestyle='none')
    
    plt.plot([], [], color='darkgrey', marker='s', label='Feasible Region',
             linestyle='none', markersize=12)
    
    # Plot constraint boundaries using the existing 'constraints' function
    num_constraints = len(constraints([2, 2]))  ## Automatically detect how 
                                                #many constraints exist##
    for i in range(num_constraints):                  # loop over the 3 constraints
        Zc = np.zeros_like(A1)                        #create empty array 
        con_linestyle = ['dotted','dashed','dashdot'] #set-up order of linestyles
        for j in range(A1.shape[0]):                  ##loop through every 
            for k in range(A1.shape[1]):              #point on the grid##
               a1 = A1[j, k]                          ##extract a1 and a2 values 
               a2 = A2[j, k]                          #at current coords##
               Zc[j, k] = constraints([a1, a2])[i]    #extract constraint value
               
        #plot contour = 0, representing constraint bound in KKT
        plt.contour(A1, A2, Zc, levels=[0], colors='black', 
                    linestyles=con_linestyle[i], linewidths=1.2)
                     
        plt.plot([], [], color='black', linestyle=con_linestyle[i], 
                 label='Constraint ' + str(i+1)) #dummy plot for legend label

    plt.legend(loc='lower right')
    plt.xlabel('Cross-Sectional Area - Beam 1 (A1)')
    plt.ylabel('Cross-Sectional Area - Beam 2 (A2)')
    plt.title("a) " + title + ' - Contours of the Objective ' 
              'Function and Feasible Region')
    plt.grid(True)
    plt.xlim(ai_l, ai_u)
    plt.ylim(ai_l, ai_u)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='both', direction='in', length=6)
    ax.tick_params(which='minor', length=3)
    plt.savefig(f"figures/{title} - Contours of the Objective Function and Feasible Region.png", dpi=1200)
    #plt.show()

#DEFINE CONVERGENCE PLOTTING FUNCTION
def convergenceplotfunc(data, title):
    #plot the convergence data using data from optifunc
    plt.figure(figsize=(9,6))
    plt.plot(data['Iteration'], data['f(X)'], marker='o', linestyle='-', 
             color = '#D44D5C')
    plt.xlabel('Iteration')
    plt.ylabel('Objective Function Value')
    plt.title("b) " + title + ' - Convergence Data')
    plt.grid(True)
    plt.savefig(f"figures/{title} - Convergence Data.png", dpi=1200)
    #plt.show()
    return