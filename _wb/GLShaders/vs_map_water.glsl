uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightDir;
uniform vec4 vSkyLightColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform vec4 vCameraPos;
uniform vec4 texture_offset;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying vec3 LightDir;
varying vec3 CameraDir;
varying vec4 PosWater;

varying  vec2 worldpos;      //swy-- pass the world pos to pixel shader
varying  vec2 sawtooth_fn;   //      together with the sawtooth for sampling
varying float triangle_fn;   //      and the synced triangle wave for masking...

uniform sampler2D diffuse_texture_2;
uniform float time_var;

varying float Fog;

void main ()
{
  vec4 vPosition;
  vPosition.w = 1.0;
  vPosition.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 vWorldPos = (matWorld * vPosition);
  vec4 tmpvar_4;
  tmpvar_4.w = 0.0;
  tmpvar_4.xyz = inNormal;
  vec3 tmpvar_5;
  tmpvar_5 = normalize((matWorld * tmpvar_4).xyz);
  vec3 tmpvar_6;
  tmpvar_6 = (matWorldView * vPosition).xyz;
  vec4 tmpvar_7;
  tmpvar_7 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.w = tmpvar_7.w;
  diffuse_light_2.xyz = (tmpvar_7.xyz + (clamp (
    dot (tmpvar_5, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec3 tmpvar_8;
  tmpvar_8 = -(vSunDir.xyz);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (max (0.0001, 
    dot (tmpvar_5, tmpvar_8)
  ) * vSunColor.xyz));
  diffuse_light_2.w = 1.0;
  mat3 tmpvar_9;
  tmpvar_9[0] = vec3(1.0, 0.0, 0.0);
  tmpvar_9[1] = vec3(0.0, 1.0, 0.0);
  tmpvar_9[2] = vec3(0.0, 0.0, 1.0);
  gl_Position = (matWorldViewProj * vPosition);
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = (inTexCoord + texture_offset.xy);
  LightDir = (tmpvar_9 * tmpvar_8);
  CameraDir = (tmpvar_9 * -(normalize(
    (vCameraPos.xyz - (matWorld * vPosition).xyz)
  )));
  PosWater = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_6, tmpvar_6))
   * fFogDensity))));

  //swy-- flowmap time-varying sawtooth and triangle
	//      functions for animating and masking the flow...
	
	float time_var_mod = time_var / 10.;
	
	//swy-- specially tweaked functions for
	//      both (n)ormals and diffuse (t)extures...
	
	float sawtooth_a_n = fract(time_var_mod);
	float sawtooth_b_n = fract(time_var_mod + 0.5);
	
	float sawtooth_a_t = fract(time_var_mod)       - 0.5;
	float sawtooth_b_t = fract(time_var_mod + 0.5) - 0.5;

	//swy-- triangle function used for masking by lerp two samples,
	//      all that is modulated by the upper sawtooths
	triangle_fn = abs(0.5 - sawtooth_a_n) / 0.5;
	
	sawtooth_fn = vec2(sawtooth_a_t, sawtooth_b_t);

	//       ^
	//	     '->
	//swy-- fits pretty well! took me a long while, tho!
	worldpos = vWorldPos.xy / 374.;
	worldpos.x -= 0.495;
	worldpos.y += 0.68;
	
	worldpos.x *= -1.;
  worldpos.y *= -1.; /* swy: seems like we also need to flip the UVs vertically on OpenGL due to the way the texture gets loaded, 2022-04-08, everyone */
}

