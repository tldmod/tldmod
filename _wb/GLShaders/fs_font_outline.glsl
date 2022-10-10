/* swy: don't set version 130 as macOS doesn't support it */

uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec2 outTexCoord;

/* inner and outer contours, 1.0/255 is invisibly thin <--> 0.0/0 the boldest */
float intour( in float d, in float w ){
    return smoothstep(0.51 - w, 0.52 + w, d);
}
float contour( in float d, in float w ){
    return smoothstep(0.30 - w, 0.45 + w, d);
}

/* just simple macros, could be a bit less messy */
float samp( in vec2 uv, float w ){
    return contour( 1.0 - texture2D(diffuse_texture,uv).r, w );
}
float intsamp( in vec2 uv, float w ){
    return intour( 1.0 - texture2D(diffuse_texture,uv).r, w );
}


void main ()
{
 /* supersampled signed font distance technique (with partial derivatives) by /u/glacialthinker on reddit
    https://www.reddit.com/r/gamedev/comments/2879jd/just_found_out_about_signed_distance_field_text/cicatot/ */

    vec2 uv = outTexCoord.xy;

    float dist = 1.0 - texture2D( diffuse_texture, uv ).r;
    float width = fwidth(dist);

    float alpha = contour( dist, width );

    // ------- (comment this block out to get your original behavior)
    // Supersample, 4 extra points
    const float dscale = 0.354; // half of 1/sqrt2; you can play with this
    vec2 duv = dscale * (dFdx(uv) + dFdy(uv));
    vec4 box = vec4(uv-duv, uv+duv);

    float asum = samp( box.xy, width )
               + samp( box.zw, width )
               + samp( box.xw, width )
               + samp( box.zy, width );

    // weighted average, with 4 extra points having 0.5 weight each,
    // so 1 + 0.5*4 = 3 is the divisor
    alpha = (alpha + asum/4.0);
    // -------

    float intour = intour( dist, width );

    float isum = intsamp( box.xy, width )
               + intsamp( box.zw, width )
               + intsamp( box.xw, width )
               + intsamp( box.zy, width );

    intour = (intour + isum/4.0);

    gl_FragColor = clamp(vec4
    ( /* mix the border and text colors using the inner contour mask.
         modulate the glyph's outer contour by the amount of transparency sent from the engine */
      mix(vec3(0.0, 0.0, 0.0).rgb, outColor0.rgb, intour), alpha * outColor0.a
    ), 0.0, 1.0);
}

