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
uniform mat4 matWorld;
uniform mat4 matWorldArray[32];
uniform mat4 matView;
uniform vec4 vLightPosDir[4];
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;
varying float Fog;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;

#define PREV_RESIZE 1.00
#define POST_RESIZE 0.95

void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;

  /* !!! */
  tmpvar_1.xyz *= PREV_RESIZE;

  vec4 tmpvar_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  vec4 tmpvar_5;
  int tmpvar_6;
  tmpvar_6 = int(inBlendIndices.x);
  int tmpvar_7;
  tmpvar_7 = int(inBlendIndices.y);
  int tmpvar_8;
  tmpvar_8 = int(inBlendIndices.z);
  int tmpvar_9;
  tmpvar_9 = int(inBlendIndices.w);
  tmpvar_5 = (((
    ((matWorldArray[tmpvar_6] * tmpvar_1) * inBlendWeight.x)
   +
    ((matWorldArray[tmpvar_7] * tmpvar_1) * inBlendWeight.y)
  ) + (
    (matWorldArray[tmpvar_8] * tmpvar_1)
   * inBlendWeight.z)) + ((matWorldArray[tmpvar_9] * tmpvar_1) * inBlendWeight.w));
  vec4 tmpvar_10;
  tmpvar_10.w = 0.0;
  tmpvar_10.xyz = inNormal;
  vec4 tmpvar_11;
  tmpvar_11.w = 0.0;
  tmpvar_11.xyz = inNormal;
  vec4 tmpvar_12;
  tmpvar_12.w = 0.0;
  tmpvar_12.xyz = inNormal;
  vec4 tmpvar_13;
  tmpvar_13.w = 0.0;
  tmpvar_13.xyz = inNormal;
  vec4 tmpvar_14;
  tmpvar_14 = (matWorld * tmpvar_5);
  tmpvar_2 = (matWorldViewProj * tmpvar_5);
  vec4 tmpvar_15;
  tmpvar_15.w = 0.0;
  tmpvar_15.xyz = normalize(((
    (((matWorldArray[tmpvar_6] * tmpvar_10).xyz * inBlendWeight.x) + ((matWorldArray[tmpvar_7] * tmpvar_11).xyz * inBlendWeight.y))
   +
    ((matWorldArray[tmpvar_8] * tmpvar_12).xyz * inBlendWeight.z)
  ) + (
    (matWorldArray[tmpvar_9] * tmpvar_13)
  .xyz * inBlendWeight.w)));

  /* !!! */
  tmpvar_15.xyz *= POST_RESIZE;

  vec3 tmpvar_16;
  tmpvar_16 = normalize((matWorld * tmpvar_15).xyz);
  vec3 tmpvar_17;
  tmpvar_17 = (matView * tmpvar_14).xyz;
  tmpvar_3.w = vAmbientColor.w;
  tmpvar_3.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_16, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_18;
  vWorldPos_18 = tmpvar_14;
  vec3 vWorldN_19;
  vWorldN_19 = tmpvar_16;
  vec4 total_21;
  total_21 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_20 = 0; j_20 < iLightPointCount; j_20++) {
    int tmpvar_22;
    tmpvar_22 = iLightIndices[j_20];
    vec3 tmpvar_23;
    tmpvar_23 = (vLightPosDir[tmpvar_22].xyz - vWorldPos_18.xyz);
    total_21 = (total_21 + ((
      clamp (dot (vWorldN_19, normalize(tmpvar_23)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_22]) * (1.0/(
      dot (tmpvar_23, tmpvar_23)
    ))));
  };
  tmpvar_3 = (tmpvar_3 + total_21);
  tmpvar_3 = (tmpvar_3 * (vMaterialColor * inColor0.zyxw));
  vec4 tmpvar_24;
  tmpvar_24 = min (vec4(1.0, 1.0, 1.0, 1.0), tmpvar_3);
  tmpvar_3 = tmpvar_24;
  vec4 tmpvar_25;
  tmpvar_25.w = 1.0;
  tmpvar_25.xyz = vSunColor.xyz;
  gl_Position = tmpvar_2;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_17, tmpvar_17))
   * fFogDensity))));
  Color = tmpvar_24;
  Tex0 = inTexCoord;
  SunLight = (((
    clamp (dot (tmpvar_16, -(vSunDir.xyz)), 0.0, 1.0)
   * tmpvar_25) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = tmpvar_4;
}

