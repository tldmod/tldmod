uniform sampler2D diffuse_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec2 Tex0;
varying vec4 SunLight;
varying float Fog;
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
  vec4 tmpvar_2;

  vec4 tex_col = texture2D (diffuse_texture, Tex0);
       tex_col = vec4(pow(tex_col.xyz, vec3(2.2)), tex_col.w);

  vec4 tex_sdw = swy_scrolling_cloud_shadows(Tex0);


  tmpvar_2 = (tex_col * (tex_sdw * Color + SunLight));
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
  gl_FragColor = clamp(tmpvar_2, 0., 1.);
}

