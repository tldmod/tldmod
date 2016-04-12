uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightDir;
uniform vec4 vSkyLightColor;
uniform float fFogDensity;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform vec4 vLightPosDir[4];
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;

uniform float time_var;

#define swy_rohan_banners true
#define swy_spr_banners false

void main ()
{
    vec3 vPosition = inPosition;
    vec2 tc = inTexCoord.xy; tc.y = 1.0-tc.y;

	//swy-- constants, tailored constants everywhere! :)
	if(swy_rohan_banners)
	{

	 //swy-- if not metal thingy
	 if(tc.x < 0.944f)
	 {
		float seed = time_var + (vPosition.x/vPosition.y/vPosition.z);
		float v_modulator;

		//swy-- special codepath for sideways banner, modulating the waving vertically/horizontally by UVs. sigh :(
		if(tc.x < 0.547f && tc.y > 0.789f)
		{
			v_modulator = tc.x * 0.5f;
		}

		else
		{
			v_modulator = tc.y;
		}

		vPosition.y += ((sin(seed+cos(vPosition.x))*0.4f)* v_modulator*vPosition.x)/vPosition.z;
	 }
	}

   //swy-- per-pixel sampling for per-vertex shaders, now that's performant! :)
   if(swy_spr_banners)
   {
	 //swy-- if not metal thingy
	 if(tc.x <= (244.f/256.f))
	 {
		float seed = time_var + (vPosition.x + vPosition.y + tc.x + tc.y) + matWorld[0][3];
		float thingie  = sin(seed + cos(vPosition.x)) * fract(tc.y*3.f) /* * abs(vPosition.x) */;
		      thingie *= 0.2f;

		vPosition.y += -(abs(thingie)*abs(thingie));
		vPosition.x += thingie*0.3f;
	 }
   }


  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = vPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_5;
  tmpvar_5.w = 0.0;
  tmpvar_5.xyz = inNormal;
  vec3 tmpvar_6;
  tmpvar_6 = normalize((matWorld * tmpvar_5).xyz);
  diffuse_light_2 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_6, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_7;
  vWorldPos_7 = (matWorld * tmpvar_1);
  vec3 vWorldN_8;
  vWorldN_8 = tmpvar_6;
  vec4 total_10;
  total_10 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_9 = 0; j_9 < iLightPointCount; j_9++) {
    int tmpvar_11;
    tmpvar_11 = iLightIndices[j_9];
    vec3 tmpvar_12;
    tmpvar_12 = (vLightPosDir[tmpvar_11].xyz - vWorldPos_7.xyz);
    total_10 = (total_10 + ((
      clamp (dot (vWorldN_8, normalize(tmpvar_12)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_11]) * (1.0/(
      dot (tmpvar_12, tmpvar_12)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_10);
  vec4 tmpvar_13;
  tmpvar_13.w = 1.0;
  tmpvar_13.xyz = vSunColor.xyz;
  vec3 tmpvar_14;
  tmpvar_14 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_14, tmpvar_14))
   * fFogDensity))));
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = inTexCoord;
  SunLight = (((
    clamp (dot (tmpvar_6, -(vSunDir.xyz)), 0.0, 1.0)
   * tmpvar_13) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = tmpvar_4;
}

