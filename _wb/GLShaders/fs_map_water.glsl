uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying vec4 Color;
varying vec2 Tex0;
varying vec3 CameraDir;

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

  vec3 normal_1;
  vec4 tex_col_2;
  vec4 tmpvar_3;
  tmpvar_3.w = Color.w;

  vec4 tmpvar_4;
  //tmpvar_4 = texture2D (diffuse_texture, Tex0);
  tmpvar_4 = tex_col;

  tex_col_2.w = tmpvar_4.w;
  tex_col_2.xyz = pow (tmpvar_4.xyz, vec3(2.2, 2.2, 2.2));


  normal_1.xy = vec2(0, 0); // ((2.0 * texture2D (normal_texture, (Tex0 * 8.0)).wy) - 1.0);
  normal_1.z = sqrt(max (1e-06, (1.0 - 
    dot (normal_1.xy, normal_1.xy)
  )));
  vec3 tmpvar_5;
  tmpvar_5 = normalize(normal_1);
  normal_1 = tmpvar_5;
  float tmpvar_6;
  tmpvar_6 = (1.0 - clamp (dot (
    normalize(CameraDir)
  , tmpvar_5), 0.0, 1.0));
  tmpvar_3.xyz = (Color.xyz + ((0.0204 + 
    (((0.9796 * tmpvar_6) * (tmpvar_6 * tmpvar_6)) * (tmpvar_6 * tmpvar_6))
  ) * Color.xyz));
  tmpvar_3.xyz = (tmpvar_3.xyz * tex_col_2.xyz);
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  tmpvar_3.w = (Color.w * tmpvar_4.w);
  gl_FragColor = tmpvar_3;

  //swy-- tint tweaks
  gl_FragColor *= vec4(0.77, 0.77, 0.80, 0.95);
  gl_FragColor.rgb += (flow_sample.x*0.03);
}

