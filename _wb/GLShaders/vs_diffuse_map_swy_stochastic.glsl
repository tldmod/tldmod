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
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 0.0;
  tmpvar_4.xyz = inNormal;
  vec3 tmpvar_5;
  tmpvar_5 = normalize((matWorld * tmpvar_4).xyz);
  diffuse_light_2 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_5, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 tmpvar_6;
  tmpvar_6.w = 1.0;
  tmpvar_6.xyz = vSunColor.xyz;
  vec3 tmpvar_7;
  tmpvar_7 = (matWorldView * tmpvar_1).xyz;
  gl_Position = (matWorldViewProj * tmpvar_1);
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = inTexCoord;
  SunLight = (((
    clamp (dot (tmpvar_5, -(vSunDir.xyz)), 0.0, 1.0)
   * tmpvar_6) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_7, tmpvar_7))
   * fFogDensity))));
  ViewDir = normalize((vCameraPos - (matWorld * tmpvar_1))).xyz;
  WorldNormal = tmpvar_5;
}

