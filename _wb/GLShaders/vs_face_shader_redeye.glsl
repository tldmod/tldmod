#version 120

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
attribute vec2 inTexCoord;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying float Fog;

varying float EyeColor;

void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 diffuse_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_3 = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_5;
  tmpvar_5.w = 0.0;
  tmpvar_5.xyz = inNormal;
  vec4 tmpvar_6;
  tmpvar_6 = normalize((matWorld * tmpvar_5));
  vec3 tmpvar_7;
  tmpvar_7 = (matWorldView * tmpvar_1).xyz;
  diffuse_light_2.w = vAmbientColor.w;
  diffuse_light_2.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_6.xyz, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_8;
  vWorldPos_8 = (matWorld * tmpvar_1);
  vec3 vWorldN_9;
  vWorldN_9 = tmpvar_6.xyz;
  vec4 total_11;
  total_11 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_10 = 0; j_10 < iLightPointCount; j_10++) {
    int tmpvar_12;
    tmpvar_12 = iLightIndices[j_10];
    vec3 tmpvar_13;
    tmpvar_13 = (vLightPosDir[tmpvar_12].xyz - vWorldPos_8.xyz);
    float tmpvar_14;
    tmpvar_14 = dot (vWorldN_9, normalize(tmpvar_13));
    total_11 = (total_11 + ((
      max ((0.2 * (tmpvar_14 + 0.9)), tmpvar_14)
     * vLightDiffuse[tmpvar_12]) * (1.0/(
      dot (tmpvar_13, tmpvar_13)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_11);
  float tmpvar_15;
  tmpvar_15 = dot (tmpvar_6.xyz, -(vSunDir.xyz));
  vec4 tmpvar_16;
  tmpvar_16.w = 1.0;
  tmpvar_16.xyz = vSunColor.xyz;
  gl_Position = tmpvar_3;
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);
  Tex0 = inTexCoord;
  SunLight = (((
    max ((0.2 * (tmpvar_15 + 0.9)), tmpvar_15)
   * tmpvar_16) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_7, tmpvar_7))
   * fFogDensity))));



   // red eye effect begin:
   vec3 vViewN = normalize(mat3(matWorldView) * inNormal); //normal in view space

   // next two lines increase eye redness radius up:
   vViewN.y = (vViewN.y<0) ? min(vViewN.y+0.2,0) : vViewN.y;
   vViewN = normalize(vViewN);

   float v = vViewN.z * vViewN.z;
         v = v * v * v;
         v = v * v * v;

   EyeColor = v * v;

   float night = clamp(1.28 * (0.9-vSunColor.x), 0.15, 1.0);
   EyeColor *= night;


}

