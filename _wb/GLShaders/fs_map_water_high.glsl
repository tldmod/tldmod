uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture2;

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
varying float Fog;

varying vec2  _worldpos;     //swy-- pass the world pos to pixel shader
varying vec2  _sawtooth_fn;  //      together with the sawtooth for sampling
varying float _triangle_fn;  //      and the synced triangle wave for masking...

void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.zw = PosWater.zw;
  vec3 normal_2;
  vec4 tex_col_3;
  vec4 tmpvar_4;
  tmpvar_4.w = Color.w;
  vec4 tmpvar_5;



    //swy-- unpack vector range from 0.0f - 1.0f to -1.0f - 1.0f

    vec4 flow_sample   = texture2D(diffuse_texture2, _worldpos.xy);
    vec2 flow_vector   = (flow_sample.rg * 2.0f) - 1.0f;
    float noise_sample = flow_sample.b;

    flow_vector.x *= -1.f;

    //swy-- sample two times at different points, and show the less
    //      stretched one at the right time in cycles, permuted by the noise to limit pulsing...

    vec4 sample_a = texture2D(diffuse_texture, vec2((_worldpos.xy*32.0) + (flow_vector*(_sawtooth_fn.x - noise_sample) * 0.5)));
    vec4 sample_b = texture2D(diffuse_texture, vec2((_worldpos.xy*32.0) + (flow_vector*(_sawtooth_fn.y - noise_sample) * 0.5)));

    vec4 tex_col = mix(sample_a.rgba, sample_b.rgba, _triangle_fn);



  tmpvar_5 = tex_col;
  tex_col_3.w = tmpvar_5.w;
  tex_col_3.xyz = pow (tmpvar_5.xyz, vec3(2.2, 2.2, 2.2));
  normal_2.xy = ((2.0 * texture2D (normal_texture, (Tex0 * 8.0)).wy) - 1.0);
  normal_2.z = sqrt(max (1e-06, (1.0 -
    dot (normal_2.xy, normal_2.xy)
  )));
  vec3 tmpvar_6;
  tmpvar_6 = normalize(normal_2);
  normal_2 = tmpvar_6;
  float tmpvar_7;
  tmpvar_7 = (1.0 - clamp (dot (
    normalize(CameraDir)
  , tmpvar_6), 0.0, 1.0));
  tmpvar_4.xyz = (Color.xyz + ((0.0204 +
    (((0.9796 * tmpvar_7) * (tmpvar_7 * tmpvar_7)) * (tmpvar_7 * tmpvar_7))
  ) * Color.xyz));
  vec4 tex_8;
  tmpvar_1.xy = (PosWater.xy + (0.35 * tmpvar_6.xy));
  vec4 tmpvar_9;
  tmpvar_9 = texture2DProj (env_texture, tmpvar_1);
  tex_8.w = tmpvar_9.w;
  tex_8.xyz = pow (tmpvar_9.xyz, output_gamma.xyz);
  tex_8.xyz = min (tex_8.xyz, 4.0);
  tmpvar_4.xyz = (tmpvar_4.xyz * (clamp (
    dot (tmpvar_6, LightDir)
  , 0.0, 1.0) * mix (tex_col_3.xyz, tex_8.xyz, reflection_factor)));
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  tmpvar_4.w = (Color.w * tmpvar_5.w);


	tmpvar_4.a  = tmpvar_4.a * tmpvar_4.a * tmpvar_4.a;

	//swy-- tint tweaks
	//Output.RGBColor.b *= pow(1.f, 1.f-tex_col.a);
	tmpvar_4 *= vec4(0.77f, 0.77f, 0.80f, 0.95f);
	tmpvar_4.rgb += (flow_sample.x * 0.03f);

  gl_FragColor = tmpvar_4;
}

