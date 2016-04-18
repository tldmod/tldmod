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
uniform mat4 matSunViewProj;
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

#define PREV_RESIZE 1.00/0.78
#define POST_RESIZE 0.78

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
  int tmpvar_5;
  tmpvar_5 = int(inBlendIndices.x);
  int tmpvar_6;
  tmpvar_6 = int(inBlendIndices.y);
  int tmpvar_7;
  tmpvar_7 = int(inBlendIndices.z);
  int tmpvar_8;
  tmpvar_8 = int(inBlendIndices.w);
  tmpvar_4 = (((
    ((matWorldArray[tmpvar_5] * tmpvar_1) * inBlendWeight.x)
   +
    ((matWorldArray[tmpvar_6] * tmpvar_1) * inBlendWeight.y)
  ) + (
    (matWorldArray[tmpvar_7] * tmpvar_1)
   * inBlendWeight.z)) + ((matWorldArray[tmpvar_8] * tmpvar_1) * inBlendWeight.w));

  /* !!! */
  tmpvar_4.xyz *= POST_RESIZE;

  vec4 tmpvar_9;
  tmpvar_9.w = 0.0;
  tmpvar_9.xyz = inNormal;
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
  tmpvar_13 = (matWorld * tmpvar_4);
  tmpvar_2 = (matWorldViewProj * tmpvar_4);
  vec4 tmpvar_14;
  tmpvar_14.w = 0.0;
  tmpvar_14.xyz = normalize(((
    (((matWorldArray[tmpvar_5] * tmpvar_9).xyz * inBlendWeight.x) + ((matWorldArray[tmpvar_6] * tmpvar_10).xyz * inBlendWeight.y))
   +
    ((matWorldArray[tmpvar_7] * tmpvar_11).xyz * inBlendWeight.z)
  ) + (
    (matWorldArray[tmpvar_8] * tmpvar_12)
  .xyz * inBlendWeight.w)));
  vec3 tmpvar_15;
  tmpvar_15 = normalize((matWorld * tmpvar_14).xyz);
  vec3 tmpvar_16;
  tmpvar_16 = (matView * tmpvar_13).xyz;
  tmpvar_3.w = vAmbientColor.w;
  tmpvar_3.xyz = (vAmbientColor.xyz + (clamp (
    dot (tmpvar_15, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_17;
  vWorldPos_17 = tmpvar_13;
  vec3 vWorldN_18;
  vWorldN_18 = tmpvar_15;
  vec4 total_20;
  total_20 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_19 = 0; j_19 < iLightPointCount; j_19++) {
    int tmpvar_21;
    tmpvar_21 = iLightIndices[j_19];
    vec3 tmpvar_22;
    tmpvar_22 = (vLightPosDir[tmpvar_21].xyz - vWorldPos_17.xyz);
    total_20 = (total_20 + ((
      clamp (dot (vWorldN_18, normalize(tmpvar_22)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_21]) * (1.0/(
      dot (tmpvar_22, tmpvar_22)
    ))));
  };
  tmpvar_3 = (tmpvar_3 + total_20);
  tmpvar_3 = (tmpvar_3 * (vMaterialColor * inColor0.zyxw));
  vec4 tmpvar_23;
  tmpvar_23 = min (vec4(1.0, 1.0, 1.0, 1.0), tmpvar_3);
  tmpvar_3 = tmpvar_23;
  vec4 tmpvar_24;
  tmpvar_24.w = 1.0;
  tmpvar_24.xyz = vSunColor.xyz;
  gl_Position = tmpvar_2;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_16, tmpvar_16))
   * fFogDensity))));
  Color = tmpvar_23;
  Tex0 = inTexCoord;
  SunLight = (((
    clamp (dot (tmpvar_15, -(vSunDir.xyz)), 0.0, 1.0)
   * tmpvar_24) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = (matSunViewProj * tmpvar_13);
}

