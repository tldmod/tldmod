/* swy: don't set version 130 as macOS doesn't support it */

uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec3 outTexCoord;

void main ()
{
    vec2 uv = outTexCoord.xy;
    vec4 sample = texture2D(diffuse_texture, uv);

    /* this basically is a boolean variable from the vertex shader that makes
       the outline/shadow either black or white, depending on the font color. */
    float bordColor = outTexCoord.z;
    float bord = clamp((1.0 - sample.r) * 2.0, 0., 1.);

    vec4 RGBColor; RGBColor.a = outColor0.a * (bord * (0.40 + 0.30 * (1.0 - sample.g)) + sample.a);

    float isB = (1.0 - sample.a) * (1.0 - 0.);

    RGBColor.rgb = outColor0.rgb * (1.0 - isB) + vec3(bordColor) * (isB);

    gl_FragColor = RGBColor;
}

