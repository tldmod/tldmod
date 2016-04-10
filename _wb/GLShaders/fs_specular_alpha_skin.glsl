uniform sampler2D diffuse_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunDir;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightDir;
uniform vec4 vSkyLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform float spec_coef;
varying float Fog;
varying vec4 VertexColor;
varying vec3 VertexLighting;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec3 ViewDir;
void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  tmpvar_3.w = 1.0;
  total_light_2.w = vAmbientColor.w;
  total_light_2.xyz = (vAmbientColor.xyz + (vec3(clamp (
    dot (-(vSunDir.xyz), SunLightDir)
  , 0.0, 1.0)) * vSunColor.xyz));
  total_light_2 = (total_light_2 + (clamp (
    dot (-(vSkyLightDir.xyz), SunLightDir)
  , 0.0, 1.0) * vSkyLightColor));
  total_light_2.xyz = (total_light_2.xyz + VertexLighting);
  tmpvar_3.xyz = min (total_light_2.xyz, 2.0);
  tmpvar_3.xyz = (tmpvar_3.xyz * vMaterialColor.xyz);
  vec4 tmpvar_4;
  tmpvar_4 = texture2D (diffuse_texture, Tex0);
  tex_col_1.w = tmpvar_4.w;
  tex_col_1.xyz = pow (tmpvar_4.xyz, vec3(2.2, 2.2, 2.2));
  tmpvar_3.xyz = (tmpvar_3.xyz * tex_col_1.xyz);
  tmpvar_3.xyz = (tmpvar_3.xyz * VertexColor.xyz);
  vec4 specColor_5;
  vec4 fSpecular_6;
  vec4 tmpvar_7;
  tmpvar_7.w = 1.0;
  tmpvar_7.xyz = vSpecularColor.xyz;
  specColor_5 = (((0.1 * spec_coef) * tmpvar_7) * tmpvar_4.w);
  vec4 tmpvar_8;
  tmpvar_8.w = 1.0;
  tmpvar_8.xyz = vSunColor.xyz;
  fSpecular_6 = ((specColor_5 * tmpvar_8) * pow (clamp (
    dot (normalize((ViewDir - vSunDir.xyz)), SunLightDir)
  , 0.0, 1.0), fMaterialPower));
  fSpecular_6 = (fSpecular_6 * VertexColor);
  fSpecular_6.xyz = (fSpecular_6.xyz + ((specColor_5.xyz * SkyLightDir) * 0.1));
  tmpvar_3 = (tmpvar_3 + fSpecular_6);
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  tmpvar_3.w = (VertexColor.w * tmpvar_4.w);
  gl_FragColor = tmpvar_3;
}

