uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec3 outTexCoord;

/* inner and outer contours, 1.0/255 is invisibly thin <--> 0.0/0 the boldest */
float intour( in float d, in float w ){
    return smoothstep(0.48 - w, 0.48 + w, d);
}
float contour( in float d, in float w ){
    return smoothstep(0.30 - w, 0.49 + w, d);
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
    alpha = (alpha + 0.5 * asum) / 3.;
    // -------

    float intour = intour( dist, width );

    float isum = intsamp( box.xy, width )
               + intsamp( box.zw, width )
               + intsamp( box.xw, width )
               + intsamp( box.zy, width );

    intour = (intour + 0.5 * isum) / 3.;

    /* this basically is a boolean variable from the vertex shader that makes
       the outline/shadow either black or white, depending on the font color. */
    float bordColor = outTexCoord.z;

    gl_FragColor = vec4
    ( /* mix the border and text colors using the inner contour mask.
         modulate the glyph's outer contour by the amount of transparency sent from the engine */
      mix(vec3(bordColor), outColor0.rgb, intour), alpha * outColor0.a
    );
}

