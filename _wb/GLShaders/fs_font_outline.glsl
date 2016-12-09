uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;

const float smoothing = 1.0/16.0;

float intour( in float d, in float w ){
    return smoothstep(0.52 - w, 0.52 + w, d);
}

float contour( in float d, in float w ){
    return smoothstep(0.30 - w, 0.45 + w, d);
}
float samp( in vec2 uv, float w ){
    return contour( texture2D(diffuse_texture,uv).r, w );
}
float intsamp( in vec2 uv, float w ){
    return intour( texture2D(diffuse_texture,uv).r, w );
}


void main ()
{

/*
  vec4 finalColor_1;
  vec4 tmpvar_2, subpixel;
  tmpvar_2 = texture2D(diffuse_texture, outTexCoord);
  subpixel = texture2D(diffuse_texture, outTexCoord + vec2(+.001, +.001)) +
             texture2D(diffuse_texture, outTexCoord + vec2(+.001, -.001)) +
             texture2D(diffuse_texture, outTexCoord + vec2(-.001, +.001));

  tmpvar_2 = ((tmpvar_2      ) * 0.8) +
             ((subpixel / 3.0) * 0.2);

  finalColor_1.a = ((1.0 - tmpvar_2.r) + tmpvar_2.a);
  finalColor_1.rgb = (outColor0.xyz * (tmpvar_2.a + 0.05));
  vec4 tmpvar_3;
  tmpvar_3 = clamp (finalColor_1, 0.0, 1.0);
  finalColor_1 = tmpvar_3;
  gl_FragColor = tmpvar_3;


vec2 uv = outTexCoord;

    float dscale = 0.354; // half of 1/sqrt2; you can play with this
    vec2 duv = /*dscale * / (dFdx(uv) + dFdy(uv));


  float alpha = smoothstep(0.5 - .03, 0.5 + .03, 1.0-tmpvar_2.r);

	gl_FragColor = vec4(outColor0.rgb, alpha * outColor0.a);

  gl_FragColor.a = 1.;
	gl_FragColor.rg = duv;



  //if (tmpvar_2.r > (128./256.)) discard;

	//gl_FragColor = vec4(tmpvar_2);


*/
	// ---

	vec2 uv = outTexCoord.xy;

    float dist = texture2D( diffuse_texture, uv ).r;
    float width = fwidth(dist);

    float alpha = contour( dist, width );

    // ------- (comment this block out to get your original behavior)
    // Supersample, 4 extra points
    float dscale = 0.354; // half of 1/sqrt2; you can play with this
    vec2 duv = dscale * (dFdx(uv) + dFdy(uv));
    vec4 box = vec4(uv-duv, uv+duv);

    float asum = samp( box.xy, width )
               + samp( box.zw, width )
               + samp( box.xw, width )
               + samp( box.zy, width );

    // weighted average, with 4 extra points having 0.5 weight each,
    // so 1 + 0.5*4 = 3 is the divisor
    alpha = (alpha + 0.5 * asum) / 3.;
    // -------


    float intour = intour( dist, width );

    float isum = intsamp( box.xy, width )
               + intsamp( box.zw, width )
               + intsamp( box.xw, width )
               + intsamp( box.zy, width );

    intour = (intour + 0.5 * isum) / 3.;

    gl_FragColor = vec4(mix(vec3(0.0,0.0,0.0), outColor0.rgb, intour( dist, width )), alpha * outColor0.a);


}

