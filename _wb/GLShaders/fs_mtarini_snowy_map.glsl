/* tld glsl shader -- fs_mtarini_snowy_map -- by swyter */

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

vec4 swy_scrolling_cloud_shadows(vec2 uvCoords)
{
    vec4 tex_sdw = texture2D(diffuse_texture_2, (uvCoords    * 0.20) + (time_var * 0.02));
    vec4 tex_sdy = texture2D(diffuse_texture_2, (uvCoords    / 3.)   + (time_var * 0.00005));

    return vec4((clamp((tex_sdw * tex_sdy), 0., 1.) * 1.).rgb , 1.);
}

void main()
{
    vec4 tex_col = texture2D(diffuse_texture, outTexCoord * 3.0);
         tex_col = vec4(pow(tex_col.xyz, vec3(2.2)), tex_col.w);

    vec4 tex_sdw = swy_scrolling_cloud_shadows(outTexCoord);

    // change the following weights to tune snow presence
    float snow = outSpec0.x * 0.70           // effect of altitude on snow presence
                 - 1.4                       // basic snow altitude
                 - (tex_col.w - 0.5) * 2.5;  // effect of alpha channel on snow presence


    snow = clamp(snow, 0.0, 0.85); // snow factor is between 0 and 0.85

    tex_col.xyz = snow * vec3(0.9, 0.9, 0.9) + (1.0 - snow) * tex_col.xyz;


    tex_col *= tex_sdw
             * outColor0                        // shade with Lambertian lighting
             + outSunLight0
             + snow * outSpec0.y                // plus shininess (only for snow)...
             * 1.3 * (1.0 - 0.5 * tex_col.w);   // ...weighted with alpha channel

    gl_FragColor = tex_col;
    gl_FragColor.w = outColor0.w;

    /* add fresnel term to make the surface look velvet soft at glancing angles */
    float fresnel = (1.0 - clamp(dot(normalize(outViewDir), normalize(outWorldNormal)), 0.0, 1.0));
    gl_FragColor.xyz = (gl_FragColor.xyz * max(0.6, ((fresnel * fresnel) + 0.1)));

    gl_FragColor.xyz = pow(gl_FragColor.xyz, output_gamma_inv.xyz);

    /* add fog mixing */
    gl_FragColor.xyz = mix(vFogColor.xyz, gl_FragColor.xyz, outFog);
}
