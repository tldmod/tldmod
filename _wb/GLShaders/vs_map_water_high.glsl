/* tld glsl shader -- vs_map_water_high -- by swyter */

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
uniform mat4 matWaterViewProj;
uniform vec4 vCameraPos;
uniform vec4 texture_offset;
uniform vec4 vDepthRT_HalfPixel_ViewportSizeInv;
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
varying float Fog;

uniform float time_var;

varying vec2  _worldpos;     //swy-- pass the world pos to pixel shader
varying vec2  _sawtooth_fn;  //      together with the sawtooth for sampling
varying float _triangle_fn;  //      and the synced triangle wave for masking...

void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 vWorldPos = (matWorld * tmpvar_1);
  vec4 tmpvar_5;
  tmpvar_5.w = 0.0;
  tmpvar_5.xyz = inNormal;
  vec3 tmpvar_6;
  tmpvar_6 = normalize((matWorld * tmpvar_5).xyz);
  vec3 tmpvar_7;
  tmpvar_7 = (matWorldView * tmpvar_1).xyz;
  vec4 tmpvar_8;
  tmpvar_8 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.w = tmpvar_8.w;
  diffuse_light_2.xyz = (tmpvar_8.xyz + (clamp (
    dot (tmpvar_6, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec3 tmpvar_9;
  tmpvar_9 = -(vSunDir.xyz);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (max (0.0001,
    dot (tmpvar_6, tmpvar_9)
  ) * vSunColor.xyz));
  diffuse_light_2.w = 1.0;
  vec4 tmpvar_10;
  tmpvar_10 = (matWaterViewProj * vWorldPos);
  vec2 tmpvar_11;
  tmpvar_11.x = tmpvar_10.x;
  tmpvar_11.y = -(tmpvar_10.y);
  tmpvar_3.xy = ((tmpvar_11 + tmpvar_10.w) / 2.0);
  tmpvar_3.xy = (tmpvar_3.xy + (vDepthRT_HalfPixel_ViewportSizeInv.xy * tmpvar_10.w));
  tmpvar_3.zw = tmpvar_10.zw;
  mat3 tmpvar_12;
  tmpvar_12[0] = vec3(1.0, 0.0, 0.0);
  tmpvar_12[1] = vec3(0.0, 1.0, 0.0);
  tmpvar_12[2] = vec3(0.0, 0.0, 1.0);
  gl_Position = (matWorldViewProj * tmpvar_1);
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = (inTexCoord + texture_offset.xy);
  LightDir = (tmpvar_12 * tmpvar_9);
  CameraDir = (tmpvar_12 * -(normalize(
    (vCameraPos.xyz - vWorldPos.xyz)
  )));
  PosWater = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_7, tmpvar_7))
   * fFogDensity))));


	//swy-- flowmap time-varying sawtooth and triangle
	//      functions for animating and masking the flow...

	float time_var_mod = time_var / 10.0;

	//swy-- specially tweaked functions for
	//      both (n)ormals and diffuse (t)extures...

	float sawtooth_a_n = fract(time_var_mod);
	float sawtooth_b_n = fract(time_var_mod + 0.5);

	float sawtooth_a_t = fract(time_var_mod)       - 0.5;
	float sawtooth_b_t = fract(time_var_mod + 0.5) - 0.5;

	//swy-- triangle function used for masking by lerp two samples,
	//      all that is modulated by the upper sawtooths
	float triangle_fn = abs(0.5 - sawtooth_a_n) / 0.5;

	_sawtooth_fn = vec2(sawtooth_a_t, sawtooth_b_t);
	_triangle_fn = triangle_fn;

	//       ^
	//	     '->
	//swy-- fits pretty well! took me a long while, tho!
	_worldpos = vWorldPos.xy / 374.0;
	_worldpos.x -= 0.495;
	_worldpos.y += 0.68;

	_worldpos.xy *= -1.0;
}

