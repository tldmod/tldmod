uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D normal_texture;
uniform sampler2D shadowmap_texture;
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
  vec4 multi_tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  total_light_2 = vAmbientColor;
  vec4 tmpvar_4;
  tmpvar_4 = texture2D (diffuse_texture, Tex0);
  multi_tex_col_1.w = 1.0;//tmpvar_4.w;
  multi_tex_col_1.xyz = (tmpvar_4.xyz * (1.0 - VertexColor.w));
  multi_tex_col_1.xyz = (multi_tex_col_1.xyz + (texture2D (diffuse_texture_2, (Tex0 * 1.237)).xyz * VertexColor.w));
  multi_tex_col_1.xyz = pow (multi_tex_col_1.xyz, vec3(2.2, 2.2, 2.2));
  vec3 tmpvar_5;
  tmpvar_5 = ((2.0 * texture2D (normal_texture, Tex0).xyz) - 1.0);
  float sun_amount_6;
  sun_amount_6 = 0.0;
  vec2 tmpvar_7;
  tmpvar_7 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_8;
  tmpvar_8 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_9;
  if ((tmpvar_8.x < ShadowTexCoord.z)) {
    tmpvar_9 = 0.0;
  } else {
    tmpvar_9 = 1.0;
  };
  vec2 tmpvar_10;
  tmpvar_10.y = 0.0;
  tmpvar_10.x = fShadowMapNextPixel;
  vec4 tmpvar_11;
  tmpvar_11 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_10));
  float tmpvar_12;
  if ((tmpvar_11.x < ShadowTexCoord.z)) {
    tmpvar_12 = 0.0;
  } else {
    tmpvar_12 = 1.0;
  };
  vec2 tmpvar_13;
  tmpvar_13.x = 0.0;
  tmpvar_13.y = fShadowMapNextPixel;
  vec4 tmpvar_14;
  tmpvar_14 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_13));
  float tmpvar_15;
  if ((tmpvar_14.x < ShadowTexCoord.z)) {
    tmpvar_15 = 0.0;
  } else {
    tmpvar_15 = 1.0;
  };
  vec4 tmpvar_16;
  tmpvar_16 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_17;
  if ((tmpvar_16.x < ShadowTexCoord.z)) {
    tmpvar_17 = 0.0;
  } else {
    tmpvar_17 = 1.0;
  };
  sun_amount_6 = clamp (mix (mix (tmpvar_9, tmpvar_12, tmpvar_7.x), mix (tmpvar_15, tmpvar_17, tmpvar_7.x), tmpvar_7.y), 0.0, 1.0);
  vec4 tmpvar_18;
  tmpvar_18.w = 1.0;
  tmpvar_18.xyz = vSunColor.xyz;
  total_light_2 = (vAmbientColor + ((
    clamp (dot (SunLightDir, tmpvar_5), 0.0, 1.0)
   * sun_amount_6) * tmpvar_18));
  total_light_2 = (total_light_2 + (clamp (
    dot (SkyLightDir, tmpvar_5)
  , 0.0, 1.0) * vSkyLightColor));
  vec4 tmpvar_19;
  tmpvar_19.w = 1.0;
  tmpvar_19.xyz = vPointLightColor.xyz;
  total_light_2 = (total_light_2 + (clamp (
    dot (PointLightDir.xyz, tmpvar_5)
  , 0.0, 1.0) * tmpvar_19));
  tmpvar_3.xyz = total_light_2.xyz;
  tmpvar_3.w = 1.0;
  tmpvar_3 = (tmpvar_3 * multi_tex_col_1);
  tmpvar_3.xyz = (tmpvar_3.xyz * VertexColor.xyz);
  tmpvar_3.w = (tmpvar_3.w * PointLightDir.w);
  float tmpvar_20;
  tmpvar_20 = (1.0 - clamp (dot (
    normalize(ViewDir)
  ,
    normalize(WorldNormal)
  ), 0.0, 1.0));
  tmpvar_3.xyz = (tmpvar_3.xyz * max (0.6, (
    (tmpvar_20 * tmpvar_20)
   + 0.1)));
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

