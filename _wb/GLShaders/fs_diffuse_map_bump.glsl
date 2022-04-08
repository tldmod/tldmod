uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec2 Tex0;
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
  tmpvar_2.xyz = (tex_col_1.xyz * (Color.xyz + (
    (clamp (dot ((
      (2.0 * texture2D (normal_texture, (Tex0 * 1.4)).xyz)
     - 1.0), SunLightDir), 0.0, 1.0) * tmpvar_4)
   * vMaterialColor).xyz));
  tmpvar_2.w = Color.w;
  float tmpvar_5;
  tmpvar_5 = (1.0 - clamp (dot (
    normalize(ViewDir)
  , 
    normalize(WorldNormal)
  ), 0.0, 1.0));
  tmpvar_2.xyz = (tmpvar_2.xyz * max (0.6, (
    (tmpvar_5 * tmpvar_5)
   + 0.1)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = clamp(tmpvar_2, 0., 1.);
}

