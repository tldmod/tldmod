uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vPointLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  total_light_2 = vAmbientColor;
  vec3 tmpvar_4;
  tmpvar_4 = ((2.0 * texture2D (normal_texture, Tex0).xyz) - 1.0);
  float sun_amount_5;
  sun_amount_5 = 0.0;
  vec2 tmpvar_6;
  tmpvar_6 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_8;
  if ((tmpvar_7.x < ShadowTexCoord.z)) {
    tmpvar_8 = 0.0;
  } else {
    tmpvar_8 = 1.0;
  };
  vec2 tmpvar_9;
  tmpvar_9.y = 0.0;
  tmpvar_9.x = fShadowMapNextPixel;
  vec4 tmpvar_10;
  tmpvar_10 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_9));
  float tmpvar_11;
  if ((tmpvar_10.x < ShadowTexCoord.z)) {
    tmpvar_11 = 0.0;
  } else {
    tmpvar_11 = 1.0;
  };
  vec2 tmpvar_12;
  tmpvar_12.x = 0.0;
  tmpvar_12.y = fShadowMapNextPixel;
  vec4 tmpvar_13;
  tmpvar_13 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_12));
  float tmpvar_14;
  if ((tmpvar_13.x < ShadowTexCoord.z)) {
    tmpvar_14 = 0.0;
  } else {
    tmpvar_14 = 1.0;
  };
  vec4 tmpvar_15;
  tmpvar_15 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_16;
  if ((tmpvar_15.x < ShadowTexCoord.z)) {
    tmpvar_16 = 0.0;
  } else {
    tmpvar_16 = 1.0;
  };
  sun_amount_5 = clamp (mix (mix (tmpvar_8, tmpvar_11, tmpvar_6.x), mix (tmpvar_14, tmpvar_16, tmpvar_6.x), tmpvar_6.y), 0.0, 1.0);
  vec4 tmpvar_17;
  tmpvar_17.w = 1.0;
  tmpvar_17.xyz = vSunColor.xyz;
  total_light_2 = (vAmbientColor + ((
    clamp (dot (SunLightDir, tmpvar_4), 0.0, 1.0)
   *
    (sun_amount_5 * sun_amount_5)
  ) * tmpvar_17));
  total_light_2 = (total_light_2 + (clamp (
    dot (SkyLightDir, tmpvar_4)
  , 0.0, 1.0) * vSkyLightColor));
  vec4 tmpvar_18;
  tmpvar_18.w = 1.0;
  tmpvar_18.xyz = vPointLightColor.xyz;
  total_light_2 = (total_light_2 + (clamp (
    dot (PointLightDir.xyz, tmpvar_4)
  , 0.0, 1.0) * tmpvar_18));
  tmpvar_3.xyz = total_light_2.xyz;
  tmpvar_3.w = 1.0;
  tmpvar_3 = (tmpvar_3 * vMaterialColor);
  vec4 tmpvar_19;
  tmpvar_19 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = 1.0;//tmpvar_19.w;
  tex_col_1.xyz = pow (tmpvar_19.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_3 = (tmpvar_3 * tex_col_1);
  tmpvar_3 = (tmpvar_3 * VertexColor);
  float tmpvar_20;
  tmpvar_20 = (1.0 - clamp (dot (ViewDir, WorldNormal), 0.0, 1.0));
  tmpvar_3.xyz = (tmpvar_3.xyz * max (0.6, (
    (tmpvar_20 * tmpvar_20)
   + 0.1)));
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  if ((tmpvar_3.w < 0.05)) {
    discard;
  };
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

