uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
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
attribute vec3 inTangent;
attribute vec3 inBinormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec3 Tex0;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec3 tmpvar_4;
  vec4 tmpvar_5;
  vec3 tmpvar_6;
  vec4 tmpvar_7;
  tmpvar_7 = (matWorld * tmpvar_1);
  vec4 tmpvar_8;
  tmpvar_8.w = 0.0;
  tmpvar_8.xyz = inNormal;
  vec3 tmpvar_9;
  tmpvar_9 = normalize((matWorld * tmpvar_8).xyz);
  vec4 tmpvar_10;
  tmpvar_10.w = 0.0;
  tmpvar_10.xyz = inBinormal;
  vec4 tmpvar_11;
  tmpvar_11.w = 0.0;
  tmpvar_11.xyz = inTangent;
  mat3 tmpvar_12;
  tmpvar_12[0] = normalize((matWorld * tmpvar_11).xyz);
  tmpvar_12[1] = normalize((matWorld * tmpvar_10).xyz);
  tmpvar_12[2] = tmpvar_9;
  vec3 tmpvar_13;
  tmpvar_13 = (matWorldView * tmpvar_1).xyz;
  tmpvar_4.xy = inTexCoord;
  tmpvar_4.z = (0.7 * (tmpvar_7.z - 1.5));
  diffuse_light_2 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_9, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  tmpvar_3.xyz = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2).xyz;
  tmpvar_3.w = (vMaterialColor.w * inColor0.w);
  gl_Position = (matWorldViewProj * tmpvar_1);
  Color = tmpvar_3;
  Tex0 = tmpvar_4;
  ShadowTexCoord = tmpvar_5;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_13, tmpvar_13))
   * fFogDensity))));
  SunLightDir = normalize((tmpvar_12 * -(vSunDir.xyz)));
  SkyLightDir = tmpvar_6;
  ViewDir = normalize((vCameraPos - tmpvar_7)).xyz;
  WorldNormal = tmpvar_9;
}

