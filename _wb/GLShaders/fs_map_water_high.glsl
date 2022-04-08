/* tld glsl shader -- fs_map_water_high -- by swyter */

uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform sampler2D env_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma;
uniform vec4 output_gamma_inv;
uniform float reflection_factor;
varying vec4 Color;
varying vec2 Tex0;
varying vec3 LightDir;
varying vec3 CameraDir;
varying vec4 PosWater;

varying  vec2 worldpos;      //swy-- pass the world pos to pixel shader
varying  vec2 sawtooth_fn;   //      together with the sawtooth for sampling
varying float triangle_fn;   //      and the synced triangle wave for masking...

uniform sampler2D diffuse_texture_2;
uniform float time_var;

varying float Fog;
void main ()
{
  //swy-- unpack vector range from 0.0f - 1.0f to -1.0f - 1.0f

  vec4  flow_sample = texture2D(diffuse_texture_2, worldpos.xy);
  vec2  flow_vector = (flow_sample.rg * 2.0) - 1.0;
  float noise_sample = flow_sample.b;

  flow_vector.x *= -1.;

  //swy-- sample two times at different points, and show the less
  //      stretched one at the right time in cycles, permuted by the noise to limit pulsing...

  vec4 sample_a = texture2D(diffuse_texture, (worldpos.xy*32.) + (flow_vector*(sawtooth_fn.x - noise_sample) * .5));
  vec4 sample_b = texture2D(diffuse_texture, (worldpos.xy*32.) + (flow_vector*(sawtooth_fn.y - noise_sample) * .5));

  vec4 tex_col = mix(sample_a.rgba, sample_b.rgba, triangle_fn);

  vec4 tmpvar_1;
  tmpvar_1.zw = PosWater.zw;
  vec3 normal_2;
  vec4 tex_col_3;
  vec4 tmpvar_4;
  tmpvar_4.w = Color.w;
  vec4 tmpvar_5;
  //tmpvar_5 = texture2D (diffuse_texture, Tex0);


  tmpvar_5 = tex_col;

  tex_col_3.w = tmpvar_5.w;
  tex_col_3.xyz = pow (tmpvar_5.xyz, vec3(2.2, 2.2, 2.2));
  normal_2.xy = vec2(0, 0); // ((2.0 * texture2D (normal_texture, (Tex0 * 8.0)).wy) - 1.0);
  normal_2.z = sqrt(max (1e-06, (1.0 - 
    dot (normal_2.xy, normal_2.xy)
  )));
  vec3 normalized_normal;
  normalized_normal = normalize(normal_2);
  normal_2 = normalized_normal;
  float tmpvar_7;
  tmpvar_7 = (1.0 - clamp (dot (
    normalize(CameraDir)
  , normalized_normal), 0.0, 1.0));
  tmpvar_4.xyz = (Color.xyz + ((0.0204 + 
    (((0.9796 * tmpvar_7) * (tmpvar_7 * tmpvar_7)) * (tmpvar_7 * tmpvar_7))
  ) * Color.xyz));
  vec4 tex_8;
  tmpvar_1.xy = (PosWater.xy + (0.35 * normalized_normal.xy));
  vec4 tmpvar_9;
  tmpvar_9 = texture2DProj (env_texture, tmpvar_1);
  tex_8.w = tmpvar_9.w;
  tex_8.xyz = pow (tmpvar_9.xyz, output_gamma.xyz);
  tex_8.xyz = min (tex_8.xyz, 4.0);
  tmpvar_4.xyz = (tmpvar_4.xyz * (clamp (
    dot (normalized_normal, LightDir)
  , 0.0, 1.0) * mix (tex_col_3.xyz, tex_8.xyz, reflection_factor)));
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  tmpvar_4.w = (Color.w * tmpvar_5.w);
  gl_FragColor = tmpvar_4; //vec4((texture2D (diffuse_texture_2, worldpos.xy)).rgb,1.).rrrr;// tmpvar_4;

  //swy-- tint tweaks
  gl_FragColor *= vec4(0.77, 0.77, 0.80, 0.95);
  gl_FragColor.rgb += (flow_sample.x*0.03);
}

