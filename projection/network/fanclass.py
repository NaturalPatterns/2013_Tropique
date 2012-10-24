#class for my lovely fan
from pyglet.gl import *
from math import pi, sin, cos , sqrt

def createline () :
    glLineWidth (10	 )
#    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(0,2,-1)

    glEnd()
    glLineWidth (10	 )


def my_own_draw (x,y,myscene, mylat, witdh_line,nbr_seg,rx ,ry,rmin ,rmax):
    depth = 0

    glLineWidth (int (witdh_line) )

    for i in range (0,nbr_seg):
        glBegin(GL_LINES)
        xbase = cos(rx +( (6.28/nbr_seg)* i ))
        ybase = sin(rx+( (6.28/nbr_seg)* i ))
#        print xbase*rmin, ybase*rmin
        old_var = (rmin + 100 *abs((cos(rx)+1)))
        #var = rmin + (1000* sqrt(1/(dist)))
        #print "old_var , var =",old_var, var
        if (myscene ==0):
            glVertex3f( depth ,xbase * rmin + x, (ybase * rmin) + y)
            #glColor3f(1,0,1)
            glVertex3f( depth ,xbase * rmax + x , (ybase * rmax) + y)

	if (myscene ==1):
		if (mylat==0):
			if  (xbase >= 0 ) : 
				glVertex3f(depth, xbase *( rmin *abs(cos(rx)+1)) + x ,(ybase *rmin) + y)
				glVertex3f(depth, xbase *( rmax *abs(cos(rx))+1) + x ,(ybase* rmax) +y )
			else :		
				glVertex3f(depth, xbase * rmin + x ,(ybase * rmin) + y)
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )
		if (mylat==1):
                      glVertex3f( depth ,xbase * rmin + x, (ybase * rmin) + y)
                      #glColor3f(1,0,1)
                      glVertex3f( depth ,xbase * rmax + x , (ybase * rmax) + y)
      
      
#			if  (xbase >= 0 ) : 
#				glVertex3f( depth,xbase * rmin + x ,(ybase * rmin) + y)
#				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )
#			else :		
#				glVertex3f(depth, xbase *( rmin *abs(cos(rx)+1)) + x ,(ybase * rmin) + y)
#				glVertex3f(depth, xbase *( rmax *abs(cos(rx))+1) + x ,(ybase * rmax ) +y )
		if (mylat==2):
			glVertex3f(depth, xbase *( rmin *abs(cos(rx)+1)) + x ,(ybase * rmin) + y)
			glVertex3f(depth, xbase *( rmax *abs(cos(rx))+1) + x ,(ybase * rmax ) +y )

	if (myscene ==2):
		if (mylat==0):
			if  (xbase >= 0 ) : 
				glVertex3f(depth, xbase *( 1 *abs(cos(rx)+2)) + x ,(ybase * rmin) + y)
				glVertex3f (depth, xbase*( 1 *abs(cos(rx)+2)) + x, (ybase * rmax ) +y)
			else :		
				glVertex3f(depth, xbase * rmin + x ,(ybase * rmin) + y)
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )
		if (mylat==1):
			if  (xbase >= 0 ) : 
				glVertex3f(depth, xbase * rmin + x ,(ybase * rmin) + y)
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )
			else :		
				glVertex3f(depth, xbase *( 1 *abs(cos(rx)+2)) + x ,(ybase * rmin) + y)
				glVertex3f(depth,xbase*( 1 *abs(cos(rx)+2)) + x, (ybase * rmax ) +y )
		if (mylat==2):
				glVertex3f(depth, xbase *( 1 *abs(cos(rx)+2)) + x ,(ybase * rmin) + y)
				glVertex3fdepth,(xbase*( 1 *abs(cos(rx)+2)) + x, (ybase * rmax ) +y )
	if (myscene ==3):
		if (mylat==0):
			if  (xbase >= 0 ) : 
				glVertex3f(depth, xbase * (1 + 0.75 *abs((cos(ry)+1))) + x ,(ybase * rmin) + y )
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )
			else :		
				glVertex3f(depth, xbase * rmin + x ,(ybase * rmin) + y)
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )
		if (mylat==1):
			if  (xbase >= 0 ) : 
				glVertex3f(depth, xbase * rmin + x ,(ybase * rmin) + y)
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )
			else :		
				glVertex3f(depth, xbase * (1 + 0.75 *abs((cos(ry)+1))) + x ,(ybase * rmin) + y )
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y , 0)
		if (mylat==2):
				glVertex3f(depth, xbase * (1 + 0.75 *abs((cos(ry)+1))) + x ,(ybase * rmin) + y )
				glVertex3f(depth, xbase * rmax + x ,(ybase * rmax ) +y )

	if (myscene ==4):
		if y ==1 :
			if  (xbase >= 0 ):
				if ( (xbase*var <= rmax) and (xbase*var <= (dist/2)) ):
					#print "var1 =",var
					glVertex3f(depth, xbase * var + placex ,ybase * rmin)
					glVertex3f(depth, xbase * rmax + placex ,ybase * rmax )
			else :		
				glVertex3f(depth, xbase * rmin + placex ,ybase * rmin)
				glVertex3f(depth, xbase * rmax + placex ,ybase * rmax )
		if y ==-1 :
			if  (xbase <= 0 ):
				if ( ( (xbase*var >= -rmax) and (xbase*var >= -(dist/2)) )  ):
					#print "var2 =",var
					glVertex3f(depth, xbase * var + placex ,ybase * rmin)
					glVertex3f(depth, xbase * rmax + placex ,ybase * rmax )
			else :		
				glVertex3f(depth, xbase * rmin + placex ,ybase * rmin)
				glVertex3f(depth, xbase * rmax + placex ,ybase * rmax )

	glEnd()


