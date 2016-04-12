uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;
void main ()
{
  vec4 finalColor_1;
  finalColor_1.a = 1.0;
  finalColor_1.rgb = (texture2D (diffuse_texture, outTexCoord).rrr + outColor0.rgb);
  gl_FragColor = finalColor_1;
}

