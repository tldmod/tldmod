uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying float Fog;
varying vec4 Color;
varying vec3 Tex0;
varying vec4 SunLight;
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
  vec4 tmpvar_2;
  vec4 tmpvar_3;
  tmpvar_3 = texture2D (diffuse_texture, Tex0.xy);
  tex_col_1.w = tmpvar_3.w;
  tex_col_1.xyz = pow (tmpvar_3.xyz, vec3(2.2, 2.2, 2.2));
  tex_col_1.xyz = (tex_col_1.xyz + clamp ((
    (Tex0.z * tmpvar_3.w)
   - 1.5), 0.0, 1.0));
  tex_col_1.w = 1.0;

  vec4 tex_sdw = swy_scrolling_cloud_shadows(Tex0.xy);

  tmpvar_2.xyz = (clamp (tex_col_1, 0.0, 1.0) * (tex_sdw * Color + SunLight)).xyz;
  tmpvar_2.w = Color.w;
  tmpvar_2.xyz = (tmpvar_2.xyz * max (0.6, (
    (1.0 - clamp (dot (ViewDir, WorldNormal), 0.0, 1.0))
   + 0.1)));
  tmpvar_2.xyz = pow (tmpvar_2.xyz, output_gamma_inv.xyz);
  tmpvar_2.xyz = mix (vFogColor.xyz, tmpvar_2.xyz, Fog);
  gl_FragColor = tmpvar_2;
}

