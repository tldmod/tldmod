
#define USE_DIRECTX9

#define USE_NEW_TREE_SYSTEM

#define FLORA_DETAIL_FADE_MUL	(3.0f / 4.0f)

#ifdef USE_DIRECTX9
//#define USE_DEVICE_TEXTURE_ASSIGN
#define USE_FX_STATE_MANAGER
//#define USE_SHADER_CONSTANT_MANAGER
#endif

//#define USE_LIGHTING_PASS
#ifdef USE_LIGHTING_PASS
	#define USE_SEQUENTIAL_LIGHTING_CALLS
	#define MAX_LIGHTS_PER_PASS 4
#endif

inline float get_wave_height(const float pos[2], const float coef, const float freq1, const float freq2, const float time)
{
	return coef * sin( (pos[0]+pos[1]) * freq1 + time) * cos( (pos[0]-pos[1]) * freq2 + (time+4));;
}


//#define USE_SHARED_DIFFUSE_MAP
#define USE_REGISTERED_SAMPLERS


#ifdef USE_REGISTERED_SAMPLERS

//STR: order is important for performance! (after fx_MeshTextureSampler_Register, all sampler assigned to "diffuse_texture")
#define fx_ReflectionTextureSampler_Register 		0
#define fx_EnvTextureSampler_Register				1
#define fx_Diffuse2Sampler_Register 				2
#define fx_NormalTextureSampler_Register			3
#define fx_SpecularTextureSampler_Register 		 	4
#define fx_DepthTextureSampler_Register 			5
#define fx_CubicTextureSampler_Register 			6
#define fx_ShadowmapTextureSampler_Register 		7
#define fx_ScreenTextureSampler_Register			8
#define fx_MeshTextureSampler_Register 				9
#define fx_ClampedTextureSampler_Register 			10
#define fx_FontTextureSampler_Register 				11
#define fx_CharacterShadowTextureSampler_Register	12
#define fx_MeshTextureSamplerNoFilter_Register 		13
#define fx_DiffuseTextureSamplerNoWrap_Register 	14
#define fx_GrassTextureSampler_Register 			15


// s# like versions for fx files
#define fx_ReflectionTextureSampler_RegisterS 		s0
#define fx_EnvTextureSampler_RegisterS				s1
#define fx_Diffuse2Sampler_RegisterS 				s2
#define fx_NormalTextureSampler_RegisterS			s3
#define fx_SpecularTextureSampler_RegisterS 		s4
#define fx_DepthTextureSampler_RegisterS 			s5
#define fx_CubicTextureSampler_RegisterS 			s6
#define fx_ShadowmapTextureSampler_RegisterS 		s7
#define fx_ScreenTextureSampler_RegisterS			s8
#define fx_MeshTextureSampler_RegisterS 			s9
#define fx_ClampedTextureSampler_RegisterS 			s10
#define fx_FontTextureSampler_RegisterS 			s11
#define fx_CharacterShadowTextureSampler_RegisterS	s12
#define fx_MeshTextureSamplerNoFilter_RegisterS 	s13
#define fx_DiffuseTextureSamplerNoWrap_RegisterS 	s14
#define fx_GrassTextureSampler_RegisterS 			s15
                                               
#endif