/* tld glsl shader -- fs_mtarini_swampy_map -- by swyter */

uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform vec4 vFogColor;
uniform vec4 input_gamma;
uniform vec4 output_gamma_inv;

uniform float time_var;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;
varying vec4 outSpec0;
varying vec4 outSunLight0;

#define MAP_SPECIAL_SWAMP true
#define MAP_BLEND_SMOOTH false
#define MAP_BLEND_HARD false
#define MAP_BLEND_MID true

void main()
{
    vec4 tex_col = texture2D(diffuse_texture, outTexCoord * 3.0);
    vec4 tex_sdw = texture2D(diffuse_texture_2, (outTexCoord * 0.2f) + (time_var * 0.02f));

	//tex_col.rgb = pow(tex_col.rgb, input_gamma.rgb);

    gl_FragColor = tex_col * (tex_sdw * outColor0 + outSunLight0);

	if (MAP_SPECIAL_SWAMP)
	{
        // artificial color for swamp
        vec4 swampCol = gl_FragColor + vec4(+0.015, +0.015, +0.085, 0.0);
        gl_FragColor = (outSpec0.x > 0.0) ? swampCol : gl_FragColor;
	}

	if (MAP_BLEND_SMOOTH)
	{
        gl_FragColor.w = outColor0.a;
	}

  	if (MAP_BLEND_HARD)
  	{
        gl_FragColor.w = clamp(
         (0.5 + (outColor0.a - 0.5) * 2.0 + (tex_col.a - 0.5))
        , 0.0, 1.0);
	}

 	if (MAP_BLEND_MID)
 	{
        gl_FragColor.w = clamp(
         (0.5) * outColor0.a +
         (0.5) * (0.5 + (outColor0.a - 0.5) * 2.0 + (tex_col.a - 0.5))
        , 0.0, 1.0);
	}
}
