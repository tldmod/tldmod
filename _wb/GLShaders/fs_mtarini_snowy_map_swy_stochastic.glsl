
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


/* swy: technique lifted from «Procedural Stochastic Textures by Tiling and Blending», created by Thomas Deliot and Eric Heitz (turned the GLSL into HLSL)
        https://drive.google.com/file/d/1QecekuuyWgw68HU9tg6ENfrCTCVIjm6l/view */
vec2 hash(ivec2 p)
{
  return fract(sin(mat2(127.1, 311.7, 269.5, 183.3) * vec2(p)) * 43758.5453);
}

// Compute local triangle barycentric coordinates and vertex IDs
void TriangleGrid(vec2 uv,
                  out float w1, out float w2, out float w3,
                  out ivec2 vertex1, out ivec2 vertex2, out ivec2 vertex3
)
{
  // Scaling of the input
  uv *= 3.464; /* 2 * sqrt(3) */
  
  // Skew input space into simplex triangle grid
  const mat2 gridToSkewedGrid = mat2(1.0, 0.0, -0.57735027 /* tan(-30◦) */, 1.15470054 /* Saw-tooth waveform: 2 / sqrt(3) */);
  vec2 skewedCoord = gridToSkewedGrid * uv;
  
  // Compute local triangle vertex IDs and local barycentric coordinates
  ivec2 baseId = ivec2(floor(skewedCoord)   );
  vec3  temp   =  vec3(fract(skewedCoord), 0);
        temp.z = 1.0 - temp.x - temp.y;
  
  if (temp.z > 0.0)
  {
    w1 =       temp.z;
    w2 =       temp.y;
    w3 =       temp.x;
    vertex1 = baseId;
    vertex2 = baseId + ivec2(0, 1);
    vertex3 = baseId + ivec2(1, 0);
  }
  else
  {
    w1 =     - temp.z;
    w2 = 1.0 - temp.y;
    w3 = 1.0 - temp.x;
    vertex1 = baseId + ivec2(1, 1);
    vertex2 = baseId + ivec2(1, 0);
    vertex3 = baseId + ivec2(0, 1);
  }
}

vec4 stochasticTex2D(sampler2D texSampler, vec2 uvCoords, bool gammaCorrect) /* swy: use gamma-correction only for diffuse/real-color textures, not for things like normal or specular maps */
{
#ifdef STOCHASTIC_ENABLED
    float w1, w2, w3; ivec2 vertex1, vertex2, vertex3;
    TriangleGrid(uvCoords, w1, w2, w3, vertex1, vertex2, vertex3);
    
    /* swy: each triangle offsets/nudges the base UV coordinates in a different direction;
            we use the ID as a hash seed, so that for that index the random offset is always the same; it's permanent */
    vec2 uvA = uvCoords + hash(vertex1);
    vec2 uvB = uvCoords + hash(vertex2);
    vec2 uvC = uvCoords + hash(vertex3);
    
    /* swy: manually grab the screen-space derivatives to do correct mipmapping without shimmering, and anisotropic filtering */
    vec2 duvdx = dFdx(uvCoords);
    vec2 duvdy = dFdy(uvCoords);
    
    /* swy: sample the texels of every overlapping triangle under this point; there are always three of them
            note: it's important do the gamma correction right at the start; if we blend and then gamma-correct the result, it will look wrong */
    vec4 texA = textureGrad(texSampler, uvA, duvdx, duvdy); if (gammaCorrect) texA.rgb = pow(texA.rgb, vec3(2.2));
    vec4 texB = textureGrad(texSampler, uvB, duvdx, duvdy); if (gammaCorrect) texB.rgb = pow(texB.rgb, vec3(2.2));
    vec4 texC = textureGrad(texSampler, uvC, duvdx, duvdy); if (gammaCorrect) texC.rgb = pow(texC.rgb, vec3(2.2));
    
    /* swy: use a simple linear blend; no fancy histogram-preserving texture preprocessing here;
            we could also use some kind of height blending, by exploiting the .z channels of
            normalmaps or the albedo itself with some RGB tweaking */
    return (w1 * texA) + (w2 * texB) + (w3 * texC);
#else
    vec4 tex = texture2D(texSampler, uvCoords); if (gammaCorrect) tex.rgb = pow(tex.rgb, vec3(2.2)); return tex;
#endif
}


vec4 stochasticTex2DWithDistFadeOut(sampler2D texSampler, vec2 uvCoords, bool gammaCorrect)
{
    vec4 stocColor = stochasticTex2D(texSampler, uvCoords, gammaCorrect);
    vec4 origColor =       texture2D(texSampler, uvCoords);
    
    if (gammaCorrect)
        origColor.rgb = pow(origColor.rgb, vec3(2.2));
    
    return stocColor;//lerp(origColor, stocColor, .5);
}

/* swy: -- */



vec4 swy_scrolling_cloud_shadows(vec2 uvCoords)
{
    vec4 tex_sdw = texture2D(diffuse_texture_2, (uvCoords    * 0.20) + (time_var * 0.02));
    vec4 tex_sdy = texture2D(diffuse_texture_2, (uvCoords    / 3.)   + (time_var * 0.00005));

    return vec4((clamp((tex_sdw * tex_sdy), 0., 1.) * 1.).rgb , 1.);
}

void main()
{
    vec4 tex_col = stochasticTex2D(diffuse_texture, outTexCoord * 3.0, true);
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
