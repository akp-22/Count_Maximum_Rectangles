# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:38:46 2019

@author: kashok
"""
"""
Rectangle is defined by bottom left corner, width and height. 
Input text file should contain the number of the rectangles followed by the rectangles
"""

import sys
import math

"""
Algo in brief:
#Algo step 1: 
Iterate the below step for all the given rectangles
>Select a rectange
 
    #Algo step 2: 
    Iterate the below steps for all the 4 corners of the selected rectangle
    >Choose a corner from the selected rectangle. It is a reference corner.     

        #Algo step 3:               
        >Collect all the remaining rectangle corners
        >Sort all these corners as per the polar angle wrt to reference corner
        >Traverse through all the corner points and 
        if the encountered corner point is of a new rectangle 
            then increment the rectangle found counter (line of sight) and 
        if the encountered corner point is the last one of a rectangle 
            then decrement the rectangle found counter (line of sight) 
       
        #Algo step 4:
        >Update global maximum for the rectangle found (line of sight) counter 
            and the corresponding corner points for the line  
        >Reset the rectangle found (line of sight) counter for a new reference corner point 
        
>Maximum Number of rectangles that a line can pass through is the global maximum of the rectangle found (line of sight) counter 
>The line can be drawn from the updated line corners 
"""


"""
Algo implementation Software architecture:
    
    1. input : x, y, w, h
    2. rectangle list : [ [r1, c1, c2, c3, c4], [r2, ...], [rn, ...] ]
 
    Repeat the below step for all the N rectangles
    3. Pick a reference rectangle: [ri, c1, c2, c3, c4]
       
        Repeat the below step for all the 4 corners
        4. Pick a rererence corner from the reference rectangle: cr = c1/c2/c3/c4
           
            5. collect all the remaing rectangles in a list:
                [ [r1, c1, c2, c3, c4],... [ri-1, ..],[ri+1,..] ...[rn, ...] ]
            6. Find slope (or polor angle) wrt to reference corner (cr) for the rectangle list
                [ [r1, m1, m2, m3, m4],... [ri-1, ..],[ri+1,..] ...[rn, ...] ]
            7. Sort the slopes in descending order for each rectangle in the list
                [ [r1, md1, md2, md3, md4],... [ri-1, ..],[ri+1,..] ...[rn, ...] ]
            8. Merge all the rectangle slopes in to a list with format:"slope, rectangle id, slope decreasing order id" list
                [ [md1, r1, 0],  [md2, r1, 1], [md3, r1, 2], [md4, r1, 3], [md1, r2, 0] ...]
                Ex: [md1, r1, 0] => max. slope of rectangle r1 or entry point
                Ex: [md3, r1, 3] => min. slope of rectangle r1 or exit point 
                NOTE: Zero degree cross over
                For rectangle slopes which present in quadrants Q1 & Q4 there shall be two sets of entry and exits
            9. Perform merge sort over above slope list, since the list contains sorted slopes for a rectangle
                [ [m1, ri, oi], [m2, ri, oi], ....[m4n-4, ri, oi]]
                where, mi is slope of a rectangle ri and order within the rectangle is oi

            10. Traverse through the  slope list, which was sorted in descending order and
                count number of entry and exits of all the rectangles at given point of time.
                11. Keep track of "maximum count (max line of sight count) " at any point of time through out the program
            
    Global maximum for the "max los count"(max. line of sight counter) 
    gives the "max number of rectangles" a line can pass through
"""



"""
Prepare rectangle list from the given input data file path
Return rectangle list contains all the 4 corner points for each and every rectangle 
Return numer of input rectangles
"""
def util_prepare_rectangle(file_path):
 
    rect_list = []
    
    f = open(file_path)
    line = f.readline()
    
    line.replace('\n', '')
    num_total_rect = int(line)
    
    line = f.readline()
    line.replace('\n', '')
    
    while line:
        v = line.split()         
        x, y, w, h = [int(x) for x in v]
        corners = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
        rect_list.append(corners)
        line = f.readline()
        line.replace('\n', '')
    f.close()
    
    return num_total_rect, rect_list


"""
utility to find polar angle for the given two point tuples
return : angle : 0 to 360deg
"""

def util_slope(p1, p2):
    
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    
    
    rad = math.atan2(y2-y1, x2-x1)
    slope = math.degrees(rad)
    if slope < 0.0:
        slope += 360.0
    
    return slope

#float comparison utility
epsilon = 0.000000001
def util_f_equal(a, b):
   return abs(a - b) < epsilon 


"""
Algo to find maximum number of rectangles through which an line pass through
Rectangle data set is available in the given input file
"""
def max_num_rects(ip_file_path):
    
    """
    1. input : x, y, w, h
    2. rectangle list : [ [r1, c1, c2, c3, c4], [r2, ...], [rn, ...] ]
    """
    #prepare rectangle points
    num_rect, rect_list = util_prepare_rectangle(ip_file_path)    
       
    #Algo start
    max_rect_line_of_sight_count = 0    
    
    if len(rect_list) <= 1:
        return len(rect_list)
    
    """
    Repeat the below step for all the N rectangles
    3. Pick a reference rectangle: [ri, c1, c2, c3, c4]
    """
    for ref_rect_index in range(len(rect_list)):
        ref_rect = rect_list[ref_rect_index]
        """
        Repeat the below step for all the 4 corners
        4. Pick a rererence corner from the reference rectangle: cr = c1/c2/c3/c4
        """
        #print ("ref_rect", ref_rect)
        for ref_corner_index in range(len(ref_rect)):
            ref_corner = ref_rect[ref_corner_index]
            #print ("ref_corner", ref_corner)
            """
            5. collect all the remaing rectangles in a list:
                [ [r1, c1, c2, c3, c4],... [ri-1, ..],[ri+1,..] ...[rn, ...] ]
            """
            """
            6. Find slope (or polor angle) wrt to reference corner (cr) for the rectangle list
                [ [r1, m1, m2, m3, m4],... [ri-1, ..],[ri+1,..] ...[rn, ...] ]
            """
           
            slope_list = []
            for rect_index in range(len(rect_list)):
                rect = rect_list[rect_index]
                if rect_index == ref_rect_index:
                    continue
                
                slope_params = []
                for corner in rect:
                    slope = util_slope(ref_corner, corner)
                    slope_params.append(slope)         
                """
                7. Sort the slopes in descending order for each rectangle in the list
                    [ [r1, md1, md2, md3, md4],... [ri-1, ..],[ri+1,..] ...[rn, ...] ]
                                     
                """
                slope_params.sort(reverse=True)                    
                #print (slope_params)
                
                """
                8. Merge all the rectangle slopes in to a list with format:"slope, rectangle id, slope decreasing order id" list
                    [ [md1, r1, 0],  [md2, r1, 1], [md3, r1, 2], [md4, r1, 3], [md1, r2, 0] ...]
                    Ex: [md1, r1, 0] => max. slope of rectangle r1 or entry point
                    Ex: [md3, r1, 3] => min. slope of rectangle r1 or exit point
                    NOTE: Zero degree cross over
                    For rectangle slopes which present in quadrants Q1 & Q4 there shall be two sets of entry and exits
                """               
                #zero degree cross over 
                if slope_params[1] >= 270 and slope_params[2] <= 90:
                    slope_list.append((slope_params[0], rect_index, 0))
                    slope_list.append((slope_params[1], rect_index, 3))
                    slope_list.append((slope_params[2], rect_index, 0))
                    slope_list.append((slope_params[3], rect_index, 3))
                else:
                    slope_list.append((slope_params[0], rect_index, 0))
                    slope_list.append((slope_params[1], rect_index, 1))
                    slope_list.append((slope_params[2], rect_index, 2))
                    slope_list.append((slope_params[3], rect_index, 3))
                    
        
            #print ("slope_list_before_merge \n", slope_list)    
            """            
            9. Perform merge sort over above slope list, since the list contains sorted slopes for a rectangle
                [ [m1, ri, oi], [m2, ri, oi], ....[m4n-4, ri, oi]]
                where, mi is slope of a rectangle ri and order within the rectangle is oi
            """
            slope_list.sort(reverse=True, key = lambda x: x[0] )  
            #print ("slope_list_after_sort \n ", slope_list)
            
            """
            10. Traverse through the  slope list, which was sorted in descending order and
                count number of entry and exits of all the rectangles at given point of time.
            """
            #slope_list parameter indexes
            slope_id = 0
#            rect_id = 1

            order_id = 2 #slope order(1, 2, 3, 4) within a rectangle
            rect_line_of_sight_count = 0;
            
            rect_exit_count = 0
            rect_exit_slope = -1.0 #can not be 0.0 to 360.0
            
            for i in range(len(slope_list)):
                
                #Entry of a rectangle in the line of sight 
                if slope_list[i][order_id] == 0 : 
                    rect_line_of_sight_count  += 1
            
                #Exit of a rectangle in the line of sight: 
                #Update the counter (decrement) just after crossing the rectangle
        
                if (rect_exit_count > 0) and not(util_f_equal(rect_exit_slope, slope_list[i][slope_id])):
                    rect_exit_slope = slope_list[i][slope_id]
                    rect_line_of_sight_count  -= rect_exit_count
                    rect_exit_count = 0 
                
                if slope_list[i][order_id] == 3:   
                    rect_exit_count += 1
                    rect_exit_slope = slope_list[i][slope_id]              
               
                """
                11. Keep track of "maximum count (max line of sight count) " at any point of time through out the program            
                Global maximum for the "max los count"(max. line of sight counter) 
                gives the "max number of rectangles" a line can pass through
                """
                if  max_rect_line_of_sight_count < rect_line_of_sight_count:
                    max_rect_line_of_sight_count = rect_line_of_sight_count
            
            #print("temp_max", rect_line_of_sight_count)
            #print("max_rect", max_rect_line_of_sight_count)
            
            
    return max_rect_line_of_sight_count + 1
    
    
#argv = "input.txt"
def main(argv):
   
    """
    for i, v in enumerate(argv):
        print("argv[{0}]: {1}".format(i, v))
    """
    #input argument    
    argv = "sample3.txt"

    #Find max. number of given rectangles through whoch a line can pass through
    count = max_num_rects(argv)
    print (count)
        
    #slope (polor angle) test cases
    """
    #+ / +
    print(util_slope((0,0),(1,3)))
    #+ / -
    print(util_slope((1,0),(0,3)))
    #- / -
    print(util_slope((1,3),(0,0)))
    #- / +
    print(util_slope((1,3),(3,1)))

    #0/0
    print(util_slope((0,0),(0,0)))
    # +/0
    print(util_slope((0,0),(0,1)))
    # -/0
    print(util_slope((0,1),(0,0)))
    # 0/-
    print(util_slope((1,0),(0,0)))
    # 0/+
    print(util_slope((0,0),(1,0)))
    """
        
if __name__ == '__main__':
    main(sys.argv[1:])    
    
