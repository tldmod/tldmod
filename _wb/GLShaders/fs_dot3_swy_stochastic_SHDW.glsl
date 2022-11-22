
uniform sampler2D diffuse_texture;
uniform sampler2D normal_texture;
uniform sampler2D shadowmap_texture;
uniform vec4 vMaterialColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vPointLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fShadowMapNextPixel;
uniform float fShadowMapSize;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
varying float Fog;
varying vec3 ViewDir;
varying vec3 WorldNormal;

uniform sampler2D diffuse_texture_2;
uniform float time_var;

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

void main ()
{
  vec4 tex_col_1;
  vec4 total_light_2;
  vec4 tmpvar_3;
  total_light_2 = vAmbientColor;
  vec3 tmpvar_4;
  tmpvar_4 = ((2.0 * stochasticTex2D(normal_texture, Tex0, false).xyz) - 1.0);
  float sun_amount_5;
  sun_amount_5 = 0.0;
  vec2 tmpvar_6;
  tmpvar_6 = fract((ShadowTexCoord.xy * fShadowMapSize));
  vec4 tmpvar_7;
  tmpvar_7 = texture2D (shadowmap_texture, ShadowTexCoord.xy);
  float tmpvar_8;
  if ((tmpvar_7.x < ShadowTexCoord.z)) {
    tmpvar_8 = 0.0;
  } else {
    tmpvar_8 = 1.0;
  };
  vec2 tmpvar_9;
  tmpvar_9.y = 0.0;
  tmpvar_9.x = fShadowMapNextPixel;
  vec4 tmpvar_10;
  tmpvar_10 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_9));
  float tmpvar_11;
  if ((tmpvar_10.x < ShadowTexCoord.z)) {
    tmpvar_11 = 0.0;
  } else {
    tmpvar_11 = 1.0;
  };
  vec2 tmpvar_12;
  tmpvar_12.x = 0.0;
  tmpvar_12.y = fShadowMapNextPixel;
  vec4 tmpvar_13;
  tmpvar_13 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + tmpvar_12));
  float tmpvar_14;
  if ((tmpvar_13.x < ShadowTexCoord.z)) {
    tmpvar_14 = 0.0;
  } else {
    tmpvar_14 = 1.0;
  };
  vec4 tmpvar_15;
  tmpvar_15 = texture2D (shadowmap_texture, (ShadowTexCoord.xy + vec2(fShadowMapNextPixel)));
  float tmpvar_16;
  if ((tmpvar_15.x < ShadowTexCoord.z)) {
    tmpvar_16 = 0.0;
  } else {
    tmpvar_16 = 1.0;
  };
  sun_amount_5 = clamp (mix (mix (tmpvar_8, tmpvar_11, tmpvar_6.x), mix (tmpvar_14, tmpvar_16, tmpvar_6.x), tmpvar_6.y), 0.0, 1.0);
  vec4 tmpvar_17;
  tmpvar_17.w = 1.0;
  tmpvar_17.xyz = vSunColor.xyz;
  total_light_2 = (vAmbientColor + ((
    clamp (dot (SunLightDir, tmpvar_4), 0.0, 1.0)
   * 
    (sun_amount_5 * sun_amount_5)
  ) * tmpvar_17));
  total_light_2 = (total_light_2 + (clamp (
    dot (SkyLightDir, tmpvar_4)
  , 0.0, 1.0) * vSkyLightColor));
  vec4 tmpvar_18;
  tmpvar_18.w = 1.0;
  tmpvar_18.xyz = vPointLightColor.xyz;
  total_light_2 = (total_light_2 + (clamp (
    dot (PointLightDir.xyz, tmpvar_4)
  , 0.0, 1.0) * tmpvar_18));
  tmpvar_3.xyz = total_light_2.xyz;
  tmpvar_3.w = 1.0;
  tmpvar_3 = (tmpvar_3 * vMaterialColor);

  tex_col_1 = stochasticTex2D(diffuse_texture, Tex0, true);

  tmpvar_3 = (tmpvar_3 * tex_col_1);
  tmpvar_3 = (tmpvar_3 * VertexColor);
  float tmpvar_20;
  tmpvar_20 = (1.0 - clamp (dot (ViewDir, WorldNormal), 0.0, 1.0));
  tmpvar_3.xyz = (tmpvar_3.xyz * max (0.6, (
    (tmpvar_20 * tmpvar_20)
   + 0.1)));
  tmpvar_3.xyz = pow (tmpvar_3.xyz, output_gamma_inv.xyz);
  if ((tmpvar_3.w < 0.05)) {
    discard;
  };
  tmpvar_3.xyz = mix (vFogColor.xyz, tmpvar_3.xyz, Fog);
  gl_FragColor = tmpvar_3;
}

