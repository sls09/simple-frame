from source import Member
from PIL import image 
im = Image.open("helper.png")
im.show()

#when running the program, an image of the frame structure will appear. More info about the frame structure is shown in the 'README.md' section.
print("Make sure you are consistant with units e.g. Newton,meters or Newton,mm or lb,in etc.\n\n\n")
member_list = []
#list
def ini_member(i):
    """initializing 3 instances of member class for 2 legged frame"""
    param_string = input("Enter coma separated values of s,p,x,w1,w2,l in given order for member {}: \n".format(i))
    s,p,x,w1,w2,l = param_string.split(",")
    mem = Member(float(s.strip()), float(p.strip()), float(x.strip()), float(w1.strip()), float(w2.strip()), float(l.strip()))
    member_list.append(mem)

'''Initiating three instance of our member class'''
'''In future if more members of a frame is to analyzed, then one needs to chage only the number of members and the end reactions region in this script. No need to change the member class'''
for ii in range(1,4):
    ini_member(ii)

m1 = member_list[0]
m2 = member_list[1]
m3 = member_list[2]
dx = m3.s - m1.s #Differnce between height of Member1 and Member2

'''Calculating vertical reaction of roller support by taking summation of moments about B1 equal to zero'''
ra = (1/m2.s) * (- m1.p * (m1.x + dx) - Member.res(m1.l, m1.w1, m1.w2) * (Member.cp(m1.l, m1.w1, m1.w2) + dx)
                 + m2.p * (m2.s - m2.x) + Member.res(m2.l, m2.w1, m2.w2) * (m2.s - Member.cp(m2.l, m2.w1, m2.w2))
                 + m3.p * (m3.s - m3.x) + Member.res(m3.l, m3.w1, m3.w2) * (m3.s - Member.cp(m3.l, m3.w1, m3.w2))
                 )
ra = round(ra, 3)

'''Finding End reactions for each member'''
a12, t12, m12 = m1.end_reactions([ra, 0, 0])
a22, t22, m22 = m2.end_reactions([t12, a12, m12])
a32, t32, m32 = m3.end_reactions([t22, a22, m22])

print("Printing End Reactions for Each Member in order (Axial, Transverse, Moment)")
print("Reactions at A1: Axial Force, Tranverse Force, Mement: " + str([ra, 0, 0]))
print("Reactions at A2: Axial Force, Tranverse Force, Mement: " + str([a12, t12, m12]))
print("Reactions at B2: Axial Force, Tranverse Force, Mement: " + str([a22, t22, m22]))
print("Reactions at B1: Axial Force, Tranverse Force, Mement: " + str([a32, t32, m32]))


'''Making Diagrams'''
figure = plt.figure(1, figsize=(15, 25))

m1_sfd = figure.add_subplot(321)
m1_sfd.set_title('Member 1 SFD')
m1_bmd = figure.add_subplot(322)
m1_bmd.set_title('Member 1 BMD')

m2_sfd = figure.add_subplot(323)
m2_sfd.set_title('Member 2 SFD')
m2_bmd = figure.add_subplot(324)
m2_bmd.set_title('Member 2 BMD')

m3_sfd = figure.add_subplot(325)
m3_sfd.set_title('Member 3 SFD')
m3_bmd = figure.add_subplot(326)
m3_bmd.set_title('Member 3 BMD')

m1_sfd.plot(m1.sections, m1.sf_ordinates())
m2_sfd.plot(m2.sections, m2.sf_ordinates())
m3_sfd.plot(m3.sections, m3.sf_ordinates())

m1_bmd.plot(m1.sections, m1.bm_ordinates(), 'r')
m2_bmd.plot(m2.sections, m2.bm_ordinates(), 'r')
m3_bmd.plot(m3.sections, m3.bm_ordinates(), 'r')

plt.show()

#Solved Example data
#10,4,3,2,2,6
#20,6,4,3,3,7
#10,6,1,2,2,7


