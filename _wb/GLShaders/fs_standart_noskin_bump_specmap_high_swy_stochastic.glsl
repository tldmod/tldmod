
uniform sampler2D diffuse_texture;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform vec4 vLightDiffuse[4];
uniform vec4 vMaterialColor;
uniform vec4 vSpecularColor;
uniform vec4 vSunColor;
uniform vec4 vAmbientColor;
uniform vec4 vGroundAmbientColor;
uniform vec4 vSkyLightColor;
uniform vec4 vFogColor;
uniform vec4 output_gamma_inv;
uniform float fMaterialPower;
uniform float spec_coef;
uniform int iLightIndices[4];
varying float Fog;
varying vec4 VertexColor;
varying vec2 Tex0;
varying vec3 SunLightDir;
varying vec3 SkyLightDir;
varying vec4 PointLightDir;
varying vec4 ShadowTexCoord;
varying vec3 ViewDir;

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
  vec3 normal_3;
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  normal_3 = ((2.0 * stochasticTex2D (normal_texture, Tex0, false)) - 1.0).xyz;
  vec4 ambientTerm_5;
  ambientTerm_5 = mix (vGroundAmbientColor, vAmbientColor, ((
    dot (normal_3, SkyLightDir)
   + 1.0) * 0.5));
  total_light_2.w = ambientTerm_5.w;
  total_light_2.xyz = (ambientTerm_5.xyz + (vec3(clamp (
    dot (SunLightDir, normal_3)
  , 0.0, 1.0)) * vSunColor.xyz));
  total_light_2 = (total_light_2 + (clamp (
    dot (SkyLightDir, normal_3)
  , 0.0, 1.0) * vSkyLightColor));
  int tmpvar_6;
  tmpvar_6 = iLightIndices[0];
  total_light_2 = (total_light_2 + clamp ((
    (dot (PointLightDir.xyz, normal_3) * vLightDiffuse[tmpvar_6])
   * PointLightDir.w), 0.0, 1.0));
  tmpvar_4.xyz = min (total_light_2.xyz, 2.0);
  tmpvar_4.xyz = (tmpvar_4.xyz * vMaterialColor.xyz);
  vec4 tmpvar_7;
  tmpvar_7 = stochasticTex2D (diffuse_texture, Tex0, false);
  tex_col_1.w = tmpvar_7.w;

  tmpvar_4.xyz = (tmpvar_4.xyz * tex_col_1.xyz);
  tmpvar_4.xyz = (tmpvar_4.xyz * VertexColor.xyz);
  vec4 specColor_8;
  vec4 fSpecular_9;
  vec4 tmpvar_10;
  tmpvar_10.w = 1.0;
  tmpvar_10.xyz = vSpecularColor.xyz;
  specColor_8 = (((0.1 * spec_coef) * tmpvar_10) * dot (stochasticTex2D (specular_texture, Tex0, false).xyz, vec3(0.33, 0.33, 0.33)));
  vec4 tmpvar_11;
  tmpvar_11.w = 1.0;
  tmpvar_11.xyz = vSunColor.xyz;
  fSpecular_9 = ((specColor_8 * tmpvar_11) * pow (clamp (
    dot (normalize((ViewDir + SunLightDir)), normal_3)
  , 0.0, 1.0), fMaterialPower));
  fSpecular_9 = (fSpecular_9 * VertexColor);
  fSpecular_9.xyz = (fSpecular_9.xyz + (specColor_8.xyz * ShadowTexCoord.xyz));
  int tmpvar_12;
  tmpvar_12 = iLightIndices[0];
  fSpecular_9 = (fSpecular_9 + ((
    (specColor_8 * vLightDiffuse[tmpvar_12])
   * 
    (PointLightDir.w * 0.5)
  ) * pow (
    clamp (dot (normalize((ViewDir + PointLightDir.xyz)), normal_3), 0.0, 1.0)
  , fMaterialPower)));
  tmpvar_4 = (tmpvar_4 + fSpecular_9);
  tmpvar_4.xyz = pow (tmpvar_4.xyz, output_gamma_inv.xyz);
  tmpvar_4.xyz = mix (vFogColor.xyz, tmpvar_4.xyz, Fog);
  tmpvar_4.w = VertexColor.w;
  gl_FragColor = tmpvar_4;
}

