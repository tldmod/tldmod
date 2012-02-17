####################################################################################################################
#  Each postfx_param contains the following fields:
#  1) id (string): 
#  2) flags (int). 
#  3) tonemap operator type (0,1,2,3)
#  4) shader parameters1 [ HDRRange, HDRExposureScaler, LuminanceAverageScaler, LuminanceMaxScaler ]
#  5) shader parameters2 [ BrightpassTreshold, BrightpassPostPower, BlurStrenght, BlurAmount ]
#  6) shader parameters3 [ AmbientColorCoef, SunColorCoef, SpecularCoef, -reserved ]
# 
	#define postfxParams1	(PFX1)	float4(postfx_editor_vector[1].x, postfx_editor_vector[1].y, postfx_editor_vector[1].z, postfx_editor_vector[1].w) 
	#define postfxParams2	(PFX2)	float4(postfx_editor_vector[2].x, postfx_editor_vector[2].y, postfx_editor_vector[2].z, postfx_editor_vector[2].w)
	#define postfxParams3	(PFX3)	float4(postfx_editor_vector[3].x, postfx_editor_vector[3].y, postfx_editor_vector[3].z, postfx_editor_vector[3].w)

####################################################################################################################
fxf_highhdr        = 0x00000001


postfx_params = [
 ("default", 0, 0, [125.9922, 1.0588, 1.4510, 9.1765], [0.9608, 1.1373, 1.1373, 0.1961], [1.0, 1.0, 1.0, 1.0000]),
 ("map_params", 0, 3, [128.0000, 1.04, 1.2941, 10.0000], [2.3725, 2.1569, 1.8431, 0.4863], [1.0, 1.0, 1.05, 1.0]),
 ("indoors", 0, 0, [128.0000, 1.0, 1.2549, 10.0000], [0.6471, 4.7843, 4.1616, 0.00155], [0.9804, 0.9804, 1.5294, 1.0000]),
 ("sunset", 0,  0, [128.0000, 0.5882, 0.9804, 0.9804], [0.0784, 2.1176, 1.3725, 0.1255], [0.9804, 0.9804, 1.7647, 1.0000]),
 ("night", 0, 0, [128.0000, 1.0, 1.2549, 10.0000], [0.6471, 4.7843, 1.2157, 0.0000], [0.9804, 0.9804, 1.5294, 1.0000]),
 #("sunny", 0, 0, [128.0000, 0.6667, 0.9804, 0.9804], [0.4510, 2.4314, 1.2941, 0.1412], [0.9804, 0.9804, 1.4118, 1.0000]),
 # ("sunny", 0, 1, [128.0000, 1.0, 0.9804, 0.9804], [1.2157, 2.4314, 1.3333, 0.1412], [1.0196, 1.0804, 1.4314, 1.0000]) ,
 ("sunny", 0,  0, [128.0000, 0.5882, 0.9804, 0.9804], [0.0784, 2.1176, 1.3725, 0.1255], [0.9804, 0.9804, 1.7647, 1.0000]),
 ("cloudy", 0, 0, [128.0000, 1.0, 0.9804, 0.0000], [0.3137, 2.6667, 2.0000, 0.4314], [0.9804, 0.9804, 1.4314, 1.0000]) ,
 ("overcast", 0, 0, [128.0000, 1.0, 0.9804, 0.0000], [0.3137, 2.6667, 2.0000, 0.0], [0.9804, 0.9804, 1.0314, 1.0000]) ,
 
 
 ("high_contrast", 0, 3, [128.0000, 1.0000, 1.2941, 10.0000], [0.4314, 2.0000, 1.0588, 0.0549], [2.0000, 0.7059, 1.4902, 1.0000]), 
  ]
