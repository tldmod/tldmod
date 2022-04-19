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
uniform mat4 matSunViewProj;
uniform vec4 vCameraPos;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying float Fog;
varying vec4 Color;
varying vec3 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec3 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4 = (matWorld * tmpvar_1);
  vec4 tmpvar_5;
  tmpvar_5.w = 0.0;
  tmpvar_5.xyz = inNormal;
  vec3 tmpvar_6;
  tmpvar_6 = normalize((matWorld * tmpvar_5).xyz);
  vec3 tmpvar_7;
  tmpvar_7 = (matWorldView * tmpvar_1).xyz;
  tmpvar_3.xy = inTexCoord;
  tmpvar_3.z = (0.7 * (tmpvar_4.z - 1.5));
  diffuse_light_2 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_6, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 tmpvar_8;
  tmpvar_8.w = 1.0;
  tmpvar_8.xyz = vSunColor.xyz;
  gl_Position = (matWorldViewProj * tmpvar_1);
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_7, tmpvar_7))
   * fFogDensity))));
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = tmpvar_3;
  SunLight = (clamp (dot (tmpvar_6, 
    -(vSunDir.xyz)
  ), 0.0, 1.0) * tmpvar_8);
  ShadowTexCoord = (matSunViewProj * tmpvar_4);
  ViewDir = normalize((vCameraPos - tmpvar_4)).xyz;
  WorldNormal = tmpvar_6;
}

