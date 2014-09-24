PI_RAD = 3.14159
TWO_PI = 2 * PI_RAD
RqD = PI_RAD / 180

  
def single_curve_airfoil():
	deLta = 0.05
	#3 point design
	tau_S = []
	chi_S = []
	chi = None
	chi0 = None
	chid = None
	chidd = None
	#hard coded "user inputs"
	tau_S.append(0.0000)
	tau_S.append(0.0300)
	tau_S.append(0.1900)
	tau_S.append(0.5000)
	tau_S.append(0.8800)
	tau_S.append(1.0000)
	tau_chi(tau_S, deLta, chi_S, chi0, chid, chidd)
	zet_S = []
	zet_S.append(0.0000)
	zet_S.append(0.0007)
	zet_S.append(-0.049)
	zet_S.append(0.0000)
	zet_S.append(0.0488)
	zet_S.append(0.0000)
	
	Np = 6 #Number of parameters
	
	#generate resulting curves and get derivatives + normals
	keL = 3
	keR = 1
	dzdt_S = []
	d2zdt2_S = []
	if(kel==2):
		dydxL = 0
	if(keR==2):
		dydxR = 0
	CS_solve(Np, tau_S, zet_S, d2zdt2_S, dzdt_S, keL, dydxL, keR, dydxR)
	
	#get coefficients for degree-n polynomial passing thru spline points
	Left_to_Right = 1
	n = Np - 1
	c = []
	X_ = []
	Y_ = []
	for i in range(0,n):
		X_[i] = tau_S[i+1]
		Y_[i] = zet_S[i+1]
	polynomial_(Left_to_Right, n, X_, Y_, c)
	
	ns = 41
	for i in range(1,ns):
		irow = i+1
		tau = (i-1) / (ns - 1)
		tau_chi(tau, deLta, chi, chi0, chid, chidd)
		CS_intrp(Np, tau_S, zet_S, d2zdt2_S, dzdt_S, tau, zeta, dzdt, d2zdt2)
		Xo = X_[0]
		Xn = X_[n]
		Yo = Y_[0]
		Yn = Y_[n]
		x = tau
		if(Left_to_Right == 1):
			y = Yo
			for j in range(1,n):
				y = y + c(j) * (x - Xo) ^ j
		else:
			y = Yn
			for j in range(1,n):
				y = y + c(j) * (x - Xn) ^ j			
		zetap = y
		
		#Leading edge radius and boattail
		if(tau == 0)
			betad = -(1 / RqD) * dzdt / chid
		elif(tau == 0.5)
			rho = dzdt ^ 2 / chidd 
		elif(tau == 1)
			betad = -(1 / RqD) * dzdt / chid

def tau_chi(tau, deLta, chi, chi0, chid, chidd):
	chi0 = 1 - math.sin(math.pi * tau) 
	
	chi = 1 - ((1 - deLta) * math.sin(math.pi * tau) + 
	deLta * math.sin(3 * math.pi * tau))
	
	chid = -((1 - deLta) * math.pi * math.cos(math.pi * tau) + 
	3 * math.pi * deLta * math.cos(3 * math.pi * tau))
	
	chidd = ((1 - deLta) * (math.pi**2) * math.sin(math.pi * tau) - 
	((3 * math.pi)**2) * deLta * math.sin(3 * math.pi * tau))	
	

def cubic_spline(nn, xx, yy, keL, dydxL, keR, dydxR, Xa, Xb, Xo, Yo, dydx, zz, area):
	CS_solve(nn, xx, yy, zz, dydx, keL, dydxL, keR, dydxR)
	CS_quadr(nn, xx, yy, zz, dydx, Xa, Xb, area)
	CS_intrip(nn, xx, yy, zz, dydx, Xo, Yo, dydxo, d2ydx2o)


def CS_solve(nn, xx, yy, zz, dydx, keL, dydxL, keR, dydxR):
	if(keL==2):
		dydxL = 0
	if(keR==2):
		dydxR = 0
	#1st and 2nd derivative arrays
  	dydx = []
  	zz = []
  	#number of splines
  	ns = nn-1
  	_del = []
  	eps = []
  	#spline length and height
  	for i in range(1, ns):
  		_del[i] = xx[i+1] - xx[i]
  		esp[i] = yy[i+1] - yy[i]
  	#generate 2D array [A][X]=[B]
  	AA = [[0 for i in xrange(nn)] for i in xrange(nn)]
  	BB = []
  	#avoid user error for edge conditions
  	if((keL < 1 or keL > 3) or (nn < 4 and keL == 3)):
  		keL = 1
  	if((keR < 1 or keR > 3) or (nn < 4 and keR == 3)):
  		keR = 1
  	#if(nn < 4 and keL == 3):
  	#	keL = 1
  	#if(nn < 4 and keR == 3):

  	#influence coefficient matrix, row i column j
  	for i in range(1, nn):
  		for j in range(1, nn):
  			#init 2d array with 0's as we traverse
  			#(should already have em but lets be safe!)
  			AA[i][j] = 0
  			#1st row (L-edge) stiff end
  			if(keL == 1 and i == 1 and j == 1):
  				#if he's hard coding the logic we could just say AA[1][1] here
  				AA[i][j] = 1
  			#1st row (L-edge) horizontal end
  			elif((keL == 0 or keL == 2) and (i == 1 and j == 1)):
  				#here too
  				AA[i][j] = _del[1] / 3
  			elif((keL == 0 or keL == 2) and (i == 1 and j == 2)):
  				AA[i][j] = _del[1] / 6
  			#1st row (L-edge) flexible end
  		elif(keL == 3 and i == 1 and j == 1):
  			AA[i][j] = 1
  		elif(keL == 3 and i == 1 and j == 2):
  			AA[i][j] = -1 - _del[1] / _del[2]
  		elif(keL == 3 and i == 1 and j == 3):
  			AA[i][j] = _del[1]/_del[2]
  		#mid row (all options)
  		elif(i > 1 and i < nn):
  			if(j == i-1):
  				AA[i][j] = _del[i-1] / 6
  			elif(j == i):
  				AA[i][j] = (_del[i-1] + _del[i]) / 3
  			elif(j == i + 1):
  				AA[i][j] = _del[i] / 6
  		#nth row (R-edge) stiff end
  		elif(keR == 1 and i == nn and j == nn):
  			AA[i][j] = 1
  		#nthr row (R-edge) horizontal end
  		elif((keR == 0 or keR == 2) and i == nn and j == nn - 1):
  			AA[i][j] = -_del[ns] / 6
  		elif((keR == 0 or keR == 2) and i == nn and j == nn - 0):
  			AA[i][j] = -_del[ns] / 3
  		#nth row (R-edge) flexible end
  		elif(keR == 3 and i == nn and j == nn):
  			AA[i][j] = 1
  		elif(keR == 3 and i == nn and j == nn - 1):
  			AA[i][j] = -1 - _del[nn-1] / _del[nn-2]
  		elif(keR == 3 and i == nn and j == nn - 2):
  			AA[i][j] = _del[nn-1] / _del[nn-2]
  	#init boundary conditions
  	BB[i]=0
  	#1st row (L-edge) stiff end
  	if(keL == 1 and i == 1):
  		BB[i] = 0
  	#1st row (L-edge) horizontal end
  	elif((keL == 0 or keL == 2) and i == 1):
  		BB[i] = esp[1] / _del[1] - dydxL
  	#1st row (L-edge) flexible end
  	elif(keL == 3 and i == 1):
  		BB[i] = 0
  	#mid row (all options)
 	elif(i > 1 and i < nn):
 		BB[i] = esp[i] / _del[i] - esp[i-1] / _del[i-1]
 	#nth row (R-edge) stiff end
 	elif(keR == 1 and i == nn):
 		BB[i] = 0
 	#nth row (R-edge) horizontal end
 	elif((keR == 0 or keR == 2) and i == nn):
 		BB[i] = esp[ns] / _del[ns] - dydxR
 	#nth row (R-edge) flexible end
 	elif(keR == 3 and i == nn):
 		BB[i] = 0
 #solution for 2nd derivatives, includes aux arrays
 Gauss(nn, AA, iL, ss)
 Solve(nn, AA, iL, BB, zz)

 #1st derivateves
 for i in range(1, nn):
 	if(i < nn):
 		dydx[i] = eps[i] / _del[i] - zz[i] * _del[i] / 3 - zz[i + 1] * _del[i] / 6
 	else:
 		dydx[i] = dydx[ns] + zz[ns] * _del[ns] / 2 + zz[nn] * _del[ns] / 2

  
def CS_quadr(nn, xx, yy, zz, dydx, Xa, Xb, area):
	
	ns = nn - 1
	delx = []
	eps = []
	
	#Spline length and height
	for i in range (i, ns):
		delx.insert(i, xx[i + 1] - xx[i])
		eps.insert(i, yy[i + 1] - yy[i])
		
		#Initialize
		area = 0
		
		#Begin with full splines
		for i in range (i, ns):
			if Xa <= xx(i) and Xb >= xx(i + 1):
				area = ( area +
				yy(i) * delx[i] + dydx(i) * ((delx[i]**2)/2) +
				zz(i) * ((delx[i]**3)/6) +
				(zz(i+1) - zz(i)) * ((delx[i]**3)/24))
		
			#Partial spline, xa
			if Xa > xx(i) and Xa < xx(i + 1):
				area = (area +
				yy(i) * delx[i] + dydx(i) * ((delx[i]**2)/2) +
				zz(i) * ((delx[i]**3)/6) +
				(zz(i + 1) - zz(i)) * ((delx[i]**3)/24) -
				yy(i) * (Xa - xx(i)) + dydx(i) * (((Xa - xx(i))**2)/2) -
				zz(i) * (((Xa - xx(i))**3)/6) -
				(zz(i + 1) - zz(i)) * ((Xa - xx(i))**4)/(24 * delx[i]))
 
			#Partial spline, xb
			if Xb > xx(i) and Xb < xx(i + 1):
				area = (area +
				yy(i) * (Xb - xx(i)) + dydx(i) * (((Xb - xx(i))**2)/2) +
				zz(i) * (((Xb - xx(i))**3)/6) +
				(zz(i + 1) - zz(i)) * (((Xb - xx(i)**4))/2))
			
			#Correct for overlap condition
			if Xa >= xx(i) and Xb <= xx(i + 1):
				area = (area -
				yy(i) * delx[i] + dydx(i) * ((delx[i]**2)/2) -
				zz(i) * ((delx[i]**3)/6) -
				(zz(i + 1) - zz(i)) * ((delx[i]**3)/24))

			#Extrapolate left and/or right
			if Xa < xx(i):
				area = area + (xx(1) - Xa) * 0.5 * (2 * yy(1) - dydx(1) * (xx(1) - Xa))
				
			if Xb > xx(nn):
				area = area + (Xb - xx(nn)) * 0.5 * (2 * yy(nn) + dydx(nn) * (Xb - xx(nn)))	
	
	
def CS_intrp(nn, xx, yy, zz, dydx, Xo, Yo, dydxo, d2ydx2o) #PROBABLY NOT DONE I THINK I DID STUFF WRONG WHAT IS del(i)??
# Cubic spline interpolation module
# Interp. Yo(Xo) & get dy/dx, d2y/dx2 at Xo, incl. linear extrap. if req'd
# All above are inputs, except the results: (Yo, dydxo, & d2ydx2o)
# Phil Barnes, Feb 2009, Public Domain, www.HowFliesTheAlbatross.com
  ns = nn - 1: ReDim del(ns), eps(ns) # ns = # of splines for nn points
# spline horizontal and vertical excursions:
#was changed from insert to append.. insert requires index
  for i in range (1, ns):
  	_del.append(i, xx[i + 1] - xx[i]
  	eps.append(i, yy[i + 1] - yy[i])
  
  if (Xo < xx[1]):
# linear extrapolate left
       Yo = yy[1] + dydx[1] * (Xo - xx[1])
       dydxo = dydx[1] + zz[1] * (Xo - xx[1])
       d3ydx3 = (zz[2] - zz[1]) / _del[1]       # 3rd derivative
       d2ydx2o = zz[1] + d3ydx3 * (Xo - xx[1])
  elif (Xo > xx[nn]):
# linear extrapolate right
       Yo = yy[nn] + dydx[nn] * (Xo - xx[nn])
       dydxo = dydx[nn] + zz[nn] * (Xo - xx[nn])
       d3ydx3 = (zz[nn] - zz[nn - 1]) / _del[ns]  # 3rd derivative
       d2ydx2o = zz[1] + d3ydx3 * (Xo - xx[1])
  else: # find applicable spline and interpolate
  	for i in range (1, ns):
      		if xx[i + 1] >= Xo:  # first get shorthand terminology:
        		xmxi = Xo - xx[i]
        		epsi = eps[i] 
        		deli = del[i]
        		yyi = yy[i]
        		zzi = zz[i]
        		dydxi = dydx[i]
        		zip1 = zz[i + 1]
        		#** = ^
        		Yo = yyi + dydxi * xmxi + zzi * xmxi ** 2 / 2 + (zip1 - zzi) * xmxi ** 3 / (6 * deli)
        		dydxo = dydxi + zzi * xmxi + (zip1 - zzi) * xmxi ** 2 / (2 * deli)
        		d2ydx2o = zzi + (zip1 - zzi) * xmxi / deli


def Gauss (n, A, L, s):
	for i in range (1,n):
		L[i] = i
		smax = 0
		for j in range (1,n):
			if (math.abs(A[i,j] > smax):
				smax = math.abs(A[i,j])
		s[i] = smax
		
	for k in range(1,n):
		rmax = 0
		for i in range(k,n):
			R = (math.abs(A[L[i],k]/s[L[i]]))
			if (R > rmax):
				j = i
				rmax = R
		Lk = L[j]
		L[j] = L[k]
		L[k] = Lk
		for i in range(k+1,n):
			xm = (A[L[i],k])/A[Lk,k]
			for j in range(k+1,n):
				A[L[i],j] = A[L[i],j] - xm*A[Lk,j]
			A[L[i],k] = xm
  
def Solve (n, A, L, B, x):
	for k in range(1,n-1):
		for i in range(k+1,n):
			B[L[i]] = (B[L[i]] - A[L[i],k] * B[L[k]])
	x[n] = B[L[n]] / A[L[n],n]
	for i in range(n-1,1,-1):
		Sum = B[L[i]]
		for j in range(i+1,n):
			Sum = (Sum - (A[L[i],j]*x[j]))
		x[i] = Sum / A[L[i],i]

def polynomial_(Left_to_Right, n, X_(), Y_(), c()):

