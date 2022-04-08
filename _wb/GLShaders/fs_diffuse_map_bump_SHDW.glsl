uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 SunLightDir;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_3.w;
  tex_col_1.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  tmpvar_4.xyz = vSunColor.xyz;
  vec4 tmpvar_5;
  tmpvar_5 = ((clamp (
    dot (((2.0 * texture2D (normal_texture, (Tex0 * 1.4)).xyz) - 1.0), SunLightDir)
  , 0.0, 1.0) * tmpvar_4) * vMaterialColor);
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
  tmpvar_2.xyz = (tex_col_1.xyz * (Color.xyz + (tmpvar_5.xyz * sun_amount_6)));
  tmpvar_2.w = Color.w;
  float tmpvar_18;
  tmpvar_18 = (1.0 - clamp (dot (
    normalize(ViewDir)
  , 
    normalize(WorldNormal)
  ), 0.0, 1.0));
  tmpvar_2.xyz = (tmpvar_2.xyz * max (0.6, (
    (tmpvar_18 * tmpvar_18)
   + 0.1)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = clamp(tmpvar_2, 0., 1.);
}

