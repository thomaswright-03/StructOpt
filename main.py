import numpy as np
import pandas as pd
import time
from scipy.optimize import minimize
from config import P, H, E, sig_u, sig_l, ai_l, ai_u
from plotting import contourplotfunc, convergenceplotfunc

#DEFINE OBJECTIVES AND CONSTRAINTS (THE OPTIMISAITON PROBLEM)
def objective1(a):
    a1, a2 = a
    objective = 2 * np.sqrt(2) * a1 + a2
    return objective

def objective2(a):
    a1, a2 = a
    objective = (P * H / E) * (1 / (a1 + np.sqrt(2) * a2))
    return objective

def objective3(a):
    objective = 0.5*(objective1(a)) + \
                0.5*(objective2(a))
    return objective

def constraints(a):
    a1, a2 = a
    constraint1 = sig_u - (P * (a2 + np.sqrt(2) * a1) / (np.sqrt(2) * a1**2 + 2\
                                                         * a1 * a2))
    constraint2 = sig_u - (P / (a1 + np.sqrt(2) * a2))
    constraint3 = sig_l - (P * a2 / (np.sqrt(2) * a1**2 + 2 * a1 * a2)) #again,
                                                                #absolute values
    return[constraint1, constraint2, constraint3] #return constraint values 
                                                    #as list

#DEFINE THE OPTIMISATION FUNCTION (THE SOLUTION)
def optifunc(objective, in_guess, bounds, constraint_func, title, contours):
    
    #optimisation function to 'nest' the minimise and plotting functions so 
    #they can be easily repeated
    
    #DEFINE CALLBACK FUNCTION
    n_iteration = 0
    def callback(ak): #store each callback in a list of dictionaries
        nonlocal n_iteration
        
        iteration_data.append({'Iteration': n_iteration+1,'A1': ak[0],
                               'A2': ak[1], 'f(X)': objective(ak)})
        n_iteration += 1
        return

    #MAIN OPTIFUNC BODY:
    print("\n" + title + ":")
    iteration_data = []
    
    #solve the optimisation
    constraints_dict = [{'type': 'ineq', 'fun': constraint_func}]
    result = minimize(objective, in_guess, bounds=bounds, 
                      constraints=constraints_dict, callback=callback, 
                      method='SLSQP')
    
    #convert the iteration callback data into a dataframe
    iteration_data = pd.DataFrame(iteration_data)
    print(iteration_data.to_string(index=False))
    
    #call the plotting functions
    contourplotfunc(objective, title, contours, result, constraints=constraints)
    convergenceplotfunc(iteration_data, title)
    
    return result, n_iteration

#PREPARE AND EXECUTE FUNCTION CALLS, STORE RESULTS IN DATAFRAME
opcalls = [objective1, objective2, objective3]
optitles = ["Optimisation 1", "Optimisation 2", "Optimisation 3"]
contour_settings = [(1,18,18), (2,6,9), (4,9.5,12)]
results_list = []

#loop to call the three objectives and respective titles/contour plot settings    
for i in range(0,len(opcalls)):
    start = time.perf_counter()
    result, iterations = optifunc(opcalls[i], [2,2], [(ai_l, ai_u),(ai_l, ai_u)],
                                  constraints, optitles[i], contour_settings[i])
    
    # Get constraint values at optimum
    x_opt = result.x
    con_vals = constraints(x_opt)

    # Determine active constraints (those close to zero)
    active = [f'Constraint {i+1}' for i, val in enumerate(con_vals)
              if np.isclose(val, 0, atol=1e-6)] #Create list of active constraints
    active_str = ', '.join(active) if active else 'None' #create comma seperated
                                                         #string or 'None'
    #calculate objective values
    f1 = objective1(x_opt)
    f2 = objective2(x_opt)                                                     

    end = time.perf_counter()                                                     
    #store results in list of dictionaries
    results_list.append({'Title': optitles[i], 'A1': result.x[0],'A2': result.x[1],
                         'f(X)': result.fun,'Iterations': iterations, 
                         'Active Constraints': active_str, 'f1(x)':f1, 'f2(x)': f2,
                         'Runtime': f"{end - start:.4f} seconds"})

#PRESENT RESULTS DATA
results_summary = pd.DataFrame(results_list) #convert dictionaries to dataframe
print("\nOptimal Results Summary:")
print(results_summary.to_string(index=False))