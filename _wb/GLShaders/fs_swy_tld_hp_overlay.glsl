/* tld glsl shader -- fs_swy_tld_hp_overlay -- by swyter */
#version 120

uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;

void main ()
{
  vec4 final_color;
  vec4 texture_color;

  vec4 tmp_1 = texture2D(diffuse_texture, outTexCoord);

  texture_color.xyz = pow(tmp_1.xyz, vec3(2.2, 2.2, 2.2));
  texture_color.w = tmp_1.w;

  vec4 tmp_2 = outColor0 * texture_color;

  final_color.xyz = pow(tmp_2.xyz, output_gamma_inv.xyz);
  final_color.xyz = mix(vFogColor.xyz, final_color.xyz, outFog);

  final_color.w = tmp_2.w;
  
  gl_FragColor = final_color;
}

