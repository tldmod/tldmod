/* swy: don't set version 130 as macOS doesn't support it */

uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;

void main ()
{
    vec2 uv = outTexCoord.xy;
    vec4 sample = texture2D(diffuse_texture, uv);
    
    vec4 RGBColor = outColor0;
    RGBColor.a    = (1.0 - sample.r) + sample.a;
    RGBColor.rgb *= 0.6 * sample.a + 0.4;

    gl_FragColor = RGBColor;
}

