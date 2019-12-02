/* tld glsl shader -- fs_swy_tld_evil_mixing -- by swyter */
#version 120

uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;

uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;


/* swyter-- used to set if the UI is the evil one or not
 *  - 'good' -> 0
 *  - 'evil' -> 1
 **/
uniform float swy_ui_evil = 0.0f;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;

void main ()
{
  vec4 final_color;
  vec4 texture_color;

  vec4 tmpvar_3 = swy_ui_evil < 0.5 ?
      texture2D(diffuse_texture,   outTexCoord) :
      texture2D(diffuse_texture_2, outTexCoord);

  texture_color.w = tmpvar_3.w;
  texture_color.xyz = pow(tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));

  vec4 tmpvar_4 = outColor0 * texture_color;

  final_color.xyz = pow(tmpvar_4.xyz, output_gamma_inv.xyz);
  final_color.xyz = mix(vFogColor.xyz, final_color.xyz, outFog);
  final_color.w = tmpvar_4.w;

  gl_FragColor = final_color;
}

