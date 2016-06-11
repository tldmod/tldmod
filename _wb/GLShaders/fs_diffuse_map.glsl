uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;

uniform float time_var;

uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
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
  tmpvar_2 = (tex_col_1 * (tex_sdw * Color + SunLight));
  float tmpvar_4;
  tmpvar_4 = (1.0 - clamp (dot (
    normalize(ViewDir)
  ,
    normalize(WorldNormal)
  ), 0.0, 1.0));
  tmpvar_2.xyz = (tmpvar_2.xyz * max (0.6, (
    (tmpvar_4 * tmpvar_4)
   + 0.1)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = clamp(tmpvar_2, 0.0, 1.0);
}

