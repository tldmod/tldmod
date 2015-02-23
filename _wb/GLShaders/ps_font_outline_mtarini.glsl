
varying vec4 outColor0;
varying vec3 outTexCoord;

void main()
{ 
  vec4 sample = texture2D(FontTextureSampler, outTexCoord.xy);

	float bord = clamp( (1.0-sample.r)*2.0, 0.0, 1.0 );
	float bordColor = outTexCoord.z;

	gl_FragColor.a = outColor0.a *(bord*(0.40+0.30*(1.0-sample.g)) + sample.a);

	float isB = (1.0-sample.a) * (1.0-sample.g);

	gl_FragColor.rgb = outColor0.rgb * (1.0-isB) + vec3(bordColor,bordColor,bordColor)* (isB);
}
