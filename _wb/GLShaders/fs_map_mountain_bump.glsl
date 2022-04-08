uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform vec4 vSunColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec3 Tex0;
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
  tmpvar_3 = (clamp (tex_col_1, 0.0, 1.0) * (tex_sdw * Color + (
    clamp (dot (((2.0 * texture2D (normal_texture, 
      (Tex0.xy * 1.4)
    ).xyz) - 1.0), SunLightDir), 0.0, 1.0)
   * tmpvar_5)));
  tmpvar_3.xyz = (tmpvar_3.xyz * max (0.6, (
    (1.0 - clamp (dot (ViewDir, WorldNormal), 0.0, 1.0))
   + 0.1)));
  tmpvar_3.w = Color.w;
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

