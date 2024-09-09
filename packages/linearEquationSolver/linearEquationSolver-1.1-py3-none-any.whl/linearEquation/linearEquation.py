def linearEquationTwo(array1,array2):
    a,b,c,d,e,f = array1[0],array1[1],array1[2],array2[0],array2[1],array2[2]
    try:
        #formula to find y and x, derived mathematically
        y = ((a*f)-(d*c))/((a*e)-(d*b))
        x = (c-(b*y))/a
        
        #format float to 3 decimal points
        y = "{:.3f}".format(y)
        x = "{:.3f}".format(x)

        return x,y
    except ZeroDivisionError:
        return "Inconsistent System or Dependant System"
    except SyntaxError:
        return "Syntax error"

def linearEquationThree(array1,array2,array3):
    a,b,c,d,e,f,g,h,i,j,k,l = array1[0],array1[1],array1[2],array1[3],array2[0],array2[1],array2[2],array2[3],array3[0],array3[1],array3[2],array3[3]
    
    try:
        #formula to find z, y and x, derived mathematically
        z = (((a**2)*l*f)-(a*l*e*b)-(i*d*a*f)+(i*b*a*h)-((a**2)*j*h)+(a*j*e*d))/((i*b*a*g)-(i*c*a*f)+((a**2)*k*f)-(a*k*e*b)+(a*j*e*c)-((a**2)*j*g))
        y = ((a*h)-(e*d)+(z*((e*c)-(a*g))))/((a*f)-(e*b))
        x = (d-(b*y)-(c*z))/(a)

        #format float to 3 decimal points
        z = "{:.3f}".format(z)
        y = "{:.3f}".format(y)
        x = "{:.3f}".format(x)
        
        return x,y,z
    except ZeroDivisionError:
        return "Inconsistent System/Dependent System"
    except SyntaxError:
        return "Syntax error"