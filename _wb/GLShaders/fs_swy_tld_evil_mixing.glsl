/* tld glsl shader -- fs_swy_tld_evil_mixing -- by swyter */
#version 120

uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2
;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;


/* swyter-- used to hide the HP overlay on TLD cutscenes */
uniform float swy_ui_evil = 0.0f;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;
void main ()
{
  vec4 finalColor_1;
  vec4 tex_col_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, outTexCoord);
  tex_col_2.w = tmpvar_3.w;
  tex_col_2.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));

  /* swyter -- linearly interpolate/mix between both GUI background textures, suggested by Kham and Merlkir! */
  vec4 tex_col_evil = texture2D(diffuse_texture_2
, outTexCoord); tex_col_evil.xyz = pow(tex_col_evil.xyz, vec3(2.2));
  tex_col_2 = mix(tex_col_2, tex_col_evil, swy_ui_evil);

  vec4 tmpvar_4;
  tmpvar_4 = (outColor0 * tex_col_2);
  finalColor_1.w = tmpvar_4.w;
  finalColor_1.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  finalColor_1.xyz = mix (vFogColor.xyz, finalColor_1.xyz, outFog);
  gl_FragColor = finalColor_1;
}

