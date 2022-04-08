/* tld glsl shader -- fs_mtarini_swampy_map -- by swyter */

uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;

uniform float time_var;

varying vec4 outColor0;
varying vec2 outTexCoord;
varying float outFog;
varying vec4 outSpec0;
varying vec4 outSunLight0;

varying vec3 outViewDir;
varying vec3 outWorldNormal;

#define MAP_SPECIAL_SWAMP true
#define MAP_BLEND_SMOOTH false
#define MAP_BLEND_HARD false
#define MAP_BLEND_MID true

vec4 swy_scrolling_cloud_shadows(vec2 uvCoords)
{
  vec4 tex_sdw = texture2D(diffuse_texture_2, (uvCoords    * 0.20) + (time_var * 0.02));
  vec4 tex_sdy = texture2D(diffuse_texture_2, (uvCoords    / 3.)   + (time_var * 0.00005));

  return vec4((clamp((tex_sdw * tex_sdy), 0., 1.) * 1.).rgb , 1.);
}

void main()
{
    vec4 tex_col = texture2D(diffuse_texture, outTexCoord * 3.0);
    vec4 tex_sdw = swy_scrolling_cloud_shadows(outTexCoord);

    tex_col.rgb = pow(tex_col.rgb, vec3(2.2));

    gl_FragColor = tex_col * (tex_sdw * outColor0 + outSunLight0);

    // gamma correct
    gl_FragColor.rgb = pow(gl_FragColor.xyz, output_gamma_inv.xyz);

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

    /* add fresnel term to make the surface look velvet soft at glancing angles */
    float fresnel = (1.0 - clamp(dot(normalize(outViewDir), normalize(outWorldNormal)), 0.0, 1.0));
    gl_FragColor.xyz = (gl_FragColor.xyz * max(0.6, ((fresnel * fresnel) + 0.1)));

    /* add fog mixing */
    gl_FragColor.xyz = mix(vFogColor.xyz, gl_FragColor.xyz, outFog);
}
