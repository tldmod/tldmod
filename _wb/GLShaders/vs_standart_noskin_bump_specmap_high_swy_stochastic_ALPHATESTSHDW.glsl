uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform float fFogDensity;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform bool bUseMotionBlur;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matMotionBlur;
uniform mat4 matSunViewProj;
uniform mat4 matViewProj;
uniform vec4 vLightPosDir[4];
uniform vec4 vCameraPos;
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
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
  vec4 vVertexColor_2;
  vVertexColor_2 = inColor0;
  vec4 vWorldPos_3;
  vec4 tmpvar_4;
  vec4 tmpvar_5;
  vec3 tmpvar_6;
  vec3 tmpvar_7;
  vec4 tmpvar_8;
  vec4 tmpvar_9;
  tmpvar_9 = (matWorld * tmpvar_1);
  vWorldPos_3 = tmpvar_9;
  vec4 tmpvar_10;
  tmpvar_10.w = 0.0;
  tmpvar_10.xyz = inNormal;
  vec3 tmpvar_11;
  tmpvar_11 = normalize((matWorld * tmpvar_10).xyz);
  if (bUseMotionBlur) {
    vec4 tmpvar_12;
    tmpvar_12 = (matMotionBlur * tmpvar_1);
    vec4 tmpvar_13;
    tmpvar_13 = normalize((tmpvar_12 - tmpvar_9));
    float tmpvar_14;
    tmpvar_14 = dot (tmpvar_11, tmpvar_13.xyz);
    float tmpvar_15;
    if ((tmpvar_14 > 0.1)) {
      tmpvar_15 = 1.0;
    } else {
      tmpvar_15 = 0.0;
    };
    vWorldPos_3 = mix (tmpvar_9, tmpvar_12, (tmpvar_15 * clamp (
      (inPosition.y + 0.15)
    , 0.0, 1.0)));
    vVertexColor_2.w = ((clamp (
      (0.5 - inPosition.y)
    , 0.0, 1.0) + clamp (
      mix (1.1, -0.6999999, clamp ((dot (tmpvar_11, tmpvar_13.xyz) + 0.5), 0.0, 1.0))
    , 0.0, 1.0)) + 0.25);
  };
  if (bUseMotionBlur) {
    tmpvar_4 = (matViewProj * vWorldPos_3);
  } else {
    tmpvar_4 = (matWorldViewProj * tmpvar_1);
  };
  vec4 tmpvar_16;
  tmpvar_16.w = 0.0;
  tmpvar_16.xyz = inBinormal;
  vec3 tmpvar_17;
  tmpvar_17 = normalize((matWorld * tmpvar_16).xyz);
  vec4 tmpvar_18;
  tmpvar_18.w = 0.0;
  tmpvar_18.xyz = inTangent;
  vec3 tmpvar_19;
  tmpvar_19 = normalize((matWorld * tmpvar_18).xyz);
  vec3 tmpvar_20;
  tmpvar_20.x = tmpvar_19.x;
  tmpvar_20.y = tmpvar_17.x;
  tmpvar_20.z = tmpvar_11.x;
  vec3 tmpvar_21;
  tmpvar_21.x = tmpvar_19.y;
  tmpvar_21.y = tmpvar_17.y;
  tmpvar_21.z = tmpvar_11.y;
  vec3 tmpvar_22;
  tmpvar_22.x = tmpvar_19.z;
  tmpvar_22.y = tmpvar_17.z;
  tmpvar_22.z = tmpvar_11.z;
  mat3 tmpvar_23;
  tmpvar_23[0] = tmpvar_20;
  tmpvar_23[1] = tmpvar_21;
  tmpvar_23[2] = tmpvar_22;
  tmpvar_6 = normalize((tmpvar_23 * -(vSunDir.xyz)));
  tmpvar_7 = (tmpvar_23 * vec3(0.0, 0.0, 1.0));
  tmpvar_5 = vVertexColor_2.zyxw;
  vec4 vWorldPos_24;
  vWorldPos_24 = vWorldPos_3;
  vec3 vWorldN_25;
  vWorldN_25 = tmpvar_11;
  vec4 total_27;
  total_27 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_26 = 0; j_26 < iLightPointCount; j_26++) {
    if ((j_26 != 0)) {
      int tmpvar_28;
      tmpvar_28 = iLightIndices[j_26];
      vec3 tmpvar_29;
      tmpvar_29 = (vLightPosDir[tmpvar_28].xyz - vWorldPos_24.xyz);
      total_27 = (total_27 + ((
        clamp (dot (vWorldN_25, normalize(tmpvar_29)), 0.0, 1.0)
       * vLightDiffuse[tmpvar_28]) * (1.0/(
        dot (tmpvar_29, tmpvar_29)
      ))));
    };
  };
  int tmpvar_30;
  tmpvar_30 = iLightIndices[0];
  vec3 tmpvar_31;
  tmpvar_31 = (vLightPosDir[tmpvar_30].xyz - vWorldPos_3.xyz);
  tmpvar_8.xyz = (tmpvar_23 * normalize(tmpvar_31));
  tmpvar_8.w = clamp ((1.0/(dot (tmpvar_31, tmpvar_31))), 0.0, 1.0);
  tmpvar_5.w = (vVertexColor_2.w * vMaterialColor.w);
  vec3 tmpvar_32;
  tmpvar_32 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_32, tmpvar_32))
   * fFogDensity))));
  VertexColor = tmpvar_5;
  VertexLighting = total_27.xyz;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_6;
  SkyLightDir = tmpvar_7;
  PointLightDir = tmpvar_8;
  ShadowTexCoord = (matSunViewProj * vWorldPos_3);
  ViewDir = (tmpvar_23 * normalize((vCameraPos.xyz - vWorldPos_3.xyz)));
}

