uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D normal_texture;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vPointLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying float Fog;
varying vec3 ViewDir;
varying vec3 WorldNormal;
void main ()
{
  vec4 multi_tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  vec4 tmpvar_4;
  tmpvar_4 = vec4(texture2D(diffuse_texture, Tex0).rgb, 1.0);
  multi_tex_col_1.w = 1.0;//tmpvar_4.w;
  multi_tex_col_1.xyz = (tmpvar_4.xyz * (1.0 - VertexColor.w));
  multi_tex_col_1.xyz = (multi_tex_col_1.xyz + (texture2D (diffuse_texture_2, (Tex0 * 1.237)).xyz * VertexColor.w));
  multi_tex_col_1.xyz = pow (multi_tex_col_1.xyz, vec3(2.2, 2.2, 2.2));
  vec3 tmpvar_5;
  tmpvar_5 = ((2.0 * texture2D (normal_texture, Tex0).xyz) - 1.0);
  vec4 tmpvar_6;
  tmpvar_6.w = 1.0;
  tmpvar_6.xyz = vSunColor.xyz;
  total_light_2 = (vAmbientColor + (clamp (
    dot (SunLightDir, tmpvar_5)
  , 0.0, 1.0) * tmpvar_6));
  total_light_2 = (total_light_2 + (clamp (
    dot (SkyLightDir, tmpvar_5)
  , 0.0, 1.0) * vSkyLightColor));
  vec4 tmpvar_7;
  tmpvar_7.w = 1.0;
  tmpvar_7.xyz = vPointLightColor.xyz;
  total_light_2 = (total_light_2 + (clamp (
    dot (PointLightDir.xyz, tmpvar_5)
  , 0.0, 1.0) * tmpvar_7));
  tmpvar_3.xyz = total_light_2.xyz;
  tmpvar_3.w = 1.0;
  tmpvar_3 = (tmpvar_3 * multi_tex_col_1);
  tmpvar_3.xyz = (tmpvar_3.xyz * VertexColor.xyz);
  tmpvar_3.w = (tmpvar_3.w * PointLightDir.w);
  float tmpvar_8;
  tmpvar_8 = (1.0 - clamp (dot (
    normalize(ViewDir)
  ,
    normalize(WorldNormal)
  ), 0.0, 1.0));
  tmpvar_3.xyz = (tmpvar_3.xyz * max (0.6, (
    (tmpvar_8 * tmpvar_8)
   + 0.1)));
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

