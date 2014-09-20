#ALGEBRATROSS!!!!!!!
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

def wing_perimeter():

def wing_spar():

def body_eye():

def body_equator():

def body_meridian():

def body_sections():

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
		if(k>=2)


def wing(para, chis, xs, ys, zs, chord, omega, delta):

def airfoil(chis, xs, ys, zs, omega, delta, chord, airkap, xx, yy, zz):

def body(xx, ye, ze, zu, zL):

def station(ye, ze, zu, zL, beta, xx, yy, zz):

def maneuver_and_view():

def define_native_rotation_transform():

def apply_native_rotation_transform(xxo, yyo, zzo, xxa, yya, zza):

def apply_perspective_transform(_eye_to_screen, xxv, yyv, zzv, xp, yp, ok_new):


def Atan2(xx, yy):
#ans is number to be returned
	return ans

def arctan(dx, dy):

	return ans

def arcsin(x):

	return ans

def arccos(xx):

	return ans

def atan(xn, xd):

	return ans

def Atan(xx, yy):

	return ans

def asin(xn, xd):

	return ans

def acos(xn, xd):
	return ans

def valmax(x1, x2):

	return max

def valmin(x1, x2):

	return min 


