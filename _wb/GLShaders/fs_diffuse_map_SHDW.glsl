uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D shadowmap_texture;

uniform float time_var;

uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  vec4 tex_col = texture2D(diffuse_texture, Tex0);
  vec4 tex_sdw = texture2D(diffuse_texture_2, (Tex0 * 0.2) + (time_var * 0.02));

  tex_col_1.w = tex_col.w;
  tex_col_1.xyz = pow (tex_col.xyz, vec3(2.2, 2.2, 2.2));
  float sun_amount_4;
  sun_amount_4 = 0.0;
  vec2 tmpvar_5;
  tmpvar_5 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_6;
  tmpvar_6 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_7;
  if ((tmpvar_6.x < ShadowTexCoord.z)) {
    tmpvar_7 = 0.0;
  } else {
    tmpvar_7 = 1.0;
  };
  vec2 tmpvar_8;
  tmpvar_8.y = 0.0;
  tmpvar_8.x = fShadowMapNextPixel;
  vec4 tmpvar_9;
  tmpvar_9 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_8));
  float tmpvar_10;
  if ((tmpvar_9.x < ShadowTexCoord.z)) {
    tmpvar_10 = 0.0;
  } else {
    tmpvar_10 = 1.0;
  };
  vec2 tmpvar_11;
  tmpvar_11.x = 0.0;
  tmpvar_11.y = fShadowMapNextPixel;
  vec4 tmpvar_12;
  tmpvar_12 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_11));
  float tmpvar_13;
  if ((tmpvar_12.x < ShadowTexCoord.z)) {
    tmpvar_13 = 0.0;
  } else {
    tmpvar_13 = 1.0;
  };
  vec4 tmpvar_14;
  tmpvar_14 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_15;
  if ((tmpvar_14.x < ShadowTexCoord.z)) {
    tmpvar_15 = 0.0;
  } else {
    tmpvar_15 = 1.0;
  };
  sun_amount_4 = clamp (mix (mix (tmpvar_7, tmpvar_10, tmpvar_5.x), mix (tmpvar_13, tmpvar_15, tmpvar_5.x), tmpvar_5.y), 0.0, 1.0);
  tmpvar_2 = (tex_col_1 * (tex_sdw * Color + (SunLight * sun_amount_4)));
  float tmpvar_16;
  tmpvar_16 = (1.0 - clamp (dot (
    normalize(ViewDir)
  ,
    normalize(WorldNormal)
  ), 0.0, 1.0));
  tmpvar_2.xyz = (tmpvar_2.xyz * max (0.6, (
    (tmpvar_16 * tmpvar_16)
   + 0.1)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = clamp(tmpvar_2, 0.0, 1.0);
}

