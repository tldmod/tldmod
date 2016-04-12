uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;
void main ()
{
  vec4 finalColor_1;
  vec4 tmpvar_2;
  tmpvar_2 = texture2D (diffuse_texture, outTexCoord);
  finalColor_1.a = ((1.0 - tmpvar_2.r) + tmpvar_2.a);
  finalColor_1.rgb = (outColor0.xyz * (tmpvar_2.a + 0.05));
  vec4 tmpvar_3;
  tmpvar_3 = clamp (finalColor_1, 0.0, 1.0);
  finalColor_1 = tmpvar_3;
  gl_FragColor = tmpvar_3;
}

