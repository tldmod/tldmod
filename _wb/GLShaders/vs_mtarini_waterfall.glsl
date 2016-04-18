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
attribute vec4 inColor1;
attribute vec2 inTexCoord;
varying float Fog;
varying vec4 Color;
varying vec3 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;

uniform float time_var;

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
  vec3 tmpvar_6;
  tmpvar_6 = normalize((matWorld * tmpvar_5).xyz);
  diffuse_light_2 = (vAmbientColor + inColor1.zyxw);
  diffuse_light_2.xyz = (diffuse_light_2.xyz + (clamp (
    dot (tmpvar_6, -(vSkyLightDir.xyz))
  , 0.0, 1.0) * vSkyLightColor.xyz));
  vec4 vWorldPos_7;
  vWorldPos_7 = (matWorld * tmpvar_1);
  vec3 vWorldN_8;
  vWorldN_8 = tmpvar_6;
  vec4 total_10;
  total_10 = vec4(0.0, 0.0, 0.0, 0.0);
  for (int j_9 = 0; j_9 < iLightPointCount; j_9++) {
    int tmpvar_11;
    tmpvar_11 = iLightIndices[j_9];
    vec3 tmpvar_12;
    tmpvar_12 = (vLightPosDir[tmpvar_11].xyz - vWorldPos_7.xyz);
    total_10 = (total_10 + ((
      clamp (dot (vWorldN_8, normalize(tmpvar_12)), 0.0, 1.0)
     * vLightDiffuse[tmpvar_11]) * (1.0/(
      dot (tmpvar_12, tmpvar_12)
    ))));
  };
  diffuse_light_2 = (diffuse_light_2 + total_10);
  vec4 tmpvar_13;
  tmpvar_13.w = 1.0;
  tmpvar_13.xyz = vSunColor.xyz;
  vec3 tmpvar_14;
  tmpvar_14 = (matWorldView * tmpvar_1).xyz;
  gl_Position = tmpvar_3;
  Fog = (1.0/(exp2((
    sqrt(dot (tmpvar_14, tmpvar_14))
   * fFogDensity))));
  Color = ((vMaterialColor * inColor0.zyxw) * diffuse_light_2);

  /* flip vertical UV space to counter reverse OpenGL (bottom-left) texture sampling vs DirectX (top-left) */
  vec2 _inTexCoord = vec2(inTexCoord.x, 1.0 - inTexCoord.y);

  Tex0 = vec3(_inTexCoord.x, _inTexCoord.y - (0.15f * time_var),
                            (_inTexCoord.y - (0.50f * time_var)) / 2.f);

  SunLight = (((
    clamp (dot (tmpvar_6, -(vSunDir.xyz)), 0.0, 1.0)
   * tmpvar_13) * vMaterialColor) * inColor0.zyxw);
  ShadowTexCoord = tmpvar_4;
}

