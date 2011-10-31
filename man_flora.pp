ps.1.1

def c0, 0.6f, 0.7f, 0.6f, 1.0f
//def c1, 0.1f, 0.1f, 0.1f, 0.0f

tex t0

//mad r1, v0, c0, c1
mul r1, v0, c0

mul r0.rgb, r1, t0
mov r0.a, t0.a
