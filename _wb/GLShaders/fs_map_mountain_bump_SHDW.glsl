uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vSunColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec4 Color;
varying vec3 Tex0;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 SunLightDir;
varying vec3 ViewDir;
varying vec3 WorldNormal;

uniform sampler2D diffuse_texture_2;
uniform float time_var;

vec4 swy_scrolling_cloud_shadows(vec2 uvCoords)
{
    vec4 tex_sdw = texture2D(diffuse_texture_2, (uvCoords    * 0.20) + (time_var * 0.02));
    vec4 tex_sdy = texture2D(diffuse_texture_2, (uvCoords    / 3.)   + (time_var * 0.00005));

    return vec4((clamp((tex_sdw * tex_sdy), 0., 1.) * 1.).rgb , 1.);
}

void main ()
{
  vec4 tex_col_1;
  vec4 sample_col_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4 = texture2D (diffuse_texture, Tex0.xy);
  sample_col_2.w = tmpvar_4.w;
  sample_col_2.xyz = pow (tmpvar_4.xyz, vec3(2.2, 2.2, 2.2));
  tex_col_1.xyz = (sample_col_2.xyz + clamp ((
    (Tex0.z * tmpvar_4.w)
   - 1.5), 0.0, 1.0));
  tex_col_1.w = 1.0;

  vec4 tex_sdw = swy_scrolling_cloud_shadows(Tex0.xy);

  vec4 tmpvar_5;
  tmpvar_5.w = 1.0;
  tmpvar_5.xyz = vSunColor.xyz;
  vec4 tmpvar_6;
  tmpvar_6 = (clamp (dot (
    ((2.0 * texture2D (normal_texture, (Tex0.xy * 1.4)).xyz) - 1.0)
  , SunLightDir), 0.0, 1.0) * tmpvar_5);
  float sun_amount_7;
  sun_amount_7 = 0.0;
  vec2 tmpvar_8;
  tmpvar_8 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_9;
  tmpvar_9 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_10;
  if ((tmpvar_9.x < ShadowTexCoord.z)) {
    tmpvar_10 = 0.0;
  } else {
    tmpvar_10 = 1.0;
  };
  vec2 tmpvar_11;
  tmpvar_11.y = 0.0;
  tmpvar_11.x = fShadowMapNextPixel;
  vec4 tmpvar_12;
  tmpvar_12 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_11));
  float tmpvar_13;
  if ((tmpvar_12.x < ShadowTexCoord.z)) {
    tmpvar_13 = 0.0;
  } else {
    tmpvar_13 = 1.0;
  };
  vec2 tmpvar_14;
  tmpvar_14.x = 0.0;
  tmpvar_14.y = fShadowMapNextPixel;
  vec4 tmpvar_15;
  tmpvar_15 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_14));
  float tmpvar_16;
  if ((tmpvar_15.x < ShadowTexCoord.z)) {
    tmpvar_16 = 0.0;
  } else {
    tmpvar_16 = 1.0;
  };
  vec4 tmpvar_17;
  tmpvar_17 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_18;
  if ((tmpvar_17.x < ShadowTexCoord.z)) {
    tmpvar_18 = 0.0;
  } else {
    tmpvar_18 = 1.0;
  };
  sun_amount_7 = clamp (mix (mix (tmpvar_10, tmpvar_13, tmpvar_8.x), mix (tmpvar_16, tmpvar_18, tmpvar_8.x), tmpvar_8.y), 0.0, 1.0);
  tmpvar_3 = (clamp (tex_col_1, 0.0, 1.0) * (tex_sdw * Color + (tmpvar_6 * sun_amount_7)));
  tmpvar_3.xyz = (tmpvar_3.xyz * max (0.6, (
    (1.0 - clamp (dot (ViewDir, WorldNormal), 0.0, 1.0))
   + 0.1)));
  tmpvar_3.w = Color.w;
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

