uniform sampler2D diffuse_texture;

uniform vec4 vAmbientColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
varying float Fog;
varying vec4 Color;
varying vec3 Tex0;
varying vec4 SunLight;

#define SWY_NIFTY_WATER true

void main ()
{
	vec4 tex_col = texture2D(diffuse_texture, Tex0.xy);

	if (SWY_NIFTY_WATER)
	{
		vec4 tex_col_b = texture2D(diffuse_texture, Tex0.xz);

		tex_col     *= tex_col_b;
		//tex_col.rgb += tex_col_b.rgb / 1.5f;
	}

	gl_FragColor =  tex_col;
	gl_FragColor.xyz = mix(vFogColor.xyz, gl_FragColor.xyz, Fog);
}

