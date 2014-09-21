#ALGEBRATROSS!!!!!!!

#importing math functions module
import math
#importing CSV for excel format data import
import csv

#Python does not have constants so naming conventions will be used
#variables in all CAPS are CONSTANTS
ZERO = 0
UNITY = 1
PI_RAD = 3.14159
PIL2 = PI_RAD/2
TWO_PI = 2*PI_RAD
PI_32 = PI_RAD * 3/2
RQ_D = PI_RAD/180
DQ_R = 1/RQ_D
PI_DEG = 180
TWO_PID = 2*PI_DEG
PID_Q2 = PI_DEG/2
PID_ Q4 = PI_DEG/4
PI_14 = PI_RAD * 1 / 4
PI_34 = PI_RAD * 3 / 4
PI_54 = PI_RAD * 5 / 4
PI_74 = PI_RAD * 7 / 4
SPAN = 3.5
ASPECT = 16
HSPAN = 1.4
BODY_L = HSPAN/1.4

#variables
delta_x = None
delta_y = None
delta_z = None
noanhedral = None
nospar = None
noeye = None
nrwos = None
eye_to_screen = None
spare = None
xwbLe = None
ywbLe = None
zwbLe = None
xwbte = None
ywbte = None
zwbte = None
xwbsu = None
ywbsu = None
zwbsu = None
xwbsL = None
ywbsL = None
zwbsL = None
pspar = None
isok = None
eye_to_screen = None
nrows = None
x_beak = None
x_head = None
x_tail = None
x_eye = None
z_eye = None 
r_eye = None
rollLd = None
pitchd = None
yawLd_ = None
xep = None
yep = None
zep = None
xfp = None
yfp = None
zfp = None
xpro = None
ypro = None
iw = None

nws = None
nap = None
npm = None
neq = None
nwp = None
nsp = None
nbs = None
nbp = None
nee = None
#lists
xws = list()
yws = list()
zws = list()
xbm = list()
ybm = list()
zbm = list()
xeq = list()
yeq = list()
zeq = list()
xwp = list()
ywp = list()
zwp = list()
xsp = list()
ysp = list()
zsp = list()
xbs = list()
ybs = list()
zbs = list()
xee = list()
yee = list()
zee = list()
Roa = list()



def draw_bird():
	#do all the excel clearing here
	main_geom()
	irow = 0
	for k in range(1,2):
		irow = irow + 1
		for i in range(1, nwp):
			irow = irow + 1
			if(k==1):
				xx = xwp[i]
				yy = 0 + ywp[i]
				zz = zwp[i]
			else:
				xx = xwp[i]
				yy = 0 - ywp[i]
				zz = zwp[i]
			#CODE DISPLAYS CELLS HERE
	#wing sections
	irow = irow + 1
	for k in range(1,2):
		irow = irow + 1
		for i in range(1, nws):
			irow = irow + 1
			for j in range(1,nap):
				irow = irow+1
				if(k==1):
					xx = xws[i][j]
					yy = 0 + yws[i][j]
					zz = zws[i][j]
				else:
					xx = xws[i][j]
					yy = 0 - yws[i][j]
					zz = zws[i][j]
				#CODE DISPLAYS CELLS HERE
	#wing spar
	irow = irow + 1
	for k in range(1,2):
		irow = irow + 1
		for i in range(1,nsp):
			irow = irow + 1
			if(k==1):
				xx = xsp[i]
				yy = 0 + ysp[i]
				zz = zsp[i]
			else:
				xx = xsp[i]
				yy = 0 - ysp[i]
				zz = zsp[i]
				#CODE DISPLAYS CELLS HERE
				
	#body meridian
	irow = irow + 1
	for i in range(1,npm):
		irow = irow + 1
		xx = xbm[i]
		yy = ybm[i]
		zz = zbm[i]
		#CODE DISPLAYS CELLS HERE
		
	#body equator
	irow = irow + 1
	for k in range(1,2):
		irow = irow + 1
		for i in range(1,neq):
			irow = irow + 1
			if(k==1):
				xx = xeq[i]
				yy = 0 + yeq[i]
				zz = zeq[i]
			else:
				xx = xeq[i]
				yy = 0 - yeq[i]
				zz = zeq[i]
			#CODE DISPLAYS CELLS HERE
			
	#body sections
	irow = irow + 1
	for k in range(1,2):
		irow = irow + 1
		for i in range(1,nbs):
			irow = irow + 1
			for i in range(1,nbp):
				irow = irow + 1
				if(k==1):
					xx = xbs[i][j]
					yy = 0 + ybs[i][j]
					zz = zbs[i][j]
				else:
					xx = xbs[i][j]
					yy = 0 - ybs[i][j]
					zz = zbs[i][j]
				#CODE DISPLAYS CELLS HERE
				
	#eye
	irow = irow + 1
	for k in range(1,2):
		irow = irow + 1
		for i in range(1,nee):
			irow = irow + 1
			if(k==1):
				xx = xee[i]
				yy = 0 + yee[i]
				zz = zee[i]
			else:
				xx = xee[i]
				yy = 0 - yee[i]
				zz = zee[i]
			#CODE DISPLAYS CELLS HERE

def main_geom():
	#construct half-wing, half-body, wb-intersect, eye, etc
	#construct wind profile arrows
	#generate right-hand geometry arrays(x, y, z element_i, section_j)
	delta_x = -0.5
	delta_y = 0
	delta_z = 0	#-0.3
	nospar = 0
	noeye = 0
	noanhedral = 0
	wing_sections()
	body_meridian()
	body_equator()
	wing_perimeter()
	if(nospar==0):
		wing_spar()
	if(noeye==0):
		body_eye()

def wing_sections():
	#wing-body intersect and all other wing sections
	#subscripts: i=span position, j = airfoil point
	#note: make nap+1 divisible by 2
	#nws = 11: nap = 39
	#nws = 2: nap = 15
	nqbc = 15
	nws = 2
	nap = 39
	#I don't think the ReDim function is needed as Python arrays are actually lists
	#wing Le and body subscript for xyz used with wing perimeter:
	#wing spar body intersect upper and lower xyz subscripts:
	jLe = (nap + 1) / 2   # for later integer comparison
	jsu = (jLe - jLe / 3)
	jsL = (jLe + jLe / 3)
	#guess of wing te/body intersect
	para_est = 0.08
	airkap = 0
	wing(para_est, chis, xs, ys, zs, chord, omega, delta)
	airfoil(chis, xs, ys, zs, omega, delta, chord, airkap, xx, yy, zz)
	rootx = xx
	rooty = yy
	rootz = zz
	for i in range(1, nws):
		if i==1:
			para = para_est
		else:
			#theta = (i - 1) * 0.9 * pi12 / (nws - 1)
			#para = pspar + (1 - pspar) * Sin(theta)
			para = 0.515
			wing(para, chis, xs, ys, zs, chord, omega, delta)
			for j in range(1, nap):
				airkap = (j - 1) * TWO_PI / (nap - 1)
				if i==1:
					if j==1:
						intersect(airkap, rootx, rooty, rootz, xws[i][j], yws[i][j], zws[i][j])
					if j>1:
						intersect(airkap, xws[i][j - 1], yws[i][j - 1], zws[i][j - 1], xws[i][j], yws[i][j], zws[i][j])
						if(j==jLe):
							xwbLe = xws[i][j]
							ywbLe = yws[i][j]
							zwbLe = zws[i][j]
						elif j==jse:
							xwbsu = xws[i][j]
							ywbsu = yws[i][j]
							zwbsu = zws[i][j]		
							pspar = para
						elif j==jjsL:
							xwbsL = xws[i][j]
							ywbsL = yws[i][j]
							zwbsL = zws[i][j]
						elif j==nap:
							xwbte = 0.5 * (xws[1][1] + xws[1][nap])
							ywbte = 0.5 * (yws[1][1] + yws[1][nap])
							zwbte = 0.5 * (zws[1][1] + zws[1][nap])
					else:
						airfoil(chis, xs, ys, zs, omega, delta, chord, airkap, xws[i][j], yws[i][j], zws[i][j])

def wing_perimeter():
	#generate perimeter of exposed wing
	nqbc = 15
	nwp = 30
	#REDIM NOT NEEDED HERE
	for i in range(1,nwp)
	theta = pirad * (i - 1) / (nwp - 1)
	#theta = pirad * (0.005 + 0.99 * (i - 1) / (nwp - 1))
	para = Sin(theta)
	if i == 1:
		xwp[i] = xwbte
		ywp[i] = ywbte
		zwp[i] = zwbte
	elif i == nwp
		xwp[i] = xwbLe
		ywp[i] = ywbLe
		zwp[i] = zwbLe
	else
		if theta <= PIL2:
			airkap = 0
		if theta > pi12:
			airkap = pirad
		wing(para, chis, xs, ys, zs, chord, omega, delta)
		airfoil(chis, xs, ys, zs, omega, delta, chord, airkap, xx, yy, zz)
		xwp[i] = xx
		ywp[i] = yy
		zwp[i] = zz

def wing_spar():
	#generate exposed wing spar
	nsta = 13
	both = 0
	if both == 1:
		#show both the upper and lower lines of the spar:
		nsp = 2 * nsta - 1
		facts = 1
	else:
		#show only the upper line of the spar
		nsp = nsta
		facts = 0.5
	#REDIM NOT NEEDED HERE
	for i in range(1,nsp):
		theta = facts * pirad * (i - 1) / (nsp - 1)
		#minor adjustment of spar nodes
		theta = theta + 0.08 * (Sin(theta)) ^ 2
		para = Sin(theta)
		if i = 1:
			xsp[i] = xwbsu
			ysp[i) = ywbsu
			zsp[i] = zwbsu
		elif i == nsp and both > 0.5:
			xsp[i] = xwbsL
			ysp[i] = ywbsL
			zsp[i] = zwbsL
		else:
			if theta <= pi12:
				airkap = (3.3 / 5) * pirad
			if theta > pi12:
				airkap = (6.7 / 5) * pirad
			wing(para, chis, xs, ys, zs, chord, omega, delta)
			airfoil(chis, xs, ys, zs, omega, delta, chord, airkap, xx, yy, zz)
			xsp[i] = xx
			ysp[i] = yy
			zsp[i] = zz

def body_eye()
	#intersection of eye and body
	nee = 30
	#REDIM NOT NEEDED HERE
	x_eye = 0.14
	z_eye = -0.045
	r_eye = 0.008
	n13 = nee / 3
	n23 = 2 * nee / 3
	eradius = r_eye
	for i in range(1,nee):
		if i <= n13:
			eradius = r_eye
		elif i < n23:
			eradius = 2 * r_eye / 3
		else:
			eradius = r_eye / 3
		theta = 3 * twopi * (i - 1) / (nee - 2)
		xee[i] = x_eye + eradius * Cos(theta)
		zee[i] = z_eye + eradius * Sin(theta)
		body(xee[i], ye, ze, zu, zL)
		#iteration on beta
		if i == 1:
			beta = -(10 / 90) * pi12
			for j in range(1,3):
			yee[i] = (zee[i] - ze) / Tan(beta)
			station(ye, ze, zu, zL, beta, xee[i], yee[i], zz)
			beta = Atn((zz - ze) / yee[i])

def body_equator():
	#locus of max width
	neq = 130
	#REDIM NOT NEEDED HERE
	for i in range(1,neq):
		theta = pirad * (i - 1) / (neq - 1)
		xeq[i] = 0.5 * body_L * (1 - Cos(theta))
		body(xeq[i], yeq[i], zeq[i], zu, zL)

def body_meridian():
	#body profile
	npm = 130
	#REDIM NOT NEEDED HERE
	for i in range(1,npm):
		theta = twopi * (i - 1) / (npm - 1)
		xbm[i] = 0.5 * body_L * (1 - Cos(theta))
		body(xbm[i], ye, ze, zu, zL)
		if theta <= pirad:
			tops = 1
			bots = 0
		else
			tops = 0
			bots = 1
		ybm[i] = 0
		zbm[i] = tops * zu + bots * zL

def body_sections():
	#body sections
	nbp = 27
	nbs = 6
	#REDIM NOT NEEDED HERE
	for i in range(1,nbs):
		if i == 1:
			xx = 0.5 * xwbLe
		if i == 2:
			xx = 0.09 * body_L
		if i == 3:
			xx = 0.3 * body_L
		if i == 4:
			xx = xwbsu
		if i == 5:
			xx = xwbte + 0.2 * (body_L - xwbte)
		if i == 6:
			xx = xwbte + 0.6 * (body_L - xwbte)
		body(xx, ye, ze, zu, zL)
		for j in range(1,nbp):
			beta = -pi12 + (j - 1) * pirad / (nbp - 1)
			station(ye, ze, zu, zL, beta, xx, yy, zz)
			xbs[i][j] = xx
			ybs[i][j] = yy
			zbs[i][j] = zz


def intersect(airkap, xpre, ypre, zpre, xx, yy, zz):
	kmax = 3
	for k in range(1,kmax):
		if(k==1):
			g2 = ypre
		elif(k==2):
			g2 = g1 + 0.005
		else:
			g2 = (c1 - g1 * dcdg) / (1 - dcdg)

		para = g2/HSPAN
		wing(para, chis, xs, ys, zs, chord, omega, delta)
		airfoil(chis, xs, ys, zs, omega, delta, chord, airkap, xx, yy, zz)
		beta = Atan((zz-ze)/g2)
		body(xx, ye, ze, zu, zL)
		station(ye, ze, zu, zL, beta, xx, yy, zz)
		c2 = yy
		if(k>=2 and g2 != g1):
			(c2 - c1)/(g2 - g1)
		g1 = g2
		c1 = c2


def wing(para, chis, xs, ys, zs, chord, omega, delta):
	#given parametric station, get wing chord, etc
	#chis = 0.75
	#xs = 0.5
	#elevate = 0.07
	#delta = 0 * PI_RAD/180
	#ys = para * HSPAN
	#zs = elevate + ys * Tan(delta)
	#chord = 0.4 * Sqr(1-math.pow(para,2))
	#omega = 0
	
	wing half planform
	chis = 0.5
	ptip = 0.55
	xo = 0.48
	chord0 = 8 * HSPAN / (PI_RAD * 16)
	ys = para * HSPAN
	if(para < ptip):
		xs = xo - 0.05 * para + 0.03 * Sin(PI_RAD * para / ptip)
		chord = chord0
		#xs = xs + 0.04 / math.exp(13*para)
	else:
		etap = (para - ptip)/(1 - ptip)
		chord = chord0 * math.pow((1 - math.pow(etap,2),0.7)
		xs = xo + 0.07 * etap
	#anhedral with flex
	if(noanhedral < 0.5):
		zs = -0.35 * math.pow(para,3) + 0.15 * math.pow(para,6)
	else:
		zs = 0
	delta = 0
	omega = 0

def airfoil(chis, xs, ys, zs, omega, delta, chord, airkap, xx, yy, zz):
	yy = ys
	xL = xs - chis * chord
	xm = xL + chord / 2
	xx = xm + 0.5 * chord * math.cos(airkap)
	chi = (xx - xL) / chord
	if(chi > 0 and chi < 1):
		camber = 0.04 * (chord / 0.4) * math.sin(PI_RAD * math.pow((1 - chi),1.5))
	else:
		camber = 0
	half_thick = 0.045 * chord * math.sin(PI_RAD * math.pow(chi,0.5))
	if(airkap <= PI_RAD):
		zz = zs + camber + half_thick
	else:
		zz = zs + camber - half_thick
		
def body(xx, ye, ze, zu, zL):
# given x, get meridian and equator info
#
#etae = abs(0.5 * BODY_L - xx) / (0.5 * BODY_L)
#ye = 0.13 * math.sqrt(1 – math.pow(etae, 2)
#ze = 0
#etam = xx / BODY_L
#zu = ze + 0.2 * math.sin(PI_RAD * math.pow(etam, 0.5)
#zL = ze - 0.1 * math.sin(PI_RAD * math.pow(etam, 0.5)
#
# body meridian and equator ---------------------
  x_beak = 0.1; x_head = 0.14; x_tail = 0.8; onemt = 1 - x_tail
  factd = 17 / 21; factw = 22 / 30; t_e = 0.96; oneme = 1 - t_e
# upper meridian and equator, downstream of beak -----------------
  ff = 1 - xx
  zu = 0.003 + 0.47 * math.pow(ff, 2) - 0.57 * math.pow(ff, 3)
# hunchback adder
  zu = zu + 0.01 * math.exp(-100 * math.pow ((xx - 0.44), 2))
  ze = -0.14 * math.pow(ff, 10)
  if xx < x_head:
# beak profile "adders"
      zu = zu - 0.08 * (1 - math.exp(-300 * math.pow((x_head - xx), 2)))
      zu = zu + 0.03 * math.sin(PI_RAD * math.pow ((xx / x_head), 0.3))
# equator profile passes through tail, wing, eyebrow, and beak
      ze = ze - 0.04 * (1 - math.exp(-700 * math.pow ((x_head - xx), 2)))
# lower meridian -----------------------------------------------
  zL1 = -0.003 - 0.2 * math.pow ((1 – xx, 3)) + 0.06 * math.sin(PI_RAD * math.pow(ff, 5))
  zL2 = 0.05 * math.sin(PI_RAD * math.pow(xx, 4)) + 0.028 / math.exp(6 * math.sqrt(xx))
  zL = zL1 + zL2
# modify all of the above for less body depth
  zu = factd * zu; ze = factd * ze; zL = factd * zL
# half-equator planform ----------------------------------------
  a1 = 0.068403; a2 = 2.2798; a3 = -5.1163; a4 = 2.9562
  if xx < x_tail: 
      ye = a1 * xx + a2 * math.pow(xx, 2) + a3 * math.pow(xx, 3) + a4 * math.pow(xx, 4)
# eyebrow bump
      ye = ye + 0.017 / math.exp(800 * math.pow(abs(xx - 0.16), 2))
# beak horizontal thickness
      if xx < x_head:
#   ye = ye + 0.015 * math.sin(PI_RAD * math.pow ((xx / x_head), 0.5))
          ye = ye + 0.013 * math.sin(PI_RAD * math.pow ((xx / x_head), 0.4))
  else:
      ye = a1 * x_tail + a2 * math.pow(x_tail, 2) + a3 * math.pow(x_tail, 3) + a4 *math.pow( x_tail, 4)
# tail fan
      ye = ye + 0.17 * (xx - x_tail)

  if xx >= t_e:
      ye = ye * math.sqrt(ff / oneme)
# adder for thighs
  ye = ye + 0.015 * math.exp(-150 * math.pow ((xx - 0.68), 2))
  ye = factw * ye
  
def station(ye, ze, zu, zL, beta, xx, yy, zz):
# given beta and local body envelope, get coordinates
  adzu = zu - ze
  adzL = ze - zL
  if beta <= 0:
      yy = ye / math.sqrt(1 + math.pow ((ye / adzL), 2) * math.pow ((math.tan(beta)), 2))
      zz = ze - adzL * math.sqrt(1 - math.pow ((yy / ye), 2))
  else:
      yy = ye / math.sqrt(1 + math.pow ((ye / adzu), 2) * math.pow ((math.tan(beta)), 2))
      zz = ze + adzu * math.sqrt(1 - math.pow ((yy / ye), 2))
  
def maneuver_and_view():
# 3D transformation, right hand rule for xyz-axes and rotations
# geom aero axes (x-aft, y-spanwise, z-up), aircraft rotated, fixed observer and focus point
# world screen axes (origin screen center, y-up, z-axis out of screen)
# allocate geom and transform rotation matrices
  isok = 1
# screen view parameters
  eye_to_screen = 2 #1
# maneuver angles:
  rollLd = Cells(4, 6)
  pitchd = Cells(7, 6)
  yawLd_ = Cells(10, 6)
# maneuver rotation:
  define_native_rotation_transform
# set/get observer and focal points
  xep = 0; yep = 0; zep = Cells(13, 6)
  xfp = 0; yfp = 0; zfp = 0
#
  for i in range(2, nrows):
      if Cells(i, 3): 
          xo = Cells(i, 3); yo = Cells(i, 4); zo = Cells(i, 5)
          apply_all_transforms(xo, yo, zo, xv, yv, zv, xp, yp)
          Cells(i, 7) = xv; Cells(i, 8) = yv; Cells(i, 9) = zv
          Cells(i, 10) = xp; Cells(i, 11) = yp
#
 
def apply_all_transforms(xxo, yyo, zzo, xxv, yyv, zzv, xp, yp):
# conduct all transformations, each point of each object:
# native rotation (and animation if applicable)
# translate before rotation
  apply_native_rotation_transform(xxo, yyo, zzo, xxv, yyv, zzv)
# perspective transform
  apply_perspective_transform(eye_to_screen, xxv, yyv, zzv, xp, yp, ok_new)
  
def define_native_rotation_transform():
# post-animation maneuver transformation matrix,
# subscript (o) original, (a) animated
# [xa ya za]^T = [Roa][xo yo zo]^T
# 3x3 matrices here include unused "zeroth" elements now req’d by VB
# use "1 to n" logic, ignoring the 0th element
# rotation series, right-hand-rule, positive looking along axis:
# 1. roll (L-wing-down) about native (body) x-axis (which points aft)
# 2. pitch up about native (R-wing) y-axis
# 3. yaw (nose left) about native ("up") z-axis
# 4. roll right 90-deg to translate from aero to world coordinates
# rotation matrix product has rotations 4,3,2,1, left to right
# rotation:   1           2           3           4
  ReDim Roa(3, 3), Rchi(3, 3), Rpsi(3, 3), Rzet(3, 3), Tchi(3, 3)
  sinchi = math.sin(RQ_D * rollLd); coschi = math.cos(RQ_D * rollLd)
  sinpsi = math.sin(RQ_D * pitchd); cospsi = math.cos(RQ_D * pitchd)
  sinzet = math.sin(RQ_D * yawLd_); coszet = math.cos(RQ_D * yawLd_)
  sinch_ = math.sin(RQ_D * (-90));  cosch_ = math.cos(RQ_D * (-90))
  Rchi(1, 1) = 1;       Rchi(1, 2) = 0;       Rchi(1, 3) = 0
  Rchi(2, 1) = 0;       Rchi(2, 2) = coschi;  Rchi(2, 3) = -sinchi
  Rchi(3, 1) = 0;       Rchi(3, 2) = sinchi;  Rchi(3, 3) = coschi
  Rpsi(1, 1) = cospsi;  Rpsi(1, 2) = 0;       Rpsi(1, 3) = sinpsi
  Rpsi(2, 1) = 0;       Rpsi(2, 2) = 1;       Rpsi(2, 3) = 0
  Rpsi(3, 1) = -sinpsi; Rpsi(3, 2) = 0;       Rpsi(3, 3) = cospsi
  Rzet(1, 1) = coszet;  Rzet(1, 2) = -sinzet; Rzet(1, 3) = 0
  Rzet(2, 1) = sinzet;  Rzet(2, 2) = coszet;  Rzet(2, 3) = 0
  Rzet(3, 1) = 0;       Rzet(3, 2) = 0;       Rzet(3, 3) = 1
  Tchi(1, 1) = 1;       Tchi(1, 2) = 0;       Tchi(1, 3) = 0
  Tchi(2, 1) = 0;       Tchi(2, 2) = cosch_;  Tchi(2, 3) = -sinch_
  Tchi(3, 1) = 0;       Tchi(3, 2) = sinch_;  Tchi(3, 3) = cosch_
  for ii in range(1, 3):
      for jj in range(1, 3):
          Roa(ii, jj) = 0   # initialized
          for kk in range(1, 3):
              for LL in range(1, 3):
                  for mm in range(1, 3):      # rotation:   4              3              2              1
                      Roa(ii, jj) = Roa(ii, jj) + Tchi(ii, kk) * Rzet(kk, LL) * Rpsi(LL, mm) * Rchi(mm, jj)
   
def apply_native_rotation_transform(xxo, yyo, zzo, xxa, yya, zza):
# rotation about aircraft body axes and body origin (roll, pitch, then yaw)
# [xa,ya,za]^T = [Roa] [xo,yo,zo]^T
  xxa = Roa(1, 1) * xxo + Roa(1, 2) * yyo + Roa(1, 3) * zzo
  yya = Roa(2, 1) * xxo + Roa(2, 2) * yyo + Roa(2, 3) * zzo
  zza = Roa(3, 1) * xxo + Roa(3, 2) * yyo + Roa(3, 3) * zzo



def Atan2(xx, yy):
	if xx == 0 and yy == 0:
		ans = 0
	elif xx == 0 and yy > 0:
		ans = 3.14159/2
	elif xx == 0 and yy < 0:
		ans = -3.14159/2
	elif xx > 0:
		ans = math.atan(yy/xx)
	else:
		ans = math.atan(yy/xx) + 3.14159
	return ans

def arctan(dx, dy):
	if dx == 0 and dy < 0:
		ans = -math.pi/2
	elif dx == 0 and dy > 0:
		ans = math.pi/2
	else
		ans = Atan2(dx, dy)
	return ans

def arcsin(x):
	if x = -1:
		ans = -math.pi/2
	elif x = 1:
		ans = math.pi/2
	else:
		ans = math.atan(x/math.sqrt(-x*x+1))
	return ans

def arccos(x):
	if x = -1:
		ans = math.pi
	elif x = 1:
		ans = 0
	else:
		ans = math.atan(-x/math.sqrt(-x*x+1))+2*math.atan(1)
	return ans

def atan(xn, xd):
	ans = 0
	if xd == 0 and xn >= 0:
		ans = 3.14159/2
	if xd == 0 and xn < 0:
		ans = -3.14159/2
	if xd != 0:
		ans = math.atan(xn/xd)
	return ans

def Atan(xx, yy):
	if xx == 0 and yy < 0:
		ans - -3.14159/2
	elif xx == 0 and yy >= 0:
		ans = 3.14159/2
	else:
		ans = math.atan(yy/xx)
	return ans

def asin(xn, xd):
	ans = math.atan((xn/xd) / math.sqrt(1 - (xn/xd)**2))
	return ans

def acos(xn, xd):
	ans = math.atan(math.sqrt(1 - (xn/xd)**2) / (xn/xd))
	return ans

def valmax(x1, x2):
	max = 0
	if x1>x2:
		max = x1
	else:
		max = x2
	return max

def valmin(x1, x2):
	min = 0
	if x1<x2:
		min = x1
	else:
		min = x2
	return min
	


