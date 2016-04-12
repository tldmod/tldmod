uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec2 Tex0;
varying float Fog;
void main ()
{
  vec4 tex_col_1;
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_3.w;
  tex_col_1.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_2 = (tex_col_1 * Color);
  if ((tmpvar_2.w < 0.1)) {
    discard;
  };
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = tmpvar_2;
}

