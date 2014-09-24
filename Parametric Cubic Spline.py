PI_RAD = 3.14159
TWO_PI = 2 * PI_RAD
RqD = PI_RAD / 180

  
def single_curve_airfoil():
	deLta = 0.05
	#3 point design
	tau_S = []
	#hard coded "user inputs"
	tau_S.append(0.0000)
	tau_S.append(0.0300)
	tau_S.append(0.1900)
	tau_S.append(0.5000)
	tau_S.append(0.8800)
	tau_S.append(1.0000)
	tau_chi(tau_S[i], deLta, chi_S[i], chi0, chid, chidd)
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
	CS_solve(Np, tau_S[], zet_S[], d2zdt2_S[], dzdt_S[], keL, dydxL, keR, dydxR)
	
	#get coefficients for degree-n polynomial passing thru spline points
	Left_to_Right = 1
	n = Np - 1
	c = []
	X_ = []
	Y_ = []
	for i in range(0,n):
		X_[i] = tau_S[i+1]
		Y_[i] = zet_S[i+1]
	polynomial_(Left_to_Right, n, X_[], Y_[], c[])
	
	ns = 41
	for i in range(1,ns):
		irow = i+1
		tau = (i-1) / (ns - 1)
		tau_chi(tau, deLta, chi, chi0, chid, chidd)
		CS_intrp(Np, tau_S(), zet_S(), d2zdt2_S(), dzdt_S(), tau, zeta, dzdt, d2zdt2)
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

def cubic_spline(nn, xx(), yy(), keL, dydxL, keR, dydxR, Xa, Xb, Xo, Yo, dydx(), zz(), area):

def CS_solve(nn, xx(), yy(), zz(), dydx(), keL, dydxL, keR, dydxR):
  
def CS_quadr(nn, xx(), yy(), zz(), dydx(), Xa, Xb, area):

def CS_intrp(nn, xx(), yy(), zz(), dydx(), Xo, Yo, dydxo, d2ydx2o) #PROBABLY NOT DONE I THINK I DID STUFF WRONG WHAT IS del(i)??
# Cubic spline interpolation module
# Interp. Yo(Xo) & get dy/dx, d2y/dx2 at Xo, incl. linear extrap. if req'd
# All above are inputs, except the results: (Yo, dydxo, & d2ydx2o)
# Phil Barnes, Feb 2009, Public Domain, www.HowFliesTheAlbatross.com
  ns = nn - 1: ReDim del(ns), eps(ns) # ns = # of splines for nn points
# spline horizontal and vertical excursions:
  for i in range (1, ns):
  del(i) = xx(i + 1) - xx(i): eps(i) = yy(i + 1) - yy(i)
  
  if Xo < xx(1):
# linear extrapolate left
       Yo = yy(1) + dydx(1) * (Xo - xx(1))
       dydxo = dydx(1) + zz(1) * (Xo - xx(1))
       d3ydx3 = (zz(2) - zz(1)) / del(1)       # 3rd derivative
       d2ydx2o = zz(1) + d3ydx3 * (Xo - xx(1))
  elif Xo > xx(nn):
# linear extrapolate right
       Yo = yy(nn) + dydx(nn) * (Xo - xx(nn))
       dydxo = dydx(nn) + zz(nn) * (Xo - xx(nn))
       d3ydx3 = (zz(nn) - zz(nn - 1)) / del(ns)  # 3rd derivative
       d2ydx2o = zz(1) + d3ydx3 * (Xo - xx(1))
  else: # find applicable spline and interpolate
    for i in range (1, ns):
      if xx(i + 1) >= Xo:  # first get shorthand terminology:
        xmxi = Xo - xx(i): epsi = eps(i): deli = del(i)
        yyi = yy(i): zzi = zz(i): dydxi = dydx(i): zip1 = zz(i + 1)
        Yo = yyi + dydxi * xmxi + zzi * xmxi ^ 2 / 2 + (zip1 - zzi) * xmxi ^ 3 / (6 * deli)
        dydxo = dydxi + zzi * xmxi + (zip1 - zzi) * xmxi ^ 2 / (2 * deli)
        d2ydx2o = zzi + (zip1 - zzi) * xmxi / deli


def Gauss(n, A(), L(), s()):
  
def Solve(n, A(), L(), B(), x()):

def polynomial_(Left_to_Right, n, X_(), Y_(), c()):

