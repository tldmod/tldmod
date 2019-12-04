/* tld glsl shader -- fs_swy_simple_shader_spiritual -- by swyter */
#version 120

uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
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
  vec4 tmpvar_4;
  tmpvar_4 = (outColor0 * tex_col_2);
  
  finalColor_1.w = tmpvar_4.w;
  finalColor_1.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  finalColor_1.xyz = mix (vFogColor.xyz, finalColor_1.xyz, outFog);
  
  finalColor_1.a = min(0.7,1.0-outColor0.a);
  finalColor_1  *= vec4(198./255., 196./255., 158./255., .8);
  
  gl_FragColor = finalColor_1;
}

