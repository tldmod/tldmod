uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform float fMaterialPower;
uniform float fFogDensity;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matWorldArray[32];
uniform vec4 vLightPosDir[4];
uniform vec4 vCameraPos;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;
varying float Fog;
varying vec4 VertexColor;
varying vec3 VertexLighting;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
varying vec3 ViewDir;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  vec4 vObjectPos_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  vec3 tmpvar_5;
  vec4 tmpvar_6;
  vec4 tmpvar_7;
  vObjectPos_2 = (((
    ((matWorldArray[int(inBlendIndices.x)] * tmpvar_1) * inBlendWeight.x)
   + 
    ((matWorldArray[int(inBlendIndices.y)] * tmpvar_1) * inBlendWeight.y)
  ) + (
    (matWorldArray[int(inBlendIndices.z)] * tmpvar_1)
   * inBlendWeight.z)) + ((matWorldArray[
    int(inBlendIndices.w)
  ] * tmpvar_1) * inBlendWeight.w));
  vec4 tmpvar_8;
  tmpvar_8 = (matWorld * vObjectPos_2);
  vec4 tmpvar_9;
  tmpvar_9.w = 0.0;
  tmpvar_9.xyz = inNormal;
  vec3 tmpvar_10;
  tmpvar_10 = normalize((matWorld * tmpvar_9).xyz);
  tmpvar_3 = (matWorldViewProj * vObjectPos_2);
  tmpvar_4 = inColor0.zyxw;
  vec4 vWorldPos_11;
  vWorldPos_11 = tmpvar_8;
  vec3 vWorldN_12;
  vWorldN_12 = tmpvar_10;
  vec4 total_14;
  total_14 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_13 = 0; j_13 < iLightPointCount; j_13++) {
    int tmpvar_15;
    tmpvar_15 = iLightIndices[j_13];
    vec3 tmpvar_16;
    tmpvar_16 = (vLightPosDir[tmpvar_15].xyz - vWorldPos_11.xyz);
    total_14 = (total_14 + ((
      clamp (dot (vWorldN_12, normalize(tmpvar_16)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_15]) * (1.0/(
      dot (tmpvar_16, tmpvar_16)
    ))));
  };
  tmpvar_5 = total_14.xyz;
  vec3 tmpvar_17;
  tmpvar_17 = normalize((vCameraPos.xyz - tmpvar_8.xyz));
  vec3 vWorldPos_18;
  vWorldPos_18 = tmpvar_8.xyz;
  vec3 vWorldN_19;
  vWorldN_19 = tmpvar_10;
  vec3 vWorldView_20;
  vWorldView_20 = tmpvar_17;
  vec4 total_22;
  total_22 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int i_21 = 0; i_21 < iLightPointCount; i_21++) {
    vec3 tmpvar_23;
    tmpvar_23 = (vLightPosDir[i_21].xyz - vWorldPos_18);
    total_22 = (total_22 + ((
      (1.0/(dot (tmpvar_23, tmpvar_23)))
     * vLightDiffuse[i_21]) * pow (
      clamp (dot (normalize((vWorldView_20 + 
        normalize(tmpvar_23)
      )), vWorldN_19), 0.0, 1.0)
    , fMaterialPower)));
  };
  tmpvar_4.w = (inColor0.w * vMaterialColor.w);
  vec3 tmpvar_24;
  tmpvar_24 = (matWorldView * vObjectPos_2).xyz;
  gl_Position = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_24, tmpvar_24))
   * fFogDensity))));
  VertexColor = tmpvar_4;
  VertexLighting = tmpvar_5;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_10;
  SkyLightDir = total_22.xyz;
  PointLightDir = tmpvar_6;
  ShadowTexCoord = tmpvar_7;
  ViewDir = tmpvar_17;
}

