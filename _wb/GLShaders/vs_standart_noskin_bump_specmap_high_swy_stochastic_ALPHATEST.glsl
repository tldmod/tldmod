uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSunDir;
uniform float fMaterialPower;
uniform float fFogDensity;
uniform int iLightPointCount;
uniform int iLightIndices[4];
uniform bool bUseMotionBlur;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
uniform mat4 matWorld;
uniform mat4 matMotionBlur;
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
  vec3 tmpvar_8;
  vec4 tmpvar_9;
  vec3 tmpvar_10;
  vec4 tmpvar_11;
  tmpvar_11 = (matWorld * tmpvar_1);
  vWorldPos_3 = tmpvar_11;
  vec4 tmpvar_12;
  tmpvar_12.w = 0.0;
  tmpvar_12.xyz = inNormal;
  vec3 tmpvar_13;
  tmpvar_13 = normalize((matWorld * tmpvar_12).xyz);
  if (bUseMotionBlur) {
    vec4 tmpvar_14;
    tmpvar_14 = (matMotionBlur * tmpvar_1);
    vec4 tmpvar_15;
    tmpvar_15 = normalize((tmpvar_14 - tmpvar_11));
    float tmpvar_16;
    tmpvar_16 = dot (tmpvar_13, tmpvar_15.xyz);
    float tmpvar_17;
    if ((tmpvar_16 > 0.1)) {
      tmpvar_17 = 1.0;
    } else {
      tmpvar_17 = 0.0;
    };
    vWorldPos_3 = mix (tmpvar_11, tmpvar_14, (tmpvar_17 * clamp (
      (inPosition.y + 0.15)
    , 0.0, 1.0)));
    vVertexColor_2.w = ((clamp (
      (0.5 - inPosition.y)
    , 0.0, 1.0) + clamp (
      mix (1.1, -0.6999999, clamp ((dot (tmpvar_13, tmpvar_15.xyz) + 0.5), 0.0, 1.0))
    , 0.0, 1.0)) + 0.25);
  };
  if (bUseMotionBlur) {
    tmpvar_4 = (matViewProj * vWorldPos_3);
  } else {
    tmpvar_4 = (matWorldViewProj * tmpvar_1);
  };
  vec4 tmpvar_18;
  tmpvar_18.w = 0.0;
  tmpvar_18.xyz = inBinormal;
  vec3 tmpvar_19;
  tmpvar_19 = normalize((matWorld * tmpvar_18).xyz);
  vec4 tmpvar_20;
  tmpvar_20.w = 0.0;
  tmpvar_20.xyz = inTangent;
  vec3 tmpvar_21;
  tmpvar_21 = normalize((matWorld * tmpvar_20).xyz);
  vec3 tmpvar_22;
  tmpvar_22.x = tmpvar_21.x;
  tmpvar_22.y = tmpvar_19.x;
  tmpvar_22.z = tmpvar_13.x;
  vec3 tmpvar_23;
  tmpvar_23.x = tmpvar_21.y;
  tmpvar_23.y = tmpvar_19.y;
  tmpvar_23.z = tmpvar_13.y;
  vec3 tmpvar_24;
  tmpvar_24.x = tmpvar_21.z;
  tmpvar_24.y = tmpvar_19.z;
  tmpvar_24.z = tmpvar_13.z;
  mat3 tmpvar_25;
  tmpvar_25[0] = tmpvar_22;
  tmpvar_25[1] = tmpvar_23;
  tmpvar_25[2] = tmpvar_24;
  tmpvar_7 = normalize((tmpvar_25 * -(vSunDir.xyz)));
  tmpvar_8 = (tmpvar_25 * vec3(0.0, 0.0, 1.0));
  tmpvar_5 = vVertexColor_2.zyxw;
  vec4 vWorldPos_26;
  vWorldPos_26 = vWorldPos_3;
  vec3 vWorldN_27;
  vWorldN_27 = tmpvar_13;
  vec4 total_29;
  total_29 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_28 = 0; j_28 < iLightPointCount; j_28++) {
    if ((j_28 != 0)) {
      int tmpvar_30;
      tmpvar_30 = iLightIndices[j_28];
      vec3 tmpvar_31;
      tmpvar_31 = (vLightPosDir[tmpvar_30].xyz - vWorldPos_26.xyz);
      total_29 = (total_29 + ((
        clamp (dot (vWorldN_27, normalize(tmpvar_31)), 0.0, 1.0)
       * vLightDiffuse[tmpvar_30]) * (1.0/(
        dot (tmpvar_31, tmpvar_31)
      ))));
    };
  };
  tmpvar_6 = total_29.xyz;
  int tmpvar_32;
  tmpvar_32 = iLightIndices[0];
  vec3 tmpvar_33;
  tmpvar_33 = (vLightPosDir[tmpvar_32].xyz - vWorldPos_3.xyz);
  tmpvar_9.xyz = (tmpvar_25 * normalize(tmpvar_33));
  tmpvar_9.w = clamp ((1.0/(dot (tmpvar_33, tmpvar_33))), 0.0, 1.0);
  vec3 tmpvar_34;
  tmpvar_34 = normalize((vCameraPos.xyz - vWorldPos_3.xyz));
  tmpvar_10 = (tmpvar_25 * tmpvar_34);
  vec3 vWorldPos_35;
  vWorldPos_35 = vWorldPos_3.xyz;
  vec3 vWorldN_36;
  vWorldN_36 = tmpvar_13;
  vec3 vWorldView_37;
  vWorldView_37 = tmpvar_34;
  vec4 total_39;
  total_39 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int i_38 = 0; i_38 < iLightPointCount; i_38++) {
    vec3 tmpvar_40;
    tmpvar_40 = (vLightPosDir[i_38].xyz - vWorldPos_35);
    total_39 = (total_39 + ((
      (1.0/(dot (tmpvar_40, tmpvar_40)))
     * vLightDiffuse[i_38]) * pow (
      clamp (dot (normalize((vWorldView_37 + 
        normalize(tmpvar_40)
      )), vWorldN_36), 0.0, 1.0)
    , fMaterialPower)));
  };
  tmpvar_5.w = (vVertexColor_2.w * vMaterialColor.w);
  vec3 tmpvar_41;
  tmpvar_41 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_4;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_41, tmpvar_41))
   * fFogDensity))));
  VertexColor = tmpvar_5;
  VertexLighting = tmpvar_6;
  Tex0 = inTexCoord;
  SunLightDir = tmpvar_7;
  SkyLightDir = tmpvar_8;
  PointLightDir = tmpvar_9;
  ShadowTexCoord = total_39;
  ViewDir = tmpvar_10;
}

